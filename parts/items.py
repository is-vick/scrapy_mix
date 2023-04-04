from scrapy_mix.core.parts.nodes import Item


class SpiderItem(Item):
    """
    use __slots__ = ('xxx', 'xxx', ..., 'xxx') to define you field for spider

    for example:
    
    __slots__ = ('name', 'age')

    """
    __slots__ = ('url1', 'url2', 'url3', 'url4', 'url5', 'url6', 'url7')



class MaoYanItem(Item):
    __slots__ = ('rank', 'film_name', 'main_actor', 'show_time', 'img_set', 'comment', 'file_path', 'comments')