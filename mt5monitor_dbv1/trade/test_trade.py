import MetaTrader5
import MetaTrader5 as mt5
import logging
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta

class Trade:
    def __init__(self):
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            quit()
        print('mt5 init')

def trade_fun(symbol):
    symbol = symbol.upper()
    print(mt5.account_info())
    print(mt5.positions_total())
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    sl = price - 200 * point
    tp = price + 200 * point
    print(f"c price: {price}")
    print(f"c point: {point}")
    print(f"sl: {sl}")
    print(f"tp: {tp}")
    # mt5.shutdown()

def get_request(symbol, lot, order_type, tp_pips):
    symbol = symbol.upper()
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).bid
    # point = round(point, 6)
    # price = round(price, 4)
    deviation = 300
    tp_pips = tp_pips * 10
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "tp": price - tp_pips * point,
        "sl": price + tp_pips * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.symbol_info(symbol).filling_mode,
    }
    return request

# td = Trade()
# print(MetaTrader5.ACCOUNT_TRADE_MODE_REAL)
# info = mt5.symbol_info("GBPJPY").filling_mode
# print( mt5.account_info() )
# print(MetaTrader5.account_info())


timezone = pytz.timezone("Etc/UTC")
# create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2022, 2, 1, tzinfo=timezone)

mt5.shutdown()
# trade_fun("GBPUSD")
# trade_fun("EURcaD")
# request = get_request('GBPJPY',0.01,mt5.ORDER_TYPE_SELL,20)
# print(request)
# print("***")
# response = mt5.order_send(request)
# #
# print(response)
# print(mt5.positions_total())
# # mt5.shutdown()