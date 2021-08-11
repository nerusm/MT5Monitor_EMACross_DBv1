import logging
import os
import time
from datetime import datetime

import MetaTrader5 as mt5
import numpy as np
import pandas as pd
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.db.db_connection import DB_Connection
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.mt5_api.ema_cross_s1.check_signal_strength_v1 import \
    SignalStrength
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.trade_wrapper import execute_trade_wrapper
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.utilities.signal_enum import Signal
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.utilities.utils import convert_to_ist
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.exceptions import handle

comment = 'EMA_Cross'
# comment = 'EMA_Cross_T'


def check_retrade(symbol, time_frame, no_of_bars, ema_span, signal, check_trend, lookback_stop_loss):
    no_of_bars_for_trend = 8
    index = list(range(0, no_of_bars_for_trend - 1))
    df_rates = __get_rates__(symbol=symbol, time_frame=time_frame, no_of_bars=no_of_bars)
    ema_rate = __get_ema__(df_rates=df_rates, ema_span=ema_span)
    df_tail = df_rates.tail(1).reset_index()
    ema_tail = ema_rate.tail(1).reset_index()

    df_tail_trend = df_rates.tail(no_of_bars_for_trend - 1)
    rates_list = df_tail_trend['close']

    trend = get_trend(index=index, data=rates_list, order=1)
    logging.debug(f"Trend: {symbol} : {trend}")
    stop_loss = find_stop_loss(n=lookback_stop_loss,data=df_rates, signal=signal)
    result = {}
    result_bool = False
    if check_trend:
        if signal == Signal.BUY.name:
            if df_tail.at[0, 'close'] > ema_tail.at[0, 'ema_long'] and trend == 'UP':
                result_bool = True
            else:
                result_bool = False
        else:
            if df_tail.at[0, 'close'] < ema_tail.at[0, 'ema_long'] and trend == 'DOWN':
                result_bool =  True
            else:
                result_bool =  False
    else:
        if signal == Signal.BUY.name:
            if df_tail.at[0, 'close'] > ema_tail.at[0, 'ema_long']:
                result_bool =  True
            else:
                result_bool =  False
        else:
            if df_tail.at[0, 'close'] < ema_tail.at[0, 'ema_long']:
                result_bool =  True
            else:
                result_bool =  False
    result['can_retrade']  = result_bool
    result['possible_stop_loss'] = stop_loss
    return result



def get_trend(index, data, order):
    logging.debug(f"Get Trend")
    coeffs = np.polyfit(index, list(data), order)
    slope = coeffs[-2]
    if slope > 0:
        return 'UP'
    else:
        return "DOWN"


def __get_ema__(df_rates, ema_span):
    short_span = int(ema_span[0])
    long_span = int(ema_span[1])
    round_digits = 5
    df_rates['ema_short'] = df_rates['close'].ewm(span=short_span, adjust=False).mean().round(
        round_digits)
    df_rates['ema_long'] = df_rates['close'].ewm(span=long_span, adjust=False).mean().round(
        round_digits)
    # comparision_result = np.where(df_rates['ema_short'] > df_rates['ema_long'], True, False)
    # df_rates['comparision_result'] = comparision_result
    # df_rates.to_csv("C:\Suren\Analysis\output_gbpusd.csv", index=False)
    # df_rates.at
    # pd.read_csv()
    frames = [df_rates['time'], df_rates['ema_short'], df_rates['ema_long']]
    return pd.concat(frames, axis=1)


def check_signal(prev_ema_bool):
    logging.debug(f"pre_ema_bool: {prev_ema_bool}")
    if prev_ema_bool:
        logging.debug(f"Signal: {Signal.SELL.name}")
        return Signal.SELL.name
    else:
        logging.debug(f"Signal: {Signal.BUY.name}")
        return Signal.BUY.name


def __check_crossed__(data, no_of_bars_to_check):
    tailed_df = data.tail(no_of_bars_to_check)
    tailed_df.reset_index(drop=True, inplace=True)
    logging.debug(f"tail: {tailed_df}")
    if tailed_df.at[0, 'short_grtr_long'] != tailed_df.at[1, 'short_grtr_long']:
        signal = check_signal(tailed_df.at[0, 'short_grtr_long'])
        return signal
    else:
        return None
        # return Signal.BUY.name
        # return Signal.SELL.name


def find_stop_loss(n, data, signal):
    if signal == 'SELL':
        tail = data.tail(n)['high'].round(4)
        tail.reset_index(drop=True, inplace=True)
        hh = tail.max()
        hhidx = tail.idxmax()
        if hhidx > 0:
            ph = tail.at[hhidx - 1]
        else:
            ph = hh
        if hhidx < tail.size:
            nh = tail.at[hhidx + 1]
        else:
            nh = hh
        if hhidx == 0:
            hh = find_stop_loss(n + 1, data, signal)
        else:
            return hh
        return hh
    else:
        tail = data.tail(n)['low']
        tail.reset_index(drop=True, inplace=True)
        ll = tail.min()
        llidx = tail.idxmin()
        if llidx > 0:
            pl = tail.at[llidx - 1]
        else:
            pl = ll
        if llidx < tail.size:
            nl = tail.at[llidx + 1]
        else:
            nl = ll
        if llidx == 0:
            find_stop_loss(n + 1, data, signal)
        else:
            return ll
        return ll


def __get_rates__(symbol, time_frame, no_of_bars):
    rates = mt5.copy_rates_from_pos(symbol, time_frame, 0, no_of_bars)
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
    daf.drop(daf.tail(1).index, inplace=True)
    return daf


class EMA:
    # db_connection = None
    index6 = range(12, 24)
    curr_runtime_timestamp = time.strftime("%d%m%Y_%H%M", time.localtime())
    ema_output_path = None
    cross_output_path_for_notification = None

    def __init__(self):
        self.db_conn_cls_obj = DB_Connection()
        self.db_connection = self.db_conn_cls_obj.get_connection(schema_name='schema_ema_monitor_30m', from_func=self.__module__)
        self.ema_output_path = os.path.join(config['output_base_path'], config['output_ema_dir'])
        self.cross_output_path_for_notification = os.path.join(config['output_base_path'],
                                                               config['output_cross_result_dir'])
        pd.set_option('display.max_columns', 500)  # number of columns to be displayed
        pd.set_option('display.width', 1500)  # max table width to display

        if not mt5.initialize():
            logging.error("initialize() failed, error code =", mt5.last_error())
            quit()

    def __write_result_for_notification__(self, symbol, result, time_frame, signal_name,
                                          signal_strength, possible_sl, strat_id):
        result['symbol'] = symbol
        result['signal'] = signal_name
        result['strength'] = signal_strength.strength
        result['closing_greater_20ema'] = signal_strength.closing_greater_20ema
        result['crossed_greater_20ema'] = signal_strength.crossed_greater_20ema
        result['rsi_greater_50'] = signal_strength.rsi_greater_50
        result['sar_below'] = signal_strength.sar_below
        result['possible_stop_loss'] = possible_sl

        if config['execute_trade'] is True:
            logging.debug("Executing Trade")
            for index, row in result.iterrows():
                logging.debug(f"Initiating trade request for {row['symbol']}")
                execute_trade_resp= execute_trade_wrapper(symbol=row['symbol'], signal=row['signal'],
                                             stop_loss=row['possible_stop_loss'],
                                             strat_id=strat_id,
                                             usr_comment=f"{comment}_{strat_id}",
                                             parent_position_id=None)
                try:
                    result.to_sql('cross_result', con=self.db_connection, if_exists='append',
                                  index=False)
                except Exception as e:
                    handle(e=e, msg="Exception while writing cross_result in write to notify")
                finally:
                    # self.db_conn_cls_obj.close_connection(from_func=self.__module__)
                    return execute_trade_resp
        else:
            logging.debug("NOT Executing Trade")


    def main_fun(self, symbol, time_frame, ema_span, strat_id):
        logging.debug("***********")
        logging.debug(f"        Processing Symbol: {symbol} at time_frame: {time_frame}")
        crossed = {}
        df_rates = __get_rates__(symbol=symbol,
                                 time_frame=time_frame,
                                 no_of_bars=config['no_of_bars'])
        if df_rates is not None:
            result = __get_ema__(df_rates, ema_span)

            length = len(result.index)
            comparision_result = np.where(result['ema_short'] > result['ema_long'], True, False)
            result["short_grtr_long"] = comparision_result

            signal = __check_crossed__(result, int(config['no_of_bars_to_check']))

            if signal is not None:
                result["is_crossed"] = "CROSS"
                crossed['is_crossed'] = True
                crossed['signal'] = signal
            else:
                crossed['is_crossed'] = False
                result["is_crossed"] = ""

            if signal is not None:
                result["is_crossed"] = "CROSS"
                signal_strength_obj = SignalStrength(symbol=symbol,
                                                     signal=signal,
                                                     df_rates=df_rates)
                signal_strength = signal_strength_obj.check_indicators()
                if signal_strength.strength == 'WEEK' and strat_id == 1:
                    result["is_crossed"] = ""
                    logging.debug(f"Strength is : {signal_strength.strength}, so rejecting this signal")
                else:
                    possible_sl = find_stop_loss(config['lookback_stop_loss'], df_rates, signal_strength_obj.ema_model.signal)
                    # print("Possible SL: ", possible_sl)
                    res = self.__write_result_for_notification__(symbol=symbol,
                                                                 result=pd.DataFrame(
                                                                     result.iloc[length - 2:length - 1,
                                                                     :]).copy(),
                                                                 time_frame=time_frame,
                                                                 signal_name=signal,
                                                                 signal_strength=signal_strength,
                                                                 possible_sl=possible_sl,
                                                                 strat_id=strat_id)
                    response_dict = dict(response=res,
                                         signal=crossed['signal'],
                                         usr_comment=f"{comment}_{strat_id}")
                    crossed['response_dict'] = response_dict

            else:
                result["is_crossed"] = ""

            if crossed is None:
                logging.warning(f"Crossed is NONE Symbol: {symbol}")
            logging.debug(f"        {str(datetime.now())}  "
                          f"********** {symbol} ********** {time_frame} "
                          f"***** Crossed: {crossed['is_crossed']}"
                          f"***** Signal: ")
            return crossed
        else:
            crossed['is_crossed'] = False
            logging.warning(f"Could not download rates for Symbol: {symbol}")
            return crossed
