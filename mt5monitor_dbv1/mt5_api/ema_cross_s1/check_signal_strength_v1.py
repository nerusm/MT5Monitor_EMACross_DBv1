import math

import pandas as pd
import talib
import talib.stream
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.mt5_api.ema_cross_s1.candle_stick_model import CandleStick
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.mt5_api.ema_cross_s1.ema_cross_s1_model import EmaCrossResult


def prepare_dataset(data):
    data = data.drop(len(data) - 1)
    round_digits = 5

    data['EMA_6'] = data['close'].ewm(span=6, adjust=False).mean().round(round_digits)
    data['EMA_12'] = data['close'].ewm(span=12, adjust=False).mean().round(round_digits)
    data['EMA_20'] = data['close'].ewm(span=20, adjust=False).mean().round(round_digits)
    # data['SMMA-50'] = data['close'].rolling(50).mean()
    data['SAR'] = talib.SAR(data.high, data.low, acceleration=0.02, maximum=0.2).round(
        round_digits)
    data['RSI_14'] = talib.RSI(data.close, timeperiod=14).round(2)
    # data.to_csv("output.csv", sep=",")
    # comment to trigger commit
    return data


class SignalStrength:
    ema_model = EmaCrossResult()

    # last_candle_stick = None
    def __init__(self, signal, df_rates, symbol):
        self.ema_model.signal = signal
        self.df_rates = df_rates
        self.symbol = symbol
        self.prepared_dataset = prepare_dataset(data=df_rates)
        self.last_candle_stick = CandleStick(symbol=symbol,
                                             data=df_rates)

    def check_indicators(self):
        tail_record = self.prepared_dataset.tail(1)
        # print(tail_record)
        self.ema_model.symbol = self.symbol
        self.ema_model.time = tail_record.iloc[0].time

        # Check if closing price above 20EMA
        close_above_ema20 = self.last_candle_stick.close > tail_record.iloc[0].EMA_20
        self.ema_model.closing_greater_20ema = close_above_ema20
        # print(f"************ Closing Price above 20EMA: {close_above_ema20}
        # Close: {self.last_candle_stick.close} : EMA:{tail_record.iloc[0].EMA_20} ")

        # Check if the EMA is_crossed is above 20EMA
        cross_above_ema20 = tail_record.iloc[0].EMA_6 > tail_record.iloc[0].EMA_20
        self.ema_model.crossed_greater_20ema = cross_above_ema20

        # Check if RSI is greater than or equal to 50
        rsi_above_50 = tail_record.iloc[0].RSI_14 >= 50
        self.ema_model.rsi_greater_50 = rsi_above_50
        # print(f"************ RSI above 50: {rsi_above_50}")

        # Check if SAR is below the low
        sar_below_lastLow = tail_record.iloc[0].SAR < self.last_candle_stick.low
        self.ema_model.sar_below = sar_below_lastLow
        # print(f"************ SAR below LOW: {sar_below_lastLow}")

        result_dict = {
            'result': [close_above_ema20, rsi_above_50, sar_below_lastLow]}
        # result_dict = {
        #     'result': [close_above_ema20, cross_above_ema20, rsi_above_50, sar_below_lastLow]}
        return self.get_strength(result_dict)

    def get_strength(self, result_dict):
        trues = 0
        df = pd.DataFrame(result_dict)
        if self.ema_model.signal == 'BUY':
            trues = len(df[df['result'] == True])
        else:
            trues = len(df[df['result'] == False])

        if trues == len(df):
            self.ema_model.strength = "STRONG"
        elif trues >= math.ceil(len(df) / 2):
            self.ema_model.strength = "MODERATE"
        else:
            self.ema_model.strength = "WEEK"
        #
        # if self.ema_model.signal == 'BUY' and self.ema_model.sar_below != True:
        #     self.ema_model.strength = "WEEK"
        #
        # elif self.ema_model.signal == 'SELL' and self.ema_model.sar_below != False:
        #     self.ema_model.strength = "WEEK"

        return self.ema_model
