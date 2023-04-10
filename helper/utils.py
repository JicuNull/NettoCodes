from datetime import datetime
import hashlib


def email2hash(email: str) -> str:
    if email is None:
        email = ''
    result = hashlib.md5(email.encode())
    return result.hexdigest()


def time2unix(time_formatted: str) -> int:
    return round(datetime.fromisoformat(time_formatted).timestamp())