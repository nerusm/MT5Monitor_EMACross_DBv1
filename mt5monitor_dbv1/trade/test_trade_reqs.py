from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.trade_order_requests import execute_trade

symbol = 'USDJPY'

order_response = execute_trade(symbol=symbol.upper(), signal='BUY', action='new',
                               position_id=1044467250)

