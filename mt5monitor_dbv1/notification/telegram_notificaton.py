import logging
import os

import pandas as pd
import telegram
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config



def get_file_name(path1, filename):
    return os.path.join(path1, filename)


def archive_files():
    cross_file_path = os.path.join(config['output_base_path'], config['output_cross_result_dir'])
    archive_file_path = os.path.join(config['output_base_path'], config['archive_dir'])
    for file in os.listdir(cross_file_path):
        logging.debug(f"Archiving file: {get_file_name(cross_file_path, file)}")
        os.rename(get_file_name(cross_file_path, file), get_file_name(archive_file_path, file))


def create_message(timeframe):
    cross_file_path = os.path.join(config['output_base_path'], config['output_cross_result_dir'])
    files = os.listdir(cross_file_path)
    msg_str_list = []
    for f in files:
        df = pd.read_csv(os.path.join(cross_file_path, f), sep="\t")
        for index, row in df.iterrows():
            txt = "EMACross <b>{timeframe}</b>\n" \
                  "Symbol:  <b>{symbol}</b>\n" \
                  "Time:       <b>{time} IST</b>\n" \
                  "Signal:     <b>{signal}</b> \n" \
                  "Strength:   <b>{strength}</b>\n" \
                  "ClosePriceAbove 20EMA: <b> {closing_greater_20ema} </b>\n" \
                  "RSIAbove 50: <b> {rsi_greater_50} </b>\n" \
                  "SAR Below: <b> {sar_below} </b>\n" \
                  "******************************************* \n".format(symbol=row['symbol'],
                                                                          time=row['time'],
                                                                          signal=row['signal'],
                                                                          timeframe=config[
                                                                              "time_frame_dict"].get(
                                                                              timeframe),
                                                                          strength=row['strength'],
                                                                          closing_greater_20ema=row[
                                                                              'closing_greater_20ema'],
                                                                          rsi_greater_50=row[
                                                                              'rsi_greater_50'],
                                                                          sar_below=row[
                                                                              'sar_below'])
            msg_str_list.append(txt)

    return msg_str_list


class Notification:
    bot = None
    group_id = "-" + str(config['forex_group_id'])


    def __init__(self, db_connection=None):
        bot_token = config['bot_token']
        self.bot = telegram.Bot(token=bot_token)
        self.db_connection = db_connection

    def send_notification_msg(self, message, timeframe):
        messages = create_message(timeframe=timeframe)
        if config['send_notification'] == True:
            for message in messages:
                try:
                    res = self.bot.send_message(chat_id=self.group_id, text=message,
                                                parse_mode="HTML")
                    # archive_files()
                    logging.debug(f"Notification sent to Chat: {res.chat.title}")

                except Exception as e:
                    logging.error(f"Error occurred while sending notification: "
                                  f"{e.__class__.__name__}:: {e.message}")
        else:
            logging.debug("send_notification is disabled")
            logging.debug("*****************************")
            file1 = open('cross_results_dbversion.txt', 'a+')
            file1.writelines(messages)
            file1.flush()
            file1.close()
            for message in messages:
                logging.debug(f"Message: \n {message}")
        # archive_files()

    def send_err_notification(self,message):
        f_message = f"<b>Exception Occured: </b>\n {message}"
        res = self.bot.send_message(chat_id=self.group_id, text=f_message,
                                    parse_mode="HTML")

