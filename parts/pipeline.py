from scrapy_mix.core.parts.pipe import Pipe
import asyncio
import random
import time
# import aiomysql

class Pipeline(Pipe):
    def open_spider(self):
        self.num = 0
        print('open Pipeline')

    async def process_itemnode(self, itemnode):
        print(itemnode.get_item())
        self.num += 1
        print(self.num)
        # time.sleep(0.2)
        # await asyncio.sleep(random.random())
        
        return itemnode
    
    def close_spider(self):
        print(self.num)
        print('close Pipeline')