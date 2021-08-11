import MetaTrader5 as mt5
from  datetime import datetime

def init_mt5():
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

from_date = datetime(2021,7,19)
to_date = datetime.now()
print(f"{from_date} : {to_date}")
init_mt5()
history_orders=mt5.history_deals_get(from_date, to_date)
if history_orders==None:
    print("No history orders with group=\"*GBP*\", error code={}".format(mt5.last_error()))
elif len(history_orders)>0:
    print("history_orders_get({}, {}, group=\"*GBP*\")={}".format(from_date,to_date,len(history_orders)))
    for t in history_orders:
        print(t.entry)
print()
mt5.shutdown()
print("hello")