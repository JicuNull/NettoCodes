class Url:

    def __init__(self, url: str, params: dict = None):
        self.__url = url
        self.__params = params

    def format(self):
        return str(self)

    def __str__(self):
        return self.__build_url(self.__url, self.__params) if self.__params is not None else self.__url

    def __repr__(self):
        return f'Url("{self.__url}", "{self.__params}")'

    @staticmethod
    def __build_url(url: str, params: dict):
        return url + '?' + '&'.join([item[0] + '=' + item[1] for item in params])
