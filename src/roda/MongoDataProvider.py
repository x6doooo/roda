from .abstracts import *
from pymongo import MongoClient
import numpy as np
from collections import namedtuple


fields = ['date', 'open', 'high', 'low', 'close', 'volume']
Quote = namedtuple('quote', fields)

def format_aggr_result_to_ndarray(res):
    data = {}
    for item in res:
        for f in fields:
            if f not in data:
                data[f] = []
            data[f].append(item[f])
    res = {}
    for k, item in data.items():
        res[k] = np.array(item)
    return res


class MongoDataProvider(DataProvider):
    def __init__(self, conf):
        uri = 'mongodb://%s:%s@%s' % (conf['username'],
                                      conf['password'],
                                      conf['host'])
        self.db = MongoClient(uri)[conf['database']]
        self.data_dict = {}

    def preload(self, codes, start_date, end_date):
        condition = {
            'date': {
                '$gte': start_date,
                '$lte': end_date
            }
        }
        for code in codes:
            data = self._db_load(code, condition)
            self.data_dict[code] = data

    def _db_load(self, code, condition):
        res = self.db['code_' + code + '_daily'].find(condition)
        return format_aggr_result_to_ndarray(res)

    def find_date_idx(self, code, date):
        code_data = self.data_dict[code]
        idx, = np.where(code_data['date'] == date)
        idx = idx[0]
        return idx

    def quote_range(self, code, idx_start, idx_end):
        data = self.data_dict[code]
        args = []
        for f in fields:
            args.append(data[f][idx_start:idx_end])
        return Quote(*args)

    def load_quote_by_date(self, code, one_date):
        idx = self.find_date_idx(code, one_date)
        return self.quote_range(code, idx, idx + 1)

    def load_quotes_by_range(self, code, start_date, end_date):
        idx_start = self.find_date_idx(code, start_date)
        idx_end = self.find_date_idx(code, end_date) + 1
        return self.quote_range(code, idx_start, idx_end)

    def load_previous_quotes(self, code, end_date, previous_num):
        idx_end = self.find_date_idx(code, end_date) + 1
        idx_start = idx_end - previous_num
        return self.quote_range(code, idx_start, idx_end)

    def load_next_quotes(self, code, start_date, next_num):
        idx_start = self.find_date_idx(code, start_date)
        idx_end = idx_start + next_num
        return self.quote_range(code, idx_start, idx_end)


