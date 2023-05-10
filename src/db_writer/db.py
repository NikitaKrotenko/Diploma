from src.config.config import Singleton, Config
from src.config.logger import Logger

from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
import pymysql


class DB:
    def __init__(self, config) -> None:
        self.config = config
        self.tunnel = self.__create_tunnell()
        # ???? do we need to start ?
        self.tunnel.start()
        self.con = self.__create_connection()
        self.engine = self.__get_engine()

    def update_con(self):
        self.con = self.__create_connection()

    def __get_engine(self):
        return create_engine("mysql+pymysql://{user}:{passwd}@{host}:{port}/{db_name}".format(
        user = self.config.bd_user, 
        passwd = self.config.bd_passwd, 
        host = self.config.bd_host, 
        db_name = self.config.db_name,
        port = self.tunnel.local_bind_port), connect_args={'connect_timeout': 120})

    # def __del__(self):
    #     self.con.commit()
    #     self.tunnel.close()

    def close_all(self):
        self.tunnel.close()
        self.con.close()
        self.engine.dispose()

    def __create_connection(self):
        connection = pymysql.connect(
        host=self.config.bd_host ,
        user=self.config.bd_user ,
        passwd=self.config.bd_passwd ,
        #todo
        port = self.tunnel.local_bind_port 
        )
        return connection

    def __create_tunnell(self):
        try:
            tunnel = SSHTunnelForwarder(self.config.bd_server,
            ssh_username = self.config.ssh_username,
            ssh_password = self.config.ssh_password,
            ssh_proxy_enabled = self.config.ssh_proxy_enabled,
            remote_bind_address = self.config.remote_bind_address)
        except BaseException as e:
            Logger().add_warning('Tunnel problems', str(e))
        return tunnel
