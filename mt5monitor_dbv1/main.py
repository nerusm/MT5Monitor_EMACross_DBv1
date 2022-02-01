# from mt5monitor_dbv1.notification.whats_app import send_notification_msg
import logging

import MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.mt5_api.ema_cross_s1.ema_cross as ema
import MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.notification.telegram_notificaton as tn
import MetaTrader5 as mt5
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.db.db_trades_crud import TardesCrud
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.exceptions import handle
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.update_trades import sync_trade_book
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.utilities.utils import reason_text
from datetime import datetime

ema_cross = ema.EMA()


def start_ema_cross(symbols, time_frame, ema_span, strat_id):
    notification = tn.Notification(ema_cross.db_connection)
    is_ema_crossed = False
    is_ema_cross = None
    list_executed_trades_dict = []
    for symbol in symbols:
        is_ema_cross = (ema_cross.main_fun(symbol=symbol, time_frame=time_frame, ema_span=ema_span,
                                           strat_id=strat_id))
        if not is_ema_crossed == True:
            is_ema_crossed = bool(is_ema_cross['is_crossed'])
        if bool(is_ema_cross['is_crossed']):
            list_executed_trades_dict.append(is_ema_cross['response_dict'])
    logging.debug(f"is_ema_crossed: {is_ema_crossed}")
    if is_ema_crossed:
        logging.debug("Sending notification")
        notification.send_notification_msg(message="", timeframe=time_frame)
    logging.debug(f"Number of executed trades: {len(list_executed_trades_dict)}")
    trade_crud = TardesCrud()
    trade_crud.create_session(schema_name="trade_schema", from_func="main.start_ema_cross",
                              engine=trade_crud.get_connection(schema_name="trade_schema",
                                                               from_func="main.start_ema_cross"))
    for element in list_executed_trades_dict:
        trade_response = element['response']
        logging.debug(f"TRADING RESP: {trade_response}")

        if trade_response is not None:
            try:
                notification.send_trade_notification(symbol=symbol, time_taken=datetime.now(), time_frame=time_frame,
                                                     trade_direction=element['signal'], strat_id=element['usr_comment'])
                trade_crud.addNewTrade(position_id=trade_response.order, symbol=symbol,
                                       order_type=element['signal'],
                                       price=trade_response.price,
                                       magic=trade_response.request.magic,
                                       comment=element['usr_comment'],
                                       request_id=trade_response.request_id,
                                       is_open=True, volume=0.01, strat_id=strat_id,
                                       reason=reason_text(mt5.ORDER_REASON_EXPERT),
                                       parent_position_id=None)
            except Exception as e:
                handle(e=e, msg=f"Exception adding new trade to table")
                trade_crud.roll_back()
    trade_crud.close_connection(from_func="main.start_ema_cross")
    trade_crud.close_session()
    sync_trade_book()
