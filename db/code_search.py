import threading
import time
import api.netto_client as netto
import db.db_manager as db


class CodeSearch(threading.Thread):

    run_flag = True

    def __init__(self):
        super().__init__()
        self.__client = netto.Client()

    def run(self) -> None:
        while self.run_flag:
            codes = self.__client.get_codes()
            db.save_codes(codes)
            print(f'Found {len(codes)} ar-codes')
            time.sleep(21600)

    def stop(self):
        self.run_flag = False
