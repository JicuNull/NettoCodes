from abc import ABC

APPLICATION_JSON = 'application/json'
URL_ENCODED = 'application/x-www-form-urlencoded'


class HttpContent(ABC):

    def __init__(self, body: dict, content_type: str):
        self.__body = body
        self.__body_type = content_type

    @property
    def body(self):
        return self.__body

    @property
    def body_type(self):
        return self.__body_type


class UrlContent(HttpContent):

    def __init__(self, body: dict):
        super().__init__(body, URL_ENCODED)


class JsonContent(HttpContent):

    def __init__(self, body: dict):
        super().__init__(body, APPLICATION_JSON)
