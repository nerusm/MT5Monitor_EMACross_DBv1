from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.main import start_ema_cross
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config

time_frame_dict = {15: 15, 30: 30, 60: 16385, 120: 16386, 180: 16387, 240: 16388}

symbols = config['symbols']
time_frame = config['time_frame']
ema_span = config['ema_spans']
strat_id = config['strat_id']

start_ema_cross(symbols=symbols, time_frame=time_frame_dict.get(int(time_frame)),
                    ema_span=ema_span, strat_id=int(strat_id))