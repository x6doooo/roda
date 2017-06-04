import csv

from src.roda import *


# def random_change():
#     return 1 + random.uniform(-0.4, 0.4)
#
# def random_decrease_change():
#     return 1 + random.uniform(-0.4, 0)
#
# def random_increase_change():
#     return 1 + random.uniform(0, 0.4)
#
# def generate_day_price(peer_price):
#     open_price = peer_price * random_change()
#     high_price = open_price * random_increase_change()
#     low_price = open_price * random_decrease_change()
#     close_price = open_price * random_change()
#
#     if close_price > high_price:
#         high_price = close_price
#     if close_price < low_price:
#         low_price = close_price
#
#     return (open_price, high_price, low_price, close_price)

# class RandomDataProvider(DataProvider):
#     def __init__(self):
#         pass
#     def load_price_by_date(self, code, one_date):
#         pass
#     def load_price_by_date_range(self, code, start_date, end_date):
#         pass
#

def read_data_from_csv(name):
    file = open('test/data/' + name + '.csv')
    spam_reader = csv.reader(file)
    for row in spam_reader:
        print(row)

    file.close()

class MockDataProvider(DataProvider):
    def __init__(self):
        self.data_dict = {
            'AMD': None,
            'NVDA': None
        }
        for code, _ in self.data_dict:
            read_data_from_csv(code)

        pass
    def load_quote_by_date(self, code, one_date):
        pass
    def load_quotes_by_range(self, code, start_date, end_date):
        pass
    def load_previous_quotes(self, code, end_date, previous_num):
        pass
#
#
# def test_init():
#     o, h, l, c = generate_day_price(10)
#     print(o, h, l, c)