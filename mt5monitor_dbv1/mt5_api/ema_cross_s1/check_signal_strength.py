import logging
# import mt5monitor_dbv1.mt5_api.ema_cross as ema
import talib
import mt5monitor_dbv1.mt5_api.ema_cross_s1.ema_cross_s1_model

from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.utilities.signal_enum import Signal


def check_signal(prev_ema_bool):
    # prev_ema_bool = bool(prev_ema_bool)
    # logging.debug(f"pre_ema_bool: {prev_ema_bool}")
    if (prev_ema_bool == 'True'):
        logging.debug(f"Signal: {Signal.SELL.name}")
        return Signal.SELL.name
    else:
        logging.debug(f"Signal: {Signal.BUY.name}")
        return Signal.BUY.name

def check_candle(df):
    logging.debug()

