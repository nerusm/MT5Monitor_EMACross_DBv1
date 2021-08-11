import logging
import MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.notification.telegram_notificaton as tn
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config

def handle(e=None, msg=""):
    print(f"Type: {type(e)}")
    notification = tn.Notification()
    strat_name = config['strat_name']
    system_name =config['system_name']

    msg_string = f"{system_name}-{strat_name} \n{e}\n{msg}"
    logging.error(e)
    logging.error(msg_string)
    notification.send_err_notification(message=msg_string)


