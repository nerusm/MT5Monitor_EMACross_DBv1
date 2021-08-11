import logging


from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.trades_orm import RetCode, Trade, ReTrade
import sqlalchemy
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config
from sqlalchemy import create_engine


class TardesCrud:

    def get_connection(self, schema_name, from_func):
        uname = config['uname']
        password = config['password']
        host = config['host']
        port = config['port']
        logging.debug(f"Initialising DB connection for {from_func}, schema: {schema_name}")
        self.engine = create_engine(
            f"mariadb+mariadbconnector://{uname}:{password}@{host}:{port}/" + schema_name)
        self.conn = self.engine.connect()
        return self.conn

    def create_session(self, schema_name, from_func):
        logging.debug(f"Creating Session for {from_func}")
        # Create a session
        self.get_connection(schema_name=schema_name, from_func=self.__module__)
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def close_session(self):
        logging.debug(f"Closing Session")
        self.session.close()

    def close_connection(self, from_func):
        logging.debug(f"Closing Connection for {from_func}")
        self.conn.close()


    # def __del__(self):
    #     self.session.close()
    #     logging.debug(f"Destructor called in TradesCrud")


    def addNewRetrade(self, posid_dict):
        reTrade = ReTrade(position_id=posid_dict.get("position_id"),
                          symbol=posid_dict.get('symbol'),
                          strat_id= posid_dict.get('strat_id'),
                          order_type=posid_dict.get('order_type'),
                          close_time=posid_dict.get('close_time'))
        self.session.add(reTrade)
        self.session.commit()
        logging.debug(f"New Retrade added: Position ID: {reTrade.position_id}, "
                      f"symbol: {reTrade.symbol}")

    def addNewTrade(self, position_id, symbol, order_type,
                    price, magic, comment, request_id, is_open,
                    volume, reason, parent_position_id, strat_id=0, strat_ref_id=1, ):
        newTrade = Trade(position_id=position_id, symbol=symbol, order_type=order_type,
                         price=price, magic=magic, comment=comment, request_id=request_id,
                         is_open=is_open, strat_id=strat_id, strat_ref_id=strat_ref_id,
                         volume=volume, reason=reason, parent_position_id=parent_position_id)

        logging.debug(f"New Trade: {newTrade}")
        self.session.add(newTrade)
        self.session.commit()
        logging.debug(f"New Trade Added, position: {position_id}")

    def select_all_retrades(self):
        retrade_list = self.session.query(ReTrade).all()
        return retrade_list

    def select_all_retrades_by_status_strat_id(self, strat_id):
        retrade_list = self.session.query(ReTrade).filter_by(is_retraded=False, strat_id=strat_id).all()
        return retrade_list

    def update_retrade_status(self, position_ids):
        for pid in position_ids:
            retrade= self.session.query(ReTrade).filter_by(position_id = pid).first()
            retrade.is_retraded = True
            self.session.commit()

    def selectBySymbolSignalOpenStatus(self, symbol, signal, isOpen):
        trade = self.session.query(Trade).filter_by(symbol=symbol, order_type=signal,
                                                    is_open=isOpen).all()
        self.session.commit()
        return trade

    def selectBySymbolSignalOpenStatusStratId(self, symbol, signal, isOpen, strat_id):
        trade = self.session.query(Trade).filter_by(symbol=symbol, order_type=signal,
                                                    is_open=isOpen, strat_id=strat_id).all()
        self.session.commit()
        return trade

    def selectByPositionId(self, position_id):
        trade = self.session.query(Trade).filter_by(position_id=position_id).first()
        self.session.commit()
        return trade

    def updateStatusByPositionId(self, position_id, profit, reason, volume,
                                 open_time, close_time, close_price):
        trade = self.session.query(Trade).filter_by(position_id=position_id).first()
        if trade is None:
            logging.error(f"Trade is None: {position_id}")
        logging.debug(f"Trade Sel: {trade}")
        trade.is_open = False
        trade.profit = profit
        trade.reason = reason
        trade.volume = volume
        trade.open_time = open_time
        trade.close_time = close_time
        trade.close_price = close_price
        self.session.commit()
        logging.debug(f"Trade status updated: {trade.position_id}")
        return None

    def addNewRetCode(self, ret_code, ret_msg, symbol, signal):
        new_ret = RetCode(ret_code, ret_msg, symbol, signal)
        self.session.add(new_ret)
        self.session.commit()

    def selectAllOpenTrades(self):
        open_trades = self.session.query(Trade).filter_by(is_open=True).all()
        self.session.commit
        return open_trades

    def roll_back(self):
        logging.debug("Rolling Back..")
        self.session.rollback()

        # logging.debug(f"Return Code added: {ret_code}")
# str = "EMACross 30M,Symbol:  EURCAD,Time:       2021-07-15 18:30:00 IST,Signal:     BUY ,Strength:   STRONG,ClosePriceAbove 20EMA:  True ,RSIAbove 50:  True ,SAR Below:  True ,Possible Stop Loss:  1.47888"
# tr = TardesCrud()
#
# res = tr.selectBySymbolOpenStatus(symbol="GBPUS",isOpen= True)
# logging.debug(f"Res: {res}")
# res = tr.selectByPositionId(position_id=12345)
# res = tr.addNewTrade(position_id=12346, symbol='EURCAD', order_type='BUY',
#                      price=0.93305, magic=123456, comment=str, request_id=1, is_open=True,
#                      strat_id=1, strat_ref_id=123)
#
# res = tr.addNewTrade(position_id=12347, symbol='USDJPY', order_type='SELL',
#                      price=1.563, magic=123456, comment='pyhton comment', request_id=1,
#                      is_open=True,
#                      strat_id=1, strat_ref_id=124)
