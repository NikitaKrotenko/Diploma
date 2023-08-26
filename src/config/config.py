
from binance import Client

class Singleton(type):
    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance

class Config():

    def __init__(self) -> None:
        self.bd_server = ('5.135.159.182')
        self.ssh_username = 'ubuntu'
        self.ssh_password = '3nSUltfK4BfYj5um'
        self.ssh_proxy_enabled = True
        self.remote_bind_address = ('localhost', 3306)

        self.bd_host = '127.0.0.1'
        self.bd_user = 'viewer1'
        self.bd_passwd = '11!!AAbbb'

        self.symbol = 'BTCUSDT'

        self.db_name = 'exchange data'

        self.binance_client = Client()

        self.files_location = "C:/Users/krotenko.n/Documents/BinanceData"
        self.tg_daiy_token = "5765462506:AAE6iQMywWE61FedKIrPTj2QMDTVBRstJKI"
        self.tg_chat_id = "494465491"