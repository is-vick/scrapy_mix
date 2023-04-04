from scrapy_mix.core.parts.nodes import Response
import time
import asyncio

class AioHttpDownLoader:
    def __init__(self, manager, create_session) -> None:
        self.manager = manager
        self.create_session = create_session

    async def download(self, request):
        # await asyncio.sleep(1)
        # response = Response(url=request.url, status=200, content=b'hello my scrapy', meta=request.meta, headers=request.headers)
        # # self.manager.responses.put((request, response))
        # return (request, response)
        
        functions = {'get': self.session.get, 'post': self.session.post, 'put': self.session.put, 'head':self.session.head, 'delete': self.session.delete, 'options': self.session.options, 'patch': self.session.patch}

        async with functions[request.method](**self.__argument_filter(request)) as resp:
            content = await resp.read()
            resp = Response(url=resp.url, status=resp.status, content=content, meta=request.meta, headers=resp.headers)
            return (request,resp)

    
    async def open_spider(self):
        self.session = await self.create_session()

    async def close_spider(self):
        await self.session.close()
        await asyncio.sleep(5)

    def __argument_filter(self, reqeust):
        tmp = {}
        for k, v in reqeust.__dict__.items():
            if k in ['callback', 'method', 'meta', 'request_type']:
                continue
            tmp[k] = v
        return tmp


class SeleniumDownloader:
    def __init__(self, manager, webdriver, options, desired_capabilities) -> None:
        self.manager = manager
        self.webdriver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)

    def download(self, request):
        # response = Response(url=request.url, status=200, content=b'hello my scrapy', meta=request.meta, headers=request.headers)
        # if request.action:
        #     self.manager.clawer.tree_manager.action(request=request, driver=self.cwebdriver)
        # # self.manager.responses.put((request, response))
        # return (request, response)


        self.webdriver.get(url=request.url)
        time.sleep(0.5)
        if request.action:
            self.manager.clawer.tree_manager.action(request=request, driver=self.cwebdriver)
            time.sleep(0.5)
        pagesource = self.webdriver.page_source
        response = Response(url=self.webdriver.current_url, status=200, content=pagesource.encode(), meta=request.meta, headers=request.headers)
        return (request, response)
    
    async def open_spider(self):
        pass

    async def close_spider(self):
        pass