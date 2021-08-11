import logging

import MetaTrader5 as mt5
from MetaTrader5._core import TradePosition

from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.exceptions import handle
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.trade_order_requests import execute_trade
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.update_trades import get_open_positions


def flip_signal(signal):
    flipper = {
        'SELL': 'BUY',
        'BUY': 'SELL'
    }
    return flipper.get(signal)


def execute_trade_wrapper(symbol, signal, stop_loss, parent_position_id, strat_id=1,
                          strat_ref_id=1,
                          usr_comment='default'):
    open_positions = get_open_positions(symbol=symbol, signal=flip_signal(signal),
                                        comment=usr_comment)
    if len(open_positions) > 0:
        for position_id in open_positions:
            tp = TradePosition(open_positions[position_id])
            logging.debug(f"Closing existing {symbol} {signal} trade, position id: {position_id}")
            close_trade(symbol=symbol, signal=signal, position_id=position_id)
    else:
        logging.debug(f"No {flip_signal(signal)} open for symbol: {symbol}")

    logging.debug(f"Opening a new {signal} trade")
    return open_new_trade(symbol=symbol, signal=signal, stop_loss=stop_loss, strat_id=strat_id,
                          strat_ref_id=None, usr_comment=usr_comment)


def open_new_trade(symbol, signal, stop_loss, strat_id, strat_ref_id, usr_comment,
                   parent_position_id=None):
    exception_msg = f"<b>Open new Trade</b>\n" \
                    f"Symbol: {symbol} \n" \
                    f"Signal: {signal} \n" \
                    f"Strat Id: {strat_id}"
    trade_response = execute_trade(symbol=symbol,
                                   signal=signal, action='new', stop_loss=stop_loss,
                                   comment=usr_comment)
    if trade_response is not None:
        if trade_response.retcode == mt5.TRADE_RETCODE_DONE:
            logging.debug(f"Trade Response: {trade_response}")
        else:
            logging.error(
                f"Trade Execution Failed, symbol: {symbol}, response code: {trade_response.retcode}")
            handle(
                msg=f"Trade Execution Failed, symbol: {symbol}, signal: {signal}, response code: {trade_response.retcode}")
            logging.error(f"{trade_response}")

    else:
        logging.error(f"Trade Response is None")
    return trade_response


def close_trade(symbol, signal, position_id):
    trade_response = execute_trade(symbol=symbol, signal=signal, action='close',
                                   position_id=position_id)
    if trade_response.retcode == mt5.TRADE_RETCODE_DONE:
        logging.debug("Trade Closed")

    logging.debug(f"Trade Response: {trade_response}")
    return trade_response
