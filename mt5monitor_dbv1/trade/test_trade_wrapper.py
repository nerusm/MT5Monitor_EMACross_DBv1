from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.trade_wrapper import execute_trade_wrapper

symbol = 'GBPUSD'
# signal='BUY'
# sl=1.1772
signal = 'BUY'
sl = 1.3846

print(execute_trade_wrapper(symbol=symbol, signal=signal, stop_loss=sl, strat_id=1,
                            usr_comment="Testing Exception handling",
                            parent_position_id="d"))
