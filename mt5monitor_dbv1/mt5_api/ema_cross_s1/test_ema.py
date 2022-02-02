import logging
import os
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config, \
    get_round_decimal
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.db.db_connection import DB_Connection
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.mt5_api.ema_cross_s1.check_signal_strength_v1 import \
    SignalStrength
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.trade_wrapper import execute_trade_wrapper
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.utilities.signal_enum import Signal
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.utilities.utils import convert_to_ist, \
    is_trade_restricted


time_frame_dict = {15: 15, 30: 30, 60: 16385, 120: 16386, 180: 16387, 240: 16388}

time_frame=time_frame_dict.get(30)

def init_mt5():
    # logging.info("Initialising MT5")
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

def __get_rates__(symbol, time_frame, no_of_bars):
    init_mt5()

    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime.today()+relativedelta(days=1,hour=0, minute=0, second=0,microsecond=0)
    logging.info(f"UTC_FROM: {utc_from}")

    rates = mt5.copy_rates_from(symbol, time_frame, utc_from, no_of_bars)
    logging.info("Using Alternate function...")
    # logging.info("\nT:\n")
    # logging.info(rates_dump)

    # rates = mt5.copy_rates_from_pos(symbol, time_frame, 0, no_of_bars)

    # mt5.cop
    retry_count = 0
    no_of_retries = config['no_of_retries']
    if rates is None:
        while retry_count < no_of_retries:
            time.sleep(config['retry_interval_secs'])
            retry_count += 1
            logging.warning(
                f"Rates None, retrying {retry_count} in {config['retry_interval_secs']} seconds "
                f"after re-initialising mt5")
            if not mt5.initialize():
                logging.error("initialize() failed, error code =", mt5.last_error())
                quit()
            rates = mt5.copy_rates_from_pos(symbol, time_frame, 0, no_of_bars)
            if rates is not None:
                break

    # create DataFrame out of the obtained data
    rates_frame = pd.DataFrame(rates)

    # convert time in seconds into the datetime format
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame['time'] = rates_frame['time'].apply(convert_to_ist)
    rates_frame['close'] = rates_frame['close']
    daf = pd.DataFrame(rates_frame.iloc[:, 0:5]).copy()
    # drop the last row since it is the current candle..
    daf.drop(daf.tail(1).index, inplace=True)
    mt5.shutdown()
    logging.info(f"\n {daf.tail(2)}")
    return daf

__get_rates__(symbol='AUDUSD', time_frame=time_frame,no_of_bars=5000)