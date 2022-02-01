from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.trade_wrapper import execute_trade_wrapper

symbol = 'USDCAD'
signal = 'BUY'
sl = 1.2720

print(execute_trade_wrapper(symbol=symbol, signal=signal, stop_loss=sl, strat_id=1,
                            usr_comment="Testing Filling Mode",
                            parent_position_id=None))
