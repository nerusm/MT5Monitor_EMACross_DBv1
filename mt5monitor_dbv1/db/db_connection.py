import sqlalchemy, logging
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config
from sqlalchemy import create_engine


class DB_Connection:
    conn = None

    # def __del__(self):
    #     logging.debug(f"Destructor called in DB_Connection")
    #     # if self.session:
    #     #     self.session.close()
    #     if self.conn is not None:
    #         self.conn.close()

    def get_connection(self,schema_name, from_func):
        uname = config['uname']
        password = config['password']
        host = config['host']
        port = config['port']
        logging.debug(f"Initialising DB connection for {from_func}, schema: {schema_name}")
        engine = create_engine(
            f"mariadb+mariadbconnector://{uname}:{password}@{host}:{port}/" + schema_name)
        self.conn = engine.connect()
        return self.conn

    def close_connection(self, from_func):
        if self.conn is not None:
            logging.debug(f"Closing Connection for {from_func}")
            self.conn.invalidate()
        else:
            logging.debug(f"self.Conn is None")
