import logging
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config

log_file_name=config['retrade_log_file_path']
format = config['log_format']
print(f"Log filename: {log_file_name}")
logging.basicConfig(filename=log_file_name, format=format,
                    level=logging.DEBUG)