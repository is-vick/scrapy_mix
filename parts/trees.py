from scrapy_mix.core.parts.tree import Tree
from scrapy_mix.core.parts.nodes import AioHttpRequest, SeleniumRequest
from parts.items import SpiderItem

# class SpiderTree(Tree):
#     def start_nodes(self):
#         for offset in range(1):
#             # url = 'http://httpbin.org/get'
#             url = f'https://www.baidu.com{offset}'
#             yield AioHttpRequest(url=url, method='get', callback="trees.SpiderTree.parse", meta={'pg1': url})

#     def parse(self, response):
#         pg1 = response.meta['pg1']
#         for i in range(10):
#             url = f'https://www.taobao.com{i}'
#             yield AioHttpRequest(url=url, method='get', callback="trees.SpiderTree.parse1", meta={'pg1': pg1, 'pg2': url, 'async': True})
          
#     def parse1(self, response):
#         pg1 = response.meta['pg1']
#         pg2 = response.meta['pg2']
#         for i in range(10):
#             url = f'https://www.maoyan.com{i}'
#             yield AioHttpRequest(url=url, method='get', callback="trees.SpiderTree.parse2", meta={'pg1': pg1, 'pg2': pg2, 'pg3': url})
          
#     def parse2(self, response):
#         pg1 = response.meta['pg1']
#         pg2 = response.meta['pg2']
#         pg3 = response.meta['pg3']
#         for i in range(1):
#             url = f'https://www.jd.com{i}'
#             yield AioHttpRequest(url=url, method='get',callback="trees.SpiderTree.parse3", meta={'pg1': pg1, 'pg2': pg2, 'pg3': pg3, 'pg4': url})

#     def parse3(self, response):
#         pg1 = response.meta['pg1']
#         pg2 = response.meta['pg2']
#         pg3 = response.meta['pg3']
#         pg4 = response.meta['pg4']

#         for i in range(1):
#             url = f'https://www.taobao.com/seleniumRequest'
#             yield SeleniumRequest(url=url, method='get', callback="trees.SpiderTree.parse4", action='trees.SpiderTree.action1', meta={'pg1': pg1, 'pg2': pg2, 'pg3': pg3, 'pg4': pg4, 'pg5': url})

#     def parse4(self, response):
#         meta = response.meta
#         item = SpiderItem()
#         item.url1 = meta['pg1']
#         item.url2 = meta['pg2']
#         item.url3 = meta['pg3']
#         item.url4 = meta['pg4']
#         item.url5 = meta['pg5']
#         for i in range(10):
#             yield item
#         # yield item

#     def action1(self, driver):
#         # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ action here', driver)
#         pass


    


from lxml import etree
from parts.items import MaoYanItem

class SpiderTree(Tree):
    num = 0
    def start_nodes(self):
        for offset in range(0, 91, 10):
            # url = 'http://httpbin.org/get'
            url = "https://www.maoyan.com/board/4?offset={}".format(offset)
            # url = 'https://www.maoyan.com/board/4?offset=10'
            # yield SeleniumRequest(url=url, method='get', callback="trees.SpiderTree.parse")
            yield AioHttpRequest(url=url, method='get', callback="parts.trees.SpiderTree.parse")
            break
            
    def parse(self, response):
        print(response.status, response.url)
        print(response.headers)
        response = etree.HTML(response.content.decode())
        films = response.xpath("//dl/dd")
        try:
            next_page = response.xpath('//a[contains(text(), "下一页")]/@href')[0].strip()
            next_page_url = 'https://www.maoyan.com/board/4?' + next_page
        except Exception as e:
            pass
        
        for film in films:
            item = MaoYanItem()
            rank = film.xpath('./i/text()')[0].strip()
            detail_url = film.xpath('.//div[@class="movie-item-info"]/p[1]/a/@href')[0].strip()
            detail_url = 'https://www.maoyan.com' + detail_url
            film_name = film.xpath('.//div[@class="movie-item-info"]/p[1]/a/@title')[0].strip()
            main_actor = film.xpath('.//div[@class="movie-item-info"]/p[2]/text()')[0].strip()
            show_time = film.xpath('.//div[@class="movie-item-info"]/p[3]/text()')[0].strip()
            item.rank = rank 
            item.film_name = film_name
            item.main_actor = main_actor
            item.show_time = show_time
            yield item
 
          