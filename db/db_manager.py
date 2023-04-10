import sqlite3
import textwrap
import helper.utils as utils
from helper.constants import *
from typing import Any
from datetime import datetime


def save_history(email: str, code: str, message: str):
    if message == CODE_SUCCESS or message == CODE_ALREADY_USED:
        md5 = utils.email2hash(email)
        conn = __get_db_connection()
        conn.execute('insert or ignore into history (email, code) values (?, ?)', (md5, code))
        conn.commit()
        conn.close()


def save_codes(codes: list[tuple]):
    conn = __get_db_connection()
    [conn.execute('insert or ignore into codes values (?, ?, ?, ?, ?)', code) for code in codes]
    conn.commit()
    conn.close()


def is_activated(email: str, code: str) -> bool:
    md5 = utils.email2hash(email)
    conn = __get_db_connection()
    count = conn.execute('select count(*) count from history where email = ? and code = ?', (md5, code)).fetchone()
    conn.close()
    return count['count'] > 0


def exists_code(code: str) -> bool:
    return __code_by_id(code) is not None


def __code_by_id(code: str) -> Any | None:
    conn = __get_db_connection()
    result = conn.execute('select * from codes where id = ?', (code,)).fetchone()
    conn.close()
    return result


def get_codes(code_type: str = None):
    __cleanup_codes()
    conn = __get_db_connection()
    codes = conn.execute('select * from codes').fetchall() if code_type is None \
        else conn.execute('select * from codes where code_type = ?', (code_type,)).fetchall()
    conn.close()
    codes = [{column: (textwrap.shorten(code[column], width=40, placeholder='...')
                       if isinstance(code[column], str) else
                       datetime.utcfromtimestamp(code[column]).strftime('%d.%m.'))
              for column in code.keys()} for code in codes]
    return codes


def __cleanup_codes():
    conn = __get_db_connection()
    conn.execute('delete from codes where valid_to < (SELECT strftime(\'%s\', \'now\'))')
    conn.commit()
    conn.close()


def init():
    conn = sqlite3.connect('database.db')
    with open('schema.sql') as schema:
        conn.executescript(schema.read())
    conn.commit()
    conn.close()


def __get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
