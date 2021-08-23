import MetaTrader5 as mt5
import logging
import sqlalchemy.dialects.mysql.mariadbconnector
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.db.db_trades_crud import TardesCrud

from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.mt5_api.ema_cross_s1.ema_cross import check_retrade
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.trade_wrapper import execute_trade_wrapper
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.update_trades import sync_trade_book
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.trade.exceptions import handle
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.configuration.app_config import config
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.utilities.utils import order_type_name, reason_text

# ema_cross = ema.EMA()
time_frame_dict = {15: 15, 30: 30, 60: 16385, 120: 16386, 180: 16387, 240: 16388}
comment = "EMA_ReTrade"
# comment = "EMA_ReTrade_T"
from_func="retrade.execute_retrades"

tc = TardesCrud()
engine = tc.get_connection(schema_name="trade_schema",from_func=from_func)


def execute_retrades():
    try:
        sync_trade_book()

        tc.create_session(schema_name="trade_schema", from_func=from_func, engine=engine)
        strat_id  =config['strat_id']
        retrades_list = tc.select_all_retrades_by_status_strat_id(strat_id=strat_id)
        print(f"Strat ID: {strat_id}")
        print(f"No of ReTrades: {len(retrades_list)}")
        pids = []
        trade_responses_dict = {}
        for retrade in retrades_list:
            position_id = retrade.position_id
            symbol = retrade.symbol
            order_type = retrade.order_type
            # print(f"config: {config}")

            retrade_dict = check_retrade(symbol=symbol,
                                         # time_frame=16385,
                                         time_frame= time_frame_dict.get( int(config['time_frame']) ),
                                         no_of_bars=config['no_of_bars'],
                                         ema_span=config['ema_spans'],
                                         signal=order_type,
                                         check_trend=config['check_trend_for_retrade'],
                                         lookback_stop_loss=int(config['lookback_stop_loss']))
            retrade_status = retrade_dict['can_retrade']
            stop_loss = retrade_dict['possible_stop_loss']

            logging.debug(f"Retrade Symbol: {symbol}, Status: {retrade_status}")
            if retrade_status:
                pids.append(position_id)
                trade_responses_dict[position_id] = execute_trade_wrapper(symbol=symbol,
                                                                          signal=order_type,
                                                                          stop_loss=stop_loss,
                                                                          parent_position_id=position_id,
                                                                          strat_id=config['strat_id'],
                                                                          usr_comment=f"{comment}_{config['strat_id']}")

            print(
                f"Retrade Symbol: {symbol}, Status: {retrade_status}, signal: {order_type}, stop loss: {stop_loss}")
        for parent_pid in trade_responses_dict:
            trade_response = trade_responses_dict.get(parent_pid)
            print(parent_pid)
            print(trade_response)
            print("------")
            tc.addNewTrade(position_id=trade_response.order,
                           symbol=trade_response.request.symbol,
                           order_type=order_type_name(trade_response.request.type),
                           price=trade_response.price,
                           magic=trade_response.request.magic, comment=trade_response.request.comment,
                           request_id=trade_response.request_id, is_open=True,
                           volume=trade_response.volume,
                           reason=reason_text(mt5.ORDER_REASON_EXPERT), parent_position_id=parent_pid,
                           strat_id=config['strat_id'])
        tc.update_retrade_status(position_ids=pids)
    except Exception as e:
        handle(e=e,msg="Exception while Retrading")
    finally:
        print(f"In Retrade.execute_retrades finally")
        tc.close_session()
        # conn.close()
        # print(conn.closed)
        # conn.invalidate()
        # tc.close_connection(from_func=from_func)




# execute_retrades()

# __get_rates__(symbol='GBPUSD',15,)
