import pandas as pd
import yfinance as yf

from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class MovingAverageCrossover(Strategy):
    short_window = 50
    long_window = 200

    def init(self):
        self.short_ma = self.I(lambda x: pd.Series(x).rolling(self.short_window).mean(), self.data.Close)
        self.long_ma = self.I(lambda x: pd.Series(x).rolling(self.long_window).mean(), self.data.Close)
    
    def next(self):
        if crossover(self.short_ma, self.long_ma):
            self.buy()
        elif crossover(self.long_ma, self.short_ma):
            self.sell()

def fetch_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df.reset_index(inplace=True)
    df.columns = df.columns.droplevel(1)

    return df

data = fetch_data('MSFT', '2015-01-01', '2023-01-01')

bt = Backtest(data, MovingAverageCrossover, cash=10000, commission=0.002)
stats = bt.run()

print(stats)

bt.plot()
