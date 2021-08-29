import logging
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config

log_file_name=config['log_file_path']
format = config['log_format']
print(f"Log filename: {log_file_name}")
logging.basicConfig(filename=log_file_name, format=format,
                    level=logging.DEBUG)


def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter(format)
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)


# setup_logger('log1', txtName+"txt")
# setup_logger('log2', txtName+"small.txt")
# logger_1 = logging.getLogger('log1')
# logger_2 = logging.getLogger('log2')