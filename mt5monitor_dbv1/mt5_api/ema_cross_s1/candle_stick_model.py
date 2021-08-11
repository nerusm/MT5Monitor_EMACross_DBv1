class CandleStick:
    time = None
    open = None
    close = None
    high = None
    low = None
    symbol = None

    def __init__(self, symbol, data):
        index = len(data)-2
        self.symbol = symbol
        self.open = data.loc[index].open
        self.high = data.loc[index].high
        self.low = data.loc[index].low
        self.close = data.loc[index].close
        self.time = data.loc[index].time