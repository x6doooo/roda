import math
from collections import namedtuple

StoreRecord = namedtuple('StoreRecord', ['price', 'volume', 'position'])
DealRecord = namedtuple('DealRecord', ['code', 'price', 'volume', 'date', 'op'])
RateRecord = namedtuple('RateRecord', ['date', 'value'])

class Context:

    def __init__(self, benchmark, data_provider, init_cash = 1000 * 1000):
        # 数据接口类，实现DataProvider类的接口方法
        self.data_provider = data_provider
        # 当前日期，context会被放入run函数中循环一个时间段，current_date字段会被赋值为当前时间
        self.current_date = None

        # 初始现金，用于计算受益
        self.init_cash = init_cash
        # 现金，用于交易
        self.cash = init_cash

        # 参照股，用于对比受益率
        self.benchmark = benchmark
        # 参照股的初始价值，用于计算参照收益率
        self.benchmark_init_value = None

        # 交易记录
        self.deals = []
        # 持仓
        self.store = {}
        # 每天的收益率
        self.rate_daily = []
        # 参照股的每天收益率
        self.benchmark_rate_daily = []

    def order(self, code, position, price):

        # 有持仓取出持仓，无持仓设为空持仓
        if code in self.store:
            record = self.store[code]
        else:
            record = StoreRecord(code, 0, 0)

        diff_position = position - record.position
        # 当前仓位等于目标仓位，不操作
        if diff_position == 0:
            return

        # 仓位需要增加
        if diff_position > 0:
            self.__buy(code, record, position, price)
            return

        self.__sell(code, record, position, price)

    def __sell(self, record, code, position, price):
        diff_position = position - record.position

        # 清仓
        if position == 0:
            income = price * record.volume
            self.cash += income
            self.store.pop(code, None)
            op_volume = record.volume
        else:
            # 目标仓位小 -> 卖出
            # 如果是空持仓不会进行到这一步 所以不用担心record.position为0
            sell_volume = round(record.volume / record.position * diff_position, 0)
            income = price * sell_volume
            self.cash += income
            new_volume = record.volume - sell_volume
            real_position = new_volume * record.price / self.init_cash
            op_volume = new_volume
            self.store[code] = StoreRecord(record.price, new_volume, real_position)

        deal = DealRecord(code, price, op_volume, self.current_date, 'sell')
        self.deals.append(deal)


    def __buy(self, record, code, position, price):
        # 目标仓位大 ->
        # 当前可用仓位： 现金 / 原始资本
        valid_position = self.cash / self.init_cash
        # 可用仓位不够用 -> 跳出

        diff_position = position - record.position

        # 目标仓位大于可用仓位   退出
        if diff_position > valid_position:
            return

        # 仓位够用 -> 买入
        buy_volume = diff_position * self.init_cash / price

        # 如果可买不足1股 -> 退出
        if buy_volume < 1:
            return

        cost = price * buy_volume
        new_volume = record.volume + buy_volume

        self.cash -= cost
        avg_price = (record.price * record.volume + cost) / new_volume
        self.store[code] = StoreRecord(avg_price, new_volume, position)
        deal = (code, price, buy_volume, self.current_date, 'buy')
        self.deals.append(deal)


    def count_value(self):
        '''
        统计当前资本收益率
        :return: None
        '''
        value = self.cash
        for code in list(self.store.keys()):
            quote = self.data_provider.load_quote_by_date(code, self.current_date)
            value += quote.close * self.store[code].volume
        self.rate_daily.append(RateRecord(self.current_date, value / self.init_cash))


    def count_benchmark_value(self):
        '''
        统计当前benchmark的收益率
        :return: None
        '''
        quote = self.data_provider.load_quote_by_date(self.benchmark, self.current_date)

        # 没有初始值的时候，以当前值初始化一下
        if self.benchmark_init_value is None:
            self.benchmark_init_value = quote.close

        self.benchmark_rate_daily.append(RateRecord(self.current_date, quote.close / self.benchmark_init_value))

