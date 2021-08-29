import os
import sys
import time
from datetime import datetime

from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.retrade.retrade import execute_retrades
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# time_frame = mt5.TIMEFRAME_M15.__int__()

# time_frame_dict =
time_frame_dict = {15: 15, 30: 30, 60: 16385, 120: 16386, 180: 16387, 240: 16388}


def train_model():

    execute_retrades()
    print(f"Done: {datetime.now()}")
    print(f"-------------------------------------------------------")


if __name__ == '__main__':

    scheduler = BackgroundScheduler()
    scheduler.add_job(train_model, IntervalTrigger(minutes=int(3)))
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        print("Run Once Now")

        execute_retrades()
        print(f"Done: {datetime.now()}")
        print(f"-------------------------------------------------------")
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)

    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        print("Scheduler shutdown")
        scheduler.shutdown()
