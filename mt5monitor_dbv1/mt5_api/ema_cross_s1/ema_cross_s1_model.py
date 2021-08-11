class EmaCrossResult:
    strength = None
    closing_greater_20ema = None
    crossed_greater_20ema = None
    rsi_greater_50 = None
    sar_below = None
    signal = None
    symbol = None
    time = None

    def __str__(self):
        return f"\n" \
               f"\nTime: {self.time} \n" \
               f"Symbol: {self.symbol} \n" \
               f"Signal: {self.signal} \n" \
               f"Strength: {self.strength}\n" \
               f"Closing Price above 20EMA: {self.closing_greater_20ema} \n" \
               f"Crossed above 20EMA: {self.crossed_greater_20ema} \n" \
               f"RSI above 50: {self.rsi_greater_50} \n" \
               f"SAR below LOW: {self.sar_below} \n"

