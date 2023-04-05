@import "https://haogeshuohuanihaohaoting.github.io/static/mdCreateMenu.js"
# Scrapy_mix
`python 3.10`

## 1.Diagram
- The frame incloude multiple manager class, they use to manage pipes, middlewares, engines, downloaders and async queue.  

- Specifcally, PipeManager manage pipes, MidWareManage manage middlewares, EngineManager manage engines, DownloaderManager manage downloaders, TreeManager manage trees and AsyncQueueManager manage async queue. This manager has lots of method to manager and process relared data.   

- For example, EngineManager.create_engines to create engines obj, EngineManager.start_engines to start engines, TreeManager.start_nodes to put the first reqeusts into async queue, TreeManager.tree_callback to process trees's callback function. All the frame need this manager to help each other. 
-  ![scrapy_mix diagram](/scrapy_mix.png)  
  
1. `TreeManager put first requests into async queue.`  
2. `EngineManager get reqeusts from async queue and put into itself stacker.`  
3. `EngineManager hand reqeuets in MidwareManager to process requests then let it into DwonloaderManager.`  
4. `DownloaderManager according the request to send reqeust and return response.`  
5. `MidwareManager process response and put it into engine.`  
6. `EngineManager put response into TreeManager then call trees's callback, and according callback's return value's type put it inot PipeManager, AsuncQueueManager or self's stacker, if type of Item put it into PipeManager, if type of request put into self's stacker, if async request put it into AsyncQueueManager.`  

## 2.Directory structure  
```python
my_scrapy                               # The root directory 
    |
    ├── scrapy_mix                      # The scrapy_mix packet
    │   ├── core                            # The core of the scrapy_mix packer
    │   │   ├── __init__.py
    │   │   ├── clawer.py
    │   │   └── managers.py
    │   └── parts                           # The parts need to inheritance and override
    │       ├── __init__.py
    │       ├── downloaders.py
    │       ├── engine.py
    │       ├── midware.py
    │       ├── nodes.py
    │       ├── pipe.py
    │       ├── stackers.py
    │       └── tree.py
    ├── settings                        # The settings for the this spider project that you need to configure
    |    ├── __init__.py
    |    ├── aiohttp_settings.py
    |    ├── clawer_settings.py
    |    └── selenium_seletings.py
    ├── wparts                          # Need to inheritance and override parts should write here
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewires.py
    │   ├── pipeline.py
    │   └── trees.py
    └── run.py                          # Run this file to start the > > spider project
```

## 3.clawer .py
```python
import asyncio
from scrapy_mix.core.managers import PipeManager, MidWareManager, EngineManager, AsyncQueueManager, TreeManager, DownloaderManager, InterruptManager


class Clawer:
    """
    class Clawer

    Main responsible:
        1. open the spider
        2. call engine_manager to start spider
        3. interrupt record and interrupt recovery
        4. close the spider

    Main apartment:
        1. async_queue_manager
        2. pipe_manager
        3. midwire_manager
        4. engine_manager
        5. tree_manager
        6. downloader
        7. interrupt_manager
    """
    # init the clawer
    def __init__(self, ) -> None:
        self.async_queue_manager = AsyncQueueManager(clawer=self)
        self.downloader_manager = DownloaderManager(clawer=self)
        self.tree_manager = TreeManager(clawer=self)
        self.pipe_manager = PipeManager(clawer=self)
        self.midware_manager = MidWareManager(clawer=self)
        self.engine_manager = EngineManager(clawer=self)
        self.interrupt_manager = InterruptManager(clawer=self)

    # excute once when the open
    async def open_spider(self):
        """
        excute once time when the spider open
        """
        await self.downloader_manager.open_spider()
        self.pipe_manager.open_spider()
        self.midware_manager.open_spider()

    # excute once when the close
    async def close_spider(self):
        self.midware_manager.close_spider()
        self.pipe_manager.close_spider()
        await self.downloader_manager.close_spider()
        await asyncio.sleep(5)

    # the core of the frame, run this method to start the crawl
    def main(self):
        """
        application interface for the program to run
        """
        try:
            asyncio.run(self.core())
            self.interrupt_manager.non_interrupt_do()
        except BaseException as e:
            asyncio.run(self.interrupt_manager.interrupt_record())
            raise e


    async def core(self):
        """
        call engine_manager to start engines
        """
        await self.open_spider()
        cache = self.interrupt_manager.cache()
        if cache:
            await self.interrupt_manager.interrupt_recovery(cache=cache)
        else:
            self.tree_manager.start_nodes()

        while not self.async_queue_manager.queue.empty():
            await self.engine_manager.start_engines()
        await self.close_spider()
```  
## 4.managers. py
```python
# here too much code, see the source code if you interested

def create_obj_from_path_dt_2lt(paths_dt):...  

def create_obj_from_path_dt_2dt(paths_dt):...  

class PipeManager:...  

class MidWareManager:...  

class EngineManager:...  

class DownloaderManager:...  

class TreeManager:...  

class InterruptManager:...  

class AsyncQueueManager:... 
```  

## 5.aiohttp_settings .py  

```python
from aiohttp import ClientSession
from aiohttp import TCPConnector


# should return a session
async def create_session():
    return ClientSession(connector=TCPConnector(verify_ssl=False))
```

## 6.clawer_settings .py  

```python
# staker Type ['SStack', 'LStack', 'LifoQueue']
ENGINE_STACKER_TYPE = 'SStack'

# engine num
ENGINE_NUM = 10

# delay second
DELAY = 1

# pipelines
PIPES = {
    'wparts.pipeline.Pipeline': 200
}

# middlewires
MIDWARES = {
    'wparts.middlewires.Middleware': 200
}

# trees
TREES = {
    'wparts.trees.SpiderTree': 200
         }
# start downloader or not
AIOHTTPDOWNLOADER = True
SELENIUMDOWNLOADER = True
```

## 7.aiohttp_settings .py  

```python
# ****************************** SeleniumDwonloader Settings *********************************
from selenium import webdriver

# ************************************** 1.options *******************************************
options = webdriver.ChromeOptions()

# 设置无界面模式
# options.add_argument('--headless')

# 设置浏览器不关闭
# options.add_experimental_option('detach', True)

# 更改UserAgent
# options.add_argument('UserAgent=%s' % ua.random)

# 设置浏览器分辨率（窗口大小）
# options.add_argument("--window-size=1920,1080")

# 隐身模式（无痕模式）
options.add_argument('--incognito')

# 禁用扩展
options.add_argument("--disable-extensions")

# 禁用GPU加速
options.add_argument("--disable-gpu")

# 禁用 3D 软件光栅化器
options.add_argument("--disable-software-rasterizer")

# 禁用javascript
options.add_argument('--disable-javascript')  

# 解决DevToolsActivePort文件不存在的报错
options.add_argument('--no-sandbox')

# 设置Chrome忽略网站证书错误
options.add_argument('--ignore-certificate-errors')

# 默认情况下，https 页面不允许从 http 链接引用 javascript/css/plug-ins。添加这一参数会放行这些内容。
options.add_argument('--allow-running-insecure-content')

# 不加载图片, 提升速度
options.add_argument("blink-settings=imagesEnabled=false")

# 去掉webdriver日志
options.add_argument("disable-blink-features=AutomationControlled")

# 通过Log读取XHR 构造chrome driver：
options.add_argument("--allow-running-insecure-content")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-single-click-autofill")
options.add_argument("--disable-autofill-keyboard-accessory-view[8]")
options.add_argument("--disable-full-form-autofill-ios")
options.add_experimental_option('perfLoggingPrefs', {
    'enableNetwork': True,
    'enablePage': False,
})

# ************************************** 2.desired_capabilities *******************************************

desired_capabilities = webdriver.DesiredCapabilities.CHROME
desired_capabilities['goog:loggingPrefs'] = {
    'browser': 'ALL',
    'performance': 'ALL',
}
desired_capabilities['perfLoggingPrefs'] = {
    'enableNetwork': True,
    'enablePage': False,
    'enableTimeline': False
}
```