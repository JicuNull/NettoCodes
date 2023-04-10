import time
import requests
import json
import traceback
import helper.utils as utils
import api.response_decode as response_decode
from typing import Any
from api.http_request import *
from api.http_content import APPLICATION_JSON as JSON


class Client:

    def get_codes(self):
        body = self.__execute(ContentModulesRequest())
        if 'data' not in body:
            return []
        lst = [item.get('nettoapp_augmented_reality') for item in body['data'] if 'nettoapp_augmented_reality' in item]
        lst = [code['coupon']['completionObject'] for code in lst if 'coupon' in code and len(code['coupon']) > 0]
        return [(code['id'], code['couponDisplayObject']['title'], code['type'],
                 utils.time2unix(code['couponDisplayObject']['gueltigVon']),
                 utils.time2unix(code['couponDisplayObject']['gueltigBis'])) for code in lst]

    def activate_code(self, code: str, email: str):
        return self.__execute(CodeActivateRequest(code, email, round(time.time())))

    def __execute(self, request: Request) -> dict | str:
        url = str(request.url)
        body = request.content.body
        headers = self.__build_headers(request.content.body_type)
        clazz = request.__class__
        return self.__query(url, body, headers, clazz)

    @staticmethod
    def __query(url: str, data: dict, headers: dict, clazz: Any) -> dict | str:
        try:
            is_json = JSON in headers['content-type']
            response = requests.post(url, headers=headers, data=json.dumps(data) if is_json else data)
            is_json = 'content-type' not in response.headers or JSON in response.headers.get('content-type', '')
            return response_decode.load(response.text, clazz) if is_json else response.text
        except requests.exceptions.RequestException:
            traceback.print_exc()
        return response_decode.fallback_response()

    @staticmethod
    def __build_headers(body_type: str) -> dict:
        return {'user-agent': 'okhttp/4.9.1',
                'x-netto-api-key': '9b4ced25-638c-4a15-a327-46ce18b2c0c2',
                'content-type': body_type}
