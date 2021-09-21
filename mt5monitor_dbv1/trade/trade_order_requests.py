import MetaTrader5 as mt5
from MetaTrader5._core import OrderSendResult, TradeRequest
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config
from random import randint
import logging, time


type_time = mt5.ORDER_TIME_DAY
type_filling = mt5.ORDER_FILLING_RETURN
deviation = 30
magic = 72591869591


# retry_count = 0

def init_mt5():
    if not mt5.initialize():
        logging.debug("initialize() failed, error code =", mt5.last_error())
        quit()
    else:
        logging.debug('************************************************************* mt5 initialised')


def order_type(signal):
    if signal == 'BUY':
        return mt5.ORDER_TYPE_BUY
    else:
        return mt5.ORDER_TYPE_SELL


def get_req_new_order(trade_request, comment="python script open"):
    symbol = trade_request.get('symbol')
    sl_tp = get_sl_tp(symbol=symbol, tp_pips=trade_request.get('tp_pips'),
                      order_type=trade_request.get('order_type'))
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": trade_request.get('lot'),
        "type": trade_request.get('order_type'),
        "price": sl_tp[0],
        "sl": trade_request.get('stop_loss'),
        "tp": sl_tp[2],
        "deviation": deviation,
        "magic": magic,
        "comment": trade_request.get('comment'),
        "type_time": mt5.ORDER_TIME_DAY,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    return request


def get_close_order_req(trade_request):
    price = get_sl_tp(symbol=trade_request.get('symbol'),
                      tp_pips=20,
                      order_type=trade_request.get('order_type'))[0]
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": trade_request.get('symbol'),
        "volume": trade_request.get('lot'),
        "type": trade_request.get('order_type'),
        "position": trade_request.get('position_id'),
        "price": price,
        "deviation": deviation,
        "magic": magic,
        "comment": trade_request.get('comment'),
        "type_time": type_time,
        "type_filling": type_filling,
    }
    return request


# def get_req_close_order()

def get_sl_tp(symbol, tp_pips, order_type):
    symbol = symbol.upper()
    point = mt5.symbol_info(symbol).point

    if order_type == mt5.ORDER_TYPE_BUY:
        price = mt5.symbol_info_tick(symbol).ask
        sl = price - (tp_pips * 10) * point
        tp = price + (tp_pips * 10) * point
    else:
        price = mt5.symbol_info_tick(symbol).bid
        tp = price - (tp_pips * 10) * point
        sl = price + (tp_pips * 10) * point
    return price, sl, tp


def get_order_request_dict(symbol, lot_size, order_type, stop_loss = None, position_id=None, tp_pips=None, comment='default'):
    data_dict = {
        'symbol': symbol,
        'lot': lot_size,
        'position_id': position_id,
        'order_type': order_type,
        'tp_pips': tp_pips,
        'stop_loss':stop_loss,
        'comment' : comment
    }
    return data_dict


def get_order_request(action, data_dict):
    switcher = {
        'new': get_req_new_order,
        'close': get_close_order_req
    }
    func = switcher.get(action)
    return func(data_dict)

def execute_trade(symbol, signal, action=None,
                  position_id=None, stop_loss = None, retry_count=1,
                  comment = 'default'):
    init_mt5()
    lot_size = config['lot_size']
    tp_pips = config['tp_pips']

    order_request = get_order_request(action=action,
                                      data_dict=get_order_request_dict(symbol=symbol,
                                                                       lot_size=lot_size,
                                                                       order_type=order_type(
                                                                           signal),
                                                                       tp_pips=tp_pips,
                                                                       position_id=position_id,
                                                                       stop_loss=stop_loss,
                                                                       comment=comment))
    logging.debug(f"Request: {order_request} ")
    response = mt5.order_send(order_request)
    logging.debug(f"Response: {response}")
    if response is not None:
        ret_code = response.retcode
        logging.debug(f"In Response is not None: {ret_code}")
    else:
        logging.warning(f"Sleep for {config['retry_interval_secs']} seconds and re-init mt5...")
        ret_code = 0
        time.sleep(config['retry_interval_secs'])
        init_mt5()
        if retry_count <= config.get('no_of_retries'):
            logging.debug(f"Re-executing trade with new request. Retry Count: {retry_count}")
            retry_count += 1
            mt5.shutdown()
            execute_trade(symbol=symbol,
                          signal=signal,
                          action=action,
                          position_id=position_id,
                          retry_count=retry_count)
        else:
            logging.error(f"Retires exhausted Response NONE: {config.get('no_of_retries')}. Exiting.")
    if ret_code != mt5.TRADE_RETCODE_DONE:
        logging.debug(f"Order request not accepted. \n"
              f"Return Code: {ret_code} \n"
              f"Return Message: {response.comment}\n")
        if ret_code in config.get('retry_ret_codes'):
            if retry_count <= config.get('no_of_retries'):
                logging.debug(f"Re-executing trade with new request. Retry Count: {retry_count}")
                retry_count += 1
                mt5.shutdown()
                execute_trade(symbol=symbol,
                              signal=signal,
                              action=action,
                              position_id=position_id,
                              retry_count=retry_count)
            else:
                logging.error(f"Retires exhausted: {config.get('no_of_retries')}. Exiting.")
        else:
            logging.error(f"Return Code not in retry return codes: {config.get('retry_ret_codes')}")

    # mt5.shutdown()
    # response = stub_newtrade_success_response(response)
    return response

def stub_newtrade_success_response(response):
    rand_position_id = randint(1000000000,2000000000)
    rand_order_id = randint(1000000000,2000000000)
    res =OrderSendResult((10009,rand_order_id,rand_position_id,0.01,1.48581,1.48581,
                          1.4859200000000001,'Request executed',2,0,response.request))
    return res
