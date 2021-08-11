import logging
import os
from datetime import datetime as dt

import pandas as pd
import pywhatkit as py
from mt5monitor_dbv1.configuration.app_config import config


def send_notification_msg(message):
    message = create_message()
    if config['send_notification']:
        if config['send_instant_msg']:
            # Single Mobile Number
            s = "+" + str(config['whatsapp_number'])
            print(s)
            py.sendwhatmsg_instantly(s, message=message)
        else:
            #  Group Message
            dtime = dt.now()
            py.sendwhatmsg_to_group(config['whatsapp_group_id'], message, dtime.hour,
                                    dtime.minute + 2, wait_time=40,
                                    print_wait_time=True)
        archive_files()
    else:
        logging.debug("send_notification is disabled")


def archive_files():
    cross_file_path = os.path.join(config['output_base_path'], config['output_cross_result_dir'])
    archive_file_path = os.path.join(config['output_base_path'], config['archive_dir'])
    for file in os.listdir(cross_file_path):
        logging.debug(f"Archiving file: {get_file_name(cross_file_path, file)}")
        os.rename(get_file_name(cross_file_path, file), get_file_name(archive_file_path, file))


def get_file_name(path1, filename):
    return os.path.join(path1, filename)


def create_message():
    cross_file_path = os.path.join(config['output_base_path'], config['output_cross_result_dir'])
    files = os.listdir(cross_file_path)
    msg_str = ""
    for f in files:
        file = open(os.path.join(cross_file_path, f), "r")
        df = pd.read_csv(os.path.join(cross_file_path, f), sep="\t")
        for index, row in df.iterrows():
            txt = "EMACross: *{symbol}* Time: *{time} IST* \n ".format(symbol=row['symbol'],
                                                                       time=row['time'])
            msg_str = msg_str + txt

    return msg_str

# send_notification_msg("d")
