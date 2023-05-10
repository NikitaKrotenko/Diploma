from src.config.config import Config

class Current_Futures_Data:
    def __init__(
            self,
            symbol='',
            markPrice='0',
            indexPrice='0', 
            estimatedSettlePrice='0', 
            lastFundingRate='0', 
            interestRate='0', 
            nextFundingTime='0', 
            time='0') -> None:
        self.symbol = symbol
        self.mark_price = float(markPrice)
        self.index_price = float(indexPrice)
        self.estimated_settle_price = float(estimatedSettlePrice)
        self._lastFundingRate = float(lastFundingRate)
        self._interestRate = float(interestRate)
        self._nextFundingTime = float(nextFundingTime)
        self._time = float(time)

        self.prepare_time_data()
        self.prepare_rate_data()

    def prepare_time_data(self):
        def conver_time(binance_timestamp):
            return int(float(binance_timestamp)/1000)
    
        self.timestamp = conver_time(self._time)
        self.time_left_secons = conver_time(self._nextFundingTime - self._time)

    def prepare_rate_data(self):
        def convert_rates(row_rates):
            return float(row_rates*100)

        self.funding = convert_rates(self._lastFundingRate)
        self.interest = convert_rates(self._interestRate)

    # @staticmethod
    def get_data(self):
        return [self.timestamp, 
            self.symbol, 
            self.mark_price, 
            self.index_price, 
            self.estimated_settle_price, 
            self.interest, 
            self.funding, 
            self.time_left_secons]

    # @staticmethod
    def get_column_names(self):
        return ['timestamp',
            'symbol',
            'mark_price', 
            'index_price', 
            'estimated_settle_price', 
            'interest', 
            'funding', 
            'time_left_secons']
    
    def get_column_types(self):
        return ['INT',
            'CHAR(10)',
            'FLOAT', 
            'FLOAT', 
            'FLOAT', 
            'FLOAT(8)', 
            'FLOAT(8)', 
            'INT']
    
    def get_dict_data(self):
        return dict(zip(self.get_column_names(), self.get_data()))
    


class Current_Futures_Reader:
    def __init__(self, config) -> None:
        self.config = config

    def get_data(self):
        return Current_Futures_Data(**self.config.binance_client.futures_mark_price(symbol=self.config.symbol))
