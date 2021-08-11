class TradeRequest:

    def __init__(self,symbol, lot, order_type, position_id=None):
        self.symbol = symbol
        self.lot = lot
        self.position_id = position_id
        self.order_type = order_type