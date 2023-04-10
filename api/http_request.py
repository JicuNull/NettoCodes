from abc import ABC, abstractmethod
from datetime import datetime
from api.http_content import HttpContent, UrlContent, JsonContent
from api.url import Url


class Request(ABC):

    def __init__(self, content: HttpContent):
        self.__content = content

    @property
    def content(self) -> HttpContent:
        return self.__content

    @property
    @abstractmethod
    def url(self) -> Url:
        pass


class ContentModulesRequest(Request):

    def __init__(self):
        content = {'api_token': 'e6Ddd8gYybhZVTen', 'api_user': 'nettoapp', 'store_id': '9999', 'id': 'MR-15801'}
        super().__init__(UrlContent(content))

    @property
    def url(self) -> Url:
        return Url('https://www.netto-online.de/api/modular/get_content_modules')


class CodeActivateRequest(Request):

    def __init__(self, code: str, email: str, unix_time: int):
        date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S')
        content = {'email': email, 'kampagneCode': code, 'teilnahmedatum': date}
        super().__init__(JsonContent(content))

    @property
    def url(self) -> Url:
        return Url('https://www.clickforbrand.de/ncp.kampagnen/v1/kampagnenteilnahmen')
