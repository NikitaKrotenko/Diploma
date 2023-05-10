from src.config.config import Config

class Current_Trade_Data:
    def __init__(
            self,
            symbol='',
            open='0',
            close='0', 
            low='0', 
            high='0', 
            volume='0', 
            trades='0', 
            time='0') -> None:
        self.symbol = symbol
        self.open = float(open)
        self.close = float(close)
        self.low = float(low)
        self.high = float(high)
        self.volume = float(volume)
        self.trades = float(trades)
        self._time = float(time)

        self.prepare_time_data()
        self.prepare_rate_data()

    def prepare_time_data(self):
        def conver_time(binance_timestamp):
            return int(float(binance_timestamp)/1000)
    
        self.timestamp = conver_time(self._time)
        self.time_left_secons = conver_time(self._nextFundingTime - self._time)

    # @staticmethod
    def get_data(self):
        return [self.timestamp, 
            self.symbol, 
            self.open, 
            self.close, 
            self.low, 
            self.high, 
            self.volume, 
            self.trades]

    # @staticmethod
    def get_column_names(self):
        return ['timestamp',
            'symbol',
            'open', 
            'close', 
            'low', 
            'high', 
            'volume', 
            'trades']
    
    def get_column_types(self):
        return ['INT',
            'CHAR(10)',
            'FLOAT', 
            'FLOAT', 
            'FLOAT', 
            'FLOAT', 
            'FLOAT', 
            'FLOAT']
    
    def get_dict_data(self):
        return dict(zip(self.get_column_names(), self.get_data()))
    


class Current_Trade_Reader:
    def __init__(self, config) -> None:
        self.config = Config()

    def get_data(self):
        row = self.config.binance_client.futures_klines(symbol=self.config.symbol, interval='1m')[-1]
        return Current_Trade_Data(symbol=self.config.symbol,
            open=row[1],
            close=row[2], 
            low=row[3], 
            high=row[4], 
            volume=row[5], 
            trades=row[-3], 
            time=row[0])
