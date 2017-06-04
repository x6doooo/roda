from .Context import *

def run(StrategyWillBeBackTest, data_provider, start_date, end_date):

    ctx = Context(None, data_provider)
    strategy = StrategyWillBeBackTest(ctx)

    benchmark_data = data_provider.load_quote_by_date_range(ctx.benchmark, start_date, end_date)

    pass