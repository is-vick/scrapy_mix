from scrapy_mix.parts.midware import Midware
from fake_useragent import UserAgent
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
'Host': 'www.maoyan.com',
'Cache-Control': 'no-cache',
'Connection': 'keep-alive',
':authority': 'p0.meituan.net',
':method': 'GET',
'Cookie': '__mta=108977981.1680525330335.1680586521713.1680588847216.13; uuid_n_v=v1; uuid=931FACF0D21B11EDB5DB33031B0079F38CD8EB1548334975999B22F1616FEBB2; _lxsdk_cuid=187471c4056c8-0f9cd964d6cbae-7a545474-144000-187471c4057c8; _lxsdk=931FACF0D21B11EDB5DB33031B0079F38CD8EB1548334975999B22F1616FEBB2; _csrf=f48aa7961ad4d1fc8af88196d35dc78fbc896ef5fe15742062b4bfd2331512ee; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1680527435,1680580211,1680585746,1680588519; _lx_utm=utm_source=bing&utm_medium=organic; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1680605626; __mta=108977981.1680525330335.1680588847216.1680605627609.14; _lxsdk_s=1874be6b518-517-a9-7d5||3'
}
class Middleware(Midware):
    def open_spider(self):
        print('open Midware')
        pass

    def process_request(self, request):
        ua = UserAgent()
        print('process request')
        headers['User-Agent'] = ua.random
        headers['Referer'] = 'https://www.maoyan.com/board/4'
        request.headers = headers
        return None
    
    def process_response(self, response):
        # print('process response')
        return None
    
    def close_spider(self):
        print('close Midware')
        pass
    