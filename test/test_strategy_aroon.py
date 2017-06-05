import talib

class StrategyAroon:
    def __init__(self, context):
        context.code = 'AMD'
        context.benchmark = 'NVDA'

    def handle_bar(self, context):
        period = 14
        data = context.load_data(context.code, limit=100)

        downs, ups = talib.AROON(data['high'], data['low'], period)

        current_price = data['close'][-1]

        the_last_up = ups[-1]
        the_last_down = downs[-1]

        if the_last_up > the_last_down:
            context.buy(context.code, current_price)
        if the_last_up < the_last_down:
            context.sell(context.code, current_price)