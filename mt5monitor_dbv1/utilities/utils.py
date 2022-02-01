import logging
import os
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo



from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config as config


def debug(message):
    curr_runtime_timestamp = time.strftime("%d:%m:%Y %H:%M:%S", time.localtime())
    print(f"{curr_runtime_timestamp}: {message}")
    filename = "EMA_Resuts1.csv"
    name = os.path.join(config['output_base_path'], config['output_ema_dir'], filename)
    logging.debug(f"Test logging {name}")


def convert_to_ist(server_time):
    # server_time = datetime.strptime(server_time, "%Y-%m-%d %H:%M:%S")
    # pytz.all_timezones
    # server_timezone = pytz.timezone('Europe/Athens')
    # ist_timezone = pytz.timezone('Asia/Kolkata')
    # server_localised = server_timezone.localize(server_time)
    # new_Time = server_localised.astimezone(ist_timezone)
    # return new_Time.replace(tzinfo=None)
    return server_time

def convert_to_athens(local_time):
    # server_time = datetime.strptime(server_time, "%Y-%m-%d %H:%M:%S")
    # pytz.all_timezones
    # server_timezone = pytz.timezone('Europe/Athens')
    # ist_timezone = pytz.timezone('Asia/Kolkata')
    # server_localised = ist_timezone.localize(local_time)
    # new_Time = server_localised.astimezone(server_timezone)
    # return new_Time.replace(tzinfo=None)
    return local_time

def millisec_to_timestamp(ms):
    target_date_time_ms = ms # or whatever
    base_datetime = datetime( 1970, 1, 1 )
    delta = timedelta( 0, 0, 0, target_date_time_ms )
    return base_datetime + delta


def reason_text(reason_int):
    reason = {
        0: 'CLIENT',
        1: 'MOBILE',
        2: 'WEB',
        3: 'EXPERT',
        4: 'SL',
        5: 'TP',
        6: 'SO'
    }
    return reason.get(reason_int)

def order_type_name(type_int):
    type = {
        0: 'BUY',
        1: 'SELL'
    }
    return type.get(type_int)

def is_trade_restricted():
    ntr_t = config['no_trade_time_range']
    ntr_d = config['no_trade_day_range']
    logging.debug(f"ntr_d: {ntr_d} ntr_t: {ntr_t}")
    ct = datetime.now()
    tt = ct.timetuple()
    t=tt.tm_hour
    d=tt.tm_wday
    if d in ntr_d:
        return True
    for tr in ntr_t:
        no_trd_range = range(tr[0],tr[1]+1)
        if t in no_trd_range:
            return True
# print(convert_to_ist("2021-05-18 11:50:00"))
