import pandas as pd

from src.db_writer.db import DB
from src.readers.trade_reader import Current_Trade_Data, Current_Trade_Reader


class Derevative_Data:
    def __init__(self, config) -> None:
        self.config = config

    def get_data_structure(self):
        self.data_structure = Current_Trade_Data()

    def get_cols_types(self):
        self.cols_types = ''.join([f'{col} {typ}, '
                                   for col, typ in zip(self.data_structure.get_column_names(),
                                                        self.data_structure.get_column_types())])[:-2]
        return self.cols_types

    def get_fresh_data(self):
        self.data = Current_Trade_Reader(self.config).get_data()
        return self.data
    
    def init_tables(self):
        DB_QUERY = f'''CREATE DATABASE IF NOT EXISTS {self.config.db_name};'''
        TABLE_QUERY = f'''CREATE TABLE IF NOT EXISTS {self.config.db_name}.{self.config.table_name}
          ({self.cols_types});'''
        cur = DB(self.config).con.cursor()
        cur.execute(DB_QUERY)
        print(cur.fetchall())
        cur.execute(TABLE_QUERY)
        print(cur.fetchall())

    def get_last_timestemp(self):
        query = f'''select MAX(timestamp) from {self.config.db_name}.{self.config.table_name}
            where symbol = '{self.config.symbol}'
            '''
        per = pd.read_sql(query, con=DB(self.config).con)
        return per['MAX(timestamp)'].iloc[0]

    
    def run(self):
        self.get_data_structure()
        self.get_cols_types()
        self.get_fresh_data()
        if self.config.mode == 'work' and not self.config.first_run:
            self.init_tables()
        elif self.config.mode == 'work':
            last = self.get_last_timestemp()
            if last is None or last < self.data.timestamp:
                pd.DataFrame(self.data.get_dict_data(), index=[0]).to_sql(
                    self.config.table_name, schema=self.config.db_name,
                    con=DB(self.config).engine, if_exists = 'append', index=False)
