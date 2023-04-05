"""
一个爬虫框架的实现，其中包含了多个管理器类，分别用于管理管道、中间件、引擎、下载器、树和异步队列。具体来说，
PipeManager 管理处理管道，MidWareManager 管理中间件，EngineManager 管理引擎，DownloaderManager 管理下载器，TreeManager 管理树，AsyncQueueManager 管理异步队列。
这些管理器类都包含了一些方法，用于管理和处理相应的数据和操作。
例如，EngineManager 中的 create_engines 方法用于创建引擎对象，start_engines 方法用于启动引擎，tree_callback 方法用于处理树的回调函数等等。
整个爬虫框架的实现是基于这些管理器类的相互协作和调用。
"""


from scrapy_mix.parts.engine import Engine
from scrapy_mix.parts.nodes import Item, AioHttpRequest, SeleniumRequest
from scrapy_mix.parts.downloaders import AioHttpDownLoader, SeleniumDownloader
from scrapy_mix.parts.stackers import *

from settings.aiohttp_settings import create_session
from settings.selenium_seletings import options, desired_capabilities
from settings import clawer_settings

from importlib import import_module
from queue import Queue, LifoQueue
from selenium import webdriver

import asyncio
import json
import time
import os


def create_obj_from_path_dt_2lt(paths_dt):
    obj_lt = []
    for path in sorted(paths_dt.items(), key= lambda x: x[1]):
        dot =path[0].rindex('.')
        modul, name = path[0][:dot], path[0][dot+1:]
        mod = import_module(modul)
        obj = getattr(mod, name)
        obj_lt.append(obj())
    return obj_lt

def create_obj_from_path_dt_2dt(paths_dt):
    obj_dt = {}
    for path in sorted(paths_dt.items(), key= lambda x: x[1]):
        dot =path[0].rindex('.')
        modul, name = path[0][:dot], path[0][dot+1:]
        mod = import_module(modul)
        obj = getattr(mod, name)
        obj_dt[path[0]] = obj()
    return obj_dt


class PipeManager:
    """
        class PipeManager
    """
    def __init__(self, clawer) -> None:
        self.item_queue = Queue()
        self.clawer = clawer
        self.pipes = create_obj_from_path_dt_2lt(clawer_settings.PIPES)


    def open_spider(self):
        for pipe in self.pipes:
            pipe.open_spider()

    async def process(self):
        while not self.item_queue.empty():
            curr_item = self.item_queue.get()
            for pipe in self.pipes:
                await pipe.process_itemnode(itemnode=curr_item)

    async def process_items(self):
        return asyncio.create_task(self.process())

    def close_spider(self):
        for pipe in self.pipes:
            pipe.close_spider()


class MidWareManager:
    def __init__(self, clawer) -> None:
        self.calwer = clawer
        self.midwares = create_obj_from_path_dt_2lt(clawer_settings.MIDWARES)

    def open_spider(self):
        for midware in self.midwares:
            midware.open_spider()

    def process_request(self, request):
        for midware in self.midwares:
            midware.process_request(request=request)

    def process_response(self, response):
        for midware in self.midwares:
            midware.process_response(response=response)

    def close_spider(self):
        for midware in self.midwares:
            midware.close_spider()


class EngineManager:
    def __init__(self, clawer) -> None:
        self.tasks = []
        self.curr_node = None
        self.clawer = clawer
        self.create_engines()
    
    def create_engines(self):
        self.workshop = Queue(clawer_settings.ENGINE_NUM)
        self.rosters = Queue(clawer_settings.ENGINE_NUM)
        for i in range(clawer_settings.ENGINE_NUM):
            en = Engine(manager=self, stacker=eval(f'{clawer_settings.ENGINE_STACKER_TYPE}()'), en_id = 0.1*i)
            self.workshop.put(en)
            self.rosters.put(en)

    async def start_engines(self):
        while not self.workshop.empty() and not self.clawer.async_queue_manager.queue.empty():
            self.curr_node = self.clawer.async_queue_manager.queue.get()
            en = self.workshop.get()
            en.stacker.put(self.curr_node)
            self.curr_node = None
            self.tasks.append(en.core())
        await asyncio.gather(*self.tasks)
        self.tasks.clear()

    def interrupt_record(self):
        records = 0
        stackers = []
        while not self.rosters.empty():
            en = self.rosters.get()
            stacker = self.engine_interrupt_record(engine=en)
            records += len(stacker)
            stackers.append(stacker)
        return records ,stackers

    async def interrupt_recovery(self, stackers):
        while len(stackers) != 0:
            while not self.workshop.empty() and len(stackers) != 0:
                en = self.workshop.get()
                self.eingie_interrupt_recovery(engine=en, stacker=stackers.pop())
                self.tasks.append(en.core())
            await asyncio.gather(*self.tasks)
            self.tasks.clear()
    
    def engine_interrupt_record(self, engine):
        if type(engine.curr_node) is tuple:
            self.clawer.midware_manager.process_response(response=engine.curr_node[1])
            self.tree_callback(engine=engine, request=engine.curr_node[0], response=engine.curr_node[1])
        elif isinstance(engine.curr_node, AioHttpRequest) or isinstance(engine.curr_node, SeleniumRequest):
            engine.stacker.put(engine.curr_node)
        tmp = []
        while not engine.stacker.empty():
            tmp.append(engine.stacker.get().load2dict())
        return tmp

    def eingie_interrupt_recovery(self, engine, stacker):
        while len(stacker) > 0:
            request_dict = stacker.pop()
            if request_dict['request_type'] == 'AioHttpRequest':
                self.clawer.async_queue_manager.queue.put(AioHttpRequest(**request_dict))
            elif request_dict['request_type'] == 'SeleniumRequest':
                self.clawer.async_queue_manager.queue.put(SeleniumRequest(**request_dict))
            else:
                raise TypeError('no such reqeust')

    def tree_callback(self, engine, request, response):
        for node in self.clawer.tree_manager.callback(request, response):
            self.__auditor(engine, node=node)
        engine.curr_node = None
    
    def __auditor(self, engine, node):
        if isinstance(node, Item):
            self.clawer.pipe_manager.item_queue.put(node)
        elif isinstance(node, AioHttpRequest) or isinstance(node, SeleniumRequest):
            if node.meta.get('async', False) == True:
                self.clawer.async_queue_manager.queue.put(node)
            else:
                engine.stacker.put(node)
        else:
            raise TypeError('only can request object or item object')

    def is_error(self,request):
        error = request.meta.get('error', None)
        if error:
            mesg = error.split('#')
            times = int(mesg[0])
            if times >= 4:
                return True
            request.meta['error'] = f'{times+1}#{error[1]}'
            self.clawer.async_queue_manager_queue.queue.put(request)
            return True


class DownloaderManager:
    def __init__(self, clawer) -> None:
        self.responses = Queue(clawer_settings.ENGINE_NUM)
        self.clawer = clawer
        self.create_downloader()

    def create_downloader(self):
        self.downloaders = {}
        if clawer_settings.AIOHTTPDOWNLOADER:
            self.downloaders['AioHttpDownLoader'] = AioHttpDownLoader(manager=self, create_session=create_session)
        if clawer_settings.SELENIUMDOWNLOADER:
            self.downloaders['SeleniumDownLoader'] = SeleniumDownloader(manager=self, webdriver=webdriver, options=options, desired_capabilities=desired_capabilities)

    async def open_spider(self):
        for k,v in self.downloaders.items():
            await v.open_spider()

    async def close_spider(self):
        for k,v in self.downloaders.items():
            await v.close_spider()

    async def download(self, request):
        print('downloading ...........................')
        if isinstance(request, AioHttpRequest):
            if clawer_settings.DELAY:
                time.sleep(clawer_settings.DELAY)
            return await self.downloaders['AioHttpDownLoader'].download(request=request)
        elif isinstance(request, SeleniumRequest):
            return self.downloaders['SeleniumDownLoader'].download(request=request)
        else:
            raise TypeError('no such downloader!!!')


class TreeManager:
    def __init__(self, clawer) -> None:
        self.clawer = clawer
        self.trees = create_obj_from_path_dt_2dt(clawer_settings.TREES)


    def start_nodes(self):
        for tree in self.trees.keys():
            for request in self.trees[tree].start_nodes():
                self.clawer.async_queue_manager.queue.put(request)
    
    def callback(self, request, response):
        method = request.callback.rsplit('.', 1)
        callback = getattr(self.trees[method[0]], method[-1])
        for node in callback(response):
            yield node
    
    def action(self, request, driver):
        method = request.action.rsplit('.',1)
        action = getattr(self.trees[method[0]], method[-1])
        action(driver)


class InterruptManager:
    def __init__(self, clawer) -> None:
        self.clawer = clawer

    async def interrupt_record(self):
        """
        record the data when occur interrupt exception
        """
        records = 0
        cache = {}
        async_queue = []
        if self.clawer.engine_manager.curr_node:
            async_queue.append(self.clawer.engine_manager.curr_node.load2dict())

        while not self.clawer.async_queue_manager.queue.empty():
            async_queue.append(self.clawer.async_queue_manager.queue.get().load2dict())

        cache['async_queue'] = async_queue

        records += len(async_queue)

        num, cache['stackers'] = self.clawer.engine_manager.interrupt_record()

        cache['records'] = records + num
        with open('cache.json', 'w') as f:
            json.dump(cache, f, ensure_ascii=True)
            
        await self.clawer.close_spider()
   

    async def interrupt_recovery(self, cache):
        """
        recovery last time's data when occur interrupt exception
        """
        print('records:', cache['records'])
        print('Recoverying data...........')
        for request_dict in cache['async_queue']:
            if request_dict['request_type'] == 'AioHttpRequest':
                self.clawer.async_queue_manager.queue.put(AioHttpRequest(**request_dict))
            elif request_dict['request_type'] == 'SeleniumRequest':
                self.clawer.async_queue_manager.queue.put(SeleniumRequest(**request_dict))
        await self.clawer.engine_manager.interrupt_recovery(stackers=cache['stackers'])

    def non_interrupt_do(self):
        try:
            os.remove('cache.json')
        except Exception as e:
            pass

    def cache(self):
        try:
            with open('cache.json', 'r') as f:
                cache = json.load(f)
                if cache['records'] != 0:
                    return cache
        except Exception as e:
            return


class AsyncQueueManager:
    def __init__(self, clawer) -> None:
        self.queue = Queue()
        self.clawer = clawer
