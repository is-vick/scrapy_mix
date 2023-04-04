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
        await asyncio.sleep(5)

