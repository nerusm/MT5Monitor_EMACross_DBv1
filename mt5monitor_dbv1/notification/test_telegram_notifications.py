import MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.notification.telegram_notificaton as tn
from datetime import datetime
n = tn.Notification()
# n.send_notification_msg("")
n.send_trade_notification(symbol="USDCAD",time_frame="H1",time_taken=datetime.now(),trade_direction="SELL", strat_id="EMA_Cross_3" )
