import yfinance as yf
import pandas as pd

ticker_symbols = ['SPY', 'QQQ', 'DIA']

for symbol in ticker_symbols:
    data = yf.download(symbol, start=pd.to_datetime('1999-01-01'),
                       end=pd.to_datetime('2024-5-31'))
    data.to_csv(f'data/{symbol}.csv')

