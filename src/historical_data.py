import pandas as pd
from src.db_writer.db import DB
from src.quarter_functions import get_delivery, get_quarter_symbol

class Historical_Data_Backup:
    def __init__(self, config) -> None:
        self.config = config

    def get_first_timestamp(self):
        query = f'''select MIN(timestamp) 
            from {self.config.db_name}.{self.config.table_name}
            where symbol = '{self.config.symbol}'
            '''
        per = pd.read_sql(query, con=DB(self.config).con)
        return per['MIN(timestamp)'].iloc[0]
    
    def get_min_quarter_timestamp(self):
        query = f'''SELECT min(timestamp)
            FROM {self.config.db_name}.{self.config.table_name}
            WHERE symbol != '{self.config.symbol}'
            '''
        return pd.read_sql(query, con=DB(self.config).con).iloc[0,0]
    
    def preprocess_data(self, data, symbol):
        data_preprocessed = pd.DataFrame([[row[i] for i in [0,1,4,3,2,5,8]] for row in data], 
                    columns=['timestamp', 'open', 'close', 'low', 'high', 'volume', 'trades'])
        data_preprocessed['timestamp']/=1000
        data_preprocessed.insert(column='symbol', loc=1, value=symbol)
        return data_preprocessed
    
    def load_raw_data_alltogether(self):
        # left it just in case
        # iterate in reverse direction from minimal available timestamp
        endTime = (self.get_first_timestamp()-30) * 1000

        all_time_data = []
        while True:
            data_1500 = self.config.binance_client.futures_klines(
                    symbol = self.config.symbol, 
                    interval = '1m', 
                    limit = 1500, 
                    endTime = endTime)
            all_time_data += data_1500
            endTime -= 90000000
            # mean we reached bottom of available data
            if (len(data_1500) != 1500):
                return all_time_data
            

    def push_to_database(self, data):
        data.to_sql(
                        self.config.table_name, schema=self.config.db_name,
                        con=DB(self.config).engine, if_exists = 'append', index=False)
        print(f"{data.shape} records pushed successfully")
        

    def load_historical_perentrentual_data_batches(self, num_batches=1):
        while True:
            endTime = (self.get_first_timestamp()-30) * 1000
            all_time_data = []
            for i in range(num_batches):
                data_1500 = self.config.binance_client.futures_klines(
                            symbol = self.config.symbol, 
                            interval = '1m', 
                            limit = 1500, 
                            endTime = endTime)
                
                all_time_data += data_1500
                endTime -= 90000000

                if(len(data_1500) < 1500):
                    print(endTime, data_1500[-1][0])
                    self.push_to_database(self.preprocess_data(all_time_data, 'BTCUSDT'))
                    return     
                   
            self.push_to_database(self.preprocess_data(all_time_data, 'BTCUSDT'))

    
    def load_historical_quarterly_data_batches(self, num_batches=120):
        endTime = (self.get_min_quarter_timestamp()-30) * 1000
        symbol = get_quarter_symbol(self.config.symbol,endTime/1000)
        finished_trigger = False
        while True:
            print(endTime, pd.to_datetime(endTime/1000, unit='s'))
            quarter_data = []
            for i in range(num_batches):
                data_1500 = self.config.binance_client.futures_klines(
                                symbol = symbol, 
                                interval = '1m', 
                                limit = 1500, 
                                endTime = endTime)
                # print(data_1500[-1][0], end=' ')
                quarter_data += data_1500
                endTime -= 90000000
                
                if(len(data_1500) < 1500):
                    finished_trigger = True
                    break

            if(finished_trigger == True):
                self.push_to_database(self.preprocess_data(quarter_data, symbol))
                print(f"quarter {symbol} loading finished successfully")
                print(len(quarter_data))
                if(len(quarter_data) < 115000):
                    return
                symbol = get_quarter_symbol(self.config.symbol,endTime//1000)
                endTime = get_delivery(endTime//1000)*1000
                # print(f"{symbol} quarter endTime is {endTime}")
                finished_trigger = False
                print(f"quarter {symbol} loading")
            else:
                print(symbol, end=' ')        
                self.push_to_database(self.preprocess_data(quarter_data, symbol))
        