from datetime import datetime
from zoneinfo import ZoneInfo

import sqlalchemy
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.utilities.utils import convert_to_athens
from sqlalchemy.ext.declarative import declarative_base


class Trade(declarative_base()):
    __tablename__ = 'trade_book'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    position_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    symbol = sqlalchemy.Column(sqlalchemy.String(length=6), primary_key=True)
    order_type = sqlalchemy.Column(sqlalchemy.String(length=4))
    price = sqlalchemy.Column(sqlalchemy.DECIMAL)
    close_price = sqlalchemy.Column(sqlalchemy.DECIMAL)
    magic = sqlalchemy.Column(sqlalchemy.Integer)
    comment = sqlalchemy.Column(sqlalchemy.String(length=500))
    request_id = sqlalchemy.Column(sqlalchemy.Integer)
    is_open = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    strat_id = sqlalchemy.Column(sqlalchemy.Integer)
    strat_ref_id = sqlalchemy.Column(sqlalchemy.Integer)
    reason = sqlalchemy.Column(sqlalchemy.String(length=10))
    profit = sqlalchemy.Column(sqlalchemy.DECIMAL)
    volume = sqlalchemy.Column(sqlalchemy.DECIMAL)
    open_time = sqlalchemy.Column(sqlalchemy.DATETIME)
    close_time = sqlalchemy.Column(sqlalchemy.DATETIME)
    parent_position_id = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, position_id, symbol, order_type,
                 price, magic, comment, request_id, is_open,
                 strat_id, strat_ref_id, reason, parent_position_id, volume=0.01,
                 open_time=convert_to_athens(
                     datetime.now(tz=ZoneInfo(config['mt5_trader_timezone'])))):
        self.position_id = position_id
        self.symbol = symbol
        self.order_type = order_type
        self.price = price
        self.magic = magic
        self.comment = comment
        self.request_id = request_id
        self.is_open = is_open
        self.strat_id = strat_id
        self.strat_ref_id = strat_ref_id
        self.volume = volume
        self.reason = reason
        self.open_time = open_time
        self.parent_position_id = parent_position_id
        # print("init trade")


class ReTrade(declarative_base()):
    __tablename__ = 'retrade_book'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    position_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    symbol = sqlalchemy.Column(sqlalchemy.String(length=6), primary_key=True)
    order_type = sqlalchemy.Column(sqlalchemy.String(length=4))
    close_time = sqlalchemy.Column(sqlalchemy.DATETIME)
    is_retraded = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    strat_id = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, position_id, symbol, order_type, strat_id,
                 close_time=convert_to_athens(
                     datetime.now(tz=ZoneInfo(config['mt5_trader_timezone'])))):
        self.position_id = position_id
        self.symbol = symbol
        self.order_type = order_type
        self.close_time = close_time
        self.is_retraded = False
        self.strat_id = strat_id

class RetCode(declarative_base()):
    __tablename__ = 'ret_codes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    ret_code = sqlalchemy.Column(sqlalchemy.Integer)
    ret_msg = sqlalchemy.Column(sqlalchemy.String(length=200), primary_key=True)
    symbol = sqlalchemy.Column(sqlalchemy.String(length=6), primary_key=True)
    signal = sqlalchemy.Column(sqlalchemy.String(length=6), primary_key=True)

    def __init__(self, ret_code, ret_msg, symbol, signal):
        self.ret_code = ret_code
        self.ret_msg = ret_msg
        self.symbol = symbol
        self.signal = signal


class TempTrades(declarative_base()):
    __tablename__ = 'temp_trades'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    fname = sqlalchemy.Column(sqlalchemy.String(length=50), primary_key=True)
    lname = sqlalchemy.Column(sqlalchemy.String(length=50), primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.DECIMAL)

    def __init__(self, fname, lname, price):
        self.fname = fname
        self.lname = lname
        self.price = price
