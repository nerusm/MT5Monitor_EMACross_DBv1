import MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.mt5_api.ema_cross_s1.ema_cross as ema


ema_cross = ema

def check_20ema_posit(symbol):

    print("06EMA: ",ema_cross.__get_ema__(symbol,(6*2)-2,16385).tail(1) )
    print("12EMA: ",ema_cross.__get_ema__(symbol,(12 * 2)-2,16385).tail(1) )
    print("50 SMMA: ",ema_cross.__get_ema__(symbol,(50 * 2)-2,16385).tail(1) )
    print("20 SMMA: ",ema_cross.__get_ema__(symbol,(20 ),16385).tail(1) )
    return None

check_20ema_posit('BRENT')