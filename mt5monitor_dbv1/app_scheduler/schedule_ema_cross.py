import os
import sys
import time
from datetime import datetime

from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.main import start_ema_cross
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers import interval

# time_frame = mt5.TIMEFRAME_M15.__int__()

# time_frame_dict =
time_frame_dict = {15: 15, 30: 30, 60: 16385, 120: 16386, 180: 16387, 240: 16388}


def train_model():
    print(f"len: {len(sys.argv)}")
    # if not len(sys.argv) == 5:
    #     print("Argument missing")
    #     exit(0)
    symbols = config['symbols']
    time_frame = config['time_frame']
    ema_span = config['ema_spans']
    strat_id = config['strat_id']
    print(f"Time Frame: {time_frame}")
    print(f"Symbols: {symbols}")
    print(f"Spans: {ema_span}")
    print(f"Strat_ID: {strat_id}")
    print("DB Version")
    start_ema_cross(symbols=symbols, time_frame=time_frame_dict.get(int(time_frame)),
                    ema_span=ema_span, strat_id=int(strat_id))
    print(f"Done: {datetime.now()}")
    print(f"-------------------------------------------------------")


if __name__ == '__main__':
    symbols = config['symbols']
    time_frame = config['time_frame']
    ema_span = config['ema_spans']
    strat_id = config['strat_id']
    print(datetime.now())
    print(len(sys.argv))
    print(sys.argv)
    print(f"S: {symbols}")
    print(f"t: {time_frame}")
    print(f"e: {ema_span}")
    print(f"sr: {strat_id}")
    # if not len(sys.argv) == 5:
    #     print("Argument missing Symbol")
    #     exit(0)
    scheduler = BackgroundScheduler()
    scheduler.add_job(train_model, IntervalTrigger(minutes=int(time_frame)))
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        print("Run Once Now")

        print(symbols)
        start_ema_cross(symbols=symbols, time_frame=time_frame_dict.get(int(time_frame)),
                        ema_span=ema_span, strat_id=int(strat_id))
        print(f"Done: {datetime.now()}")
        print(f"-------------------------------------------------------")
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)

    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        print("Scheduler shutdown")
        scheduler.shutdown()
