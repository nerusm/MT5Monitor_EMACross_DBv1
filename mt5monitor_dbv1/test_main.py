from mt5monitor_dbv1.main import start_ema_cross
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config
# print(config["timezone"])
# start_ema_cross(symbols=['GBPCAD'],time_frame=30)

# tf=config["time_frame_dict"]
# print(tf)

time_frame_dict = {15: 15, 30: 30, 60: 16385, 120: 16386, 180: 16387, 240: 16388}

# start_ema_cross(
#     symbols=['GBPUSD', 'EURUSD', 'USDJPY', 'USDCAD', 'AUDUSD', 'NZDUSD', 'USDCHF', 'EURJPY',
#              'EURAUD', 'EURCAD', 'EURGBP', 'AUDJPY', 'AUDCAD', 'GBPCAD', 'GBPAUD', 'GBPJPY'],
#     time_frame=time_frame_dict.get(30), ema_span=['5','12'])

start_ema_cross(
    symbols=['GBPUSD'],
    time_frame=time_frame_dict.get(60), ema_span=['1','50'], strat_id=config['strat_id'])
