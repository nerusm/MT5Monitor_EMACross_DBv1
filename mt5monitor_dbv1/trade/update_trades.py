import logging

import MetaTrader5 as mt5
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.db.db_trades_crud import TardesCrud
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.exceptions import handle
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.utilities.signal_enum import OrderType
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.utilities.utils import millisec_to_timestamp, \
    reason_text, order_type_name
from MetaTrader5._core import TradePosition

print("why update trades")
tc = TardesCrud()
conn = tc.get_connection(schema_name="trade_schema",from_func="update_trades.1")
tc.create_session(schema_name="trade_schema", from_func="update_trades.sync_book", engine=conn)


def init_mt5():
    if not mt5.initialize():
        logging.fatal("initialize() failed, error code =", mt5.last_error())
        quit()


def update_trade_wrapper(position_id):
    init_mt5()
    deals = mt5.history_deals_get(position=position_id)
    update_trade(deals)


def sync_trade_book():
    try:
        logging.debug(f"Syncing trade books")
        open_trades = tc.selectAllOpenTrades()
        posid_dict_list = []
        for open_trade in open_trades:
            position_id = open_trade.position_id
            # print(f"PID: {position_id}")
            deals = get_entry_exit_deals(position_id)
            # print(f"Entry: {deals[0]}")
            # print(f"Exit: {deals[1]}")
            posid_dict = update_trade(deals)
            if posid_dict is not None:
                posid_dict_list.append(posid_dict)
        create_retrade_records(posid_dict_list=posid_dict_list)
    except Exception as e:
        handle(e=e, msg="failure in syncing trade books")
        tc.roll_back()
    finally:
        print("In Finally Sync")
        tc.close_connection(from_func="update_trades.sync_book")
        tc.close_session()

def create_retrade_records(posid_dict_list):
    if len(posid_dict_list) > 0:
        for posid_dict in posid_dict_list:
            tc.addNewRetrade(posid_dict)


def get_strat_id(comment):
    sp = comment.split("_")
    return sp[len(sp)-1]

def update_trade(deals):
    entry_deal = deals[0]
    strat_id_deal = get_strat_id(entry_deal.comment)
    if deals[1] is not None:
        exit_deal = deals[1]
        logging.debug(f"Exit Deal: {exit_deal}")
        position_id = exit_deal.position_id
        exception_msg = f"Error Updating Trade Book\n" \
                        f"Position Id: {position_id}"

        try:
            tc.updateStatusByPositionId(symbol=exit_deal.symbol,position_id=exit_deal.position_id,
                                        profit=exit_deal.profit,
                                        reason=reason_text(exit_deal.reason),
                                        volume=exit_deal.volume,
                                        open_time=millisec_to_timestamp(deals[0].time_msc),
                                        close_time=millisec_to_timestamp(exit_deal.time_msc),
                                        close_price=exit_deal.price)

        except Exception as e:
            handle(e=e, msg=exception_msg)
            tc.roll_back()
        if reason_text(exit_deal.reason) == 'TP':
            dic = {'position_id': exit_deal.position_id,
                   'symbol': exit_deal.symbol,
                   'order_type': order_type_name(entry_deal.type),
                   'close_time': millisec_to_timestamp(exit_deal.time_msc),
                   'strat_id': strat_id_deal}
            return dic
        else:
            return None


def get_entry_exit_deals(position_id):
    init_mt5()
    deals = mt5.history_deals_get(position=position_id)
    entry_deal = None
    exit_deal = None
    if deals is not None and len(deals) > 0:
        for deal in deals:
            if deal.entry == mt5.DEAL_ENTRY_IN:
                entry_deal = deal
            elif deal.entry == mt5.DEAL_ENTRY_OUT:
                exit_deal = deal
    return entry_deal, exit_deal


def get_open_positions(symbol, signal, comment):
    init_mt5()
    positions = mt5.positions_get(symbol=symbol)
    posit_dict = dict()
    for position in positions:
        tp = TradePosition(position)
        if tp.type == OrderType.__getitem__(signal).value and tp.comment == comment:
            posit_dict[tp.ticket] = tp
    logging.debug(f"posit_dict: {posit_dict}")
    return posit_dict

# sync_trade_book()
