import json
from api.http_request import *
from helper.constants import *
from typing import Any


def load(txt: str, clazz: Any):
    if len(txt) == 0:
        txt = '{}'
    body = json.loads(txt)
    if clazz == CodeActivateRequest:
        code = body['FehlerCode'] if 'FehlerCode' in body else 0
        return {'message': __error_message(code)}
    return body


def fallback_response():
    return {'message': UNKNOWN_ERROR}


def __error_message(code: int):
    if code == 0:
        return CODE_SUCCESS
    elif code == 1:
        return CODE_NOT_FOUND
    elif code == 4:
        return CODE_ALREADY_USED
    elif code == 5:
        return INVALID_REQUEST
    else:
        return UNKNOWN_ERROR
