class AioHttpRequest:
    def __init__(self, url, callback, params=None, method='get', data=None, json={}, headers=None, proxy=None, meta={}, allow_redirects=True, request_type='AioHttpRequest') -> None:
        self.url = url
        self.callback = callback
        self.params = params
        self.method = method
        self.data = data
        self.json = json
        self.headers = headers
        self.proxy = proxy
        self.meta = meta
        self.allow_redirects = allow_redirects
        self.request_type = request_type

    def load2dict(self):
        return self.__dict__

class Response:
    def __init__(self, url, status, content=b'', meta={}, headers={}) -> None:
        self.url = url
        self.status = status
        self.content = content
        self.meta = meta
        self.headers = headers

    def load2dict(self):
        return {'url': self.url, 'status': self.status, 'content': self.content.decode(), 'meta': self.meta, 'headers': self.headers}


class Item:
    __slots__ = tuple()

    def __init__(self) -> None:
        self.__add_fields()

    def __add_fields(self):
        for k in self.__slots__:
            setattr(self, k, '')

    def get_item(self):
        return {k: self.__getattribute__(k) for k in self.__slots__}


class SeleniumRequest:
    def __init__(self, url, method='get', callback='', action='', headers={}, meta={}, request_type='SeleniumRequest') -> None:
        self.url = url
        self.method = method
        self.callback = callback
        self.action = action
        self.headers = headers
        self.meta = meta
        self.request_type = request_type
    
    def load2dict(self):
        return self.__dict__


class SeleniumResponse(Response):
    pass
