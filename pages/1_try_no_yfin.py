# import streamlit as st
# # import yfinance as yf
# import pandas as pd
# import numpy as np
#
#
# def calculate_adjusted_ratio(data, n):
#     data['Return'] = data['Adj Close'] / data['Adj Close'].shift(n)
#     data = data.dropna(subset=['Return'])  # Drop rows with NaN in the 'Return' column
#     return data
#
# st.title('Stock Data Analysis with Adjusted Ratio')
#
# ticker_symbols = ['SPY', 'QQQ', 'DIA']
# selected_symbols = st.multiselect('Select stock symbols:', ticker_symbols, default=ticker_symbols)
#
# n = st.slider('Select the value of n for adjusted ratio calculation:', min_value=1, max_value=30, value=5)
#
# start_date = st.date_input('Select start date:', value=pd.to_datetime('1999-01-01'))
# end_date = st.date_input('Select end date:', value=pd.to_datetime('2023-12-31'))
#
# data_frames = {}
# for symbol in selected_symbols:
#     # data = yf.download(symbol, start=start_date, end=end_date)
#     data = pd.DataFrame({'Adj Close': np.random.randint(50, 200, size=11)},
#                         index=range(1, 12))
#     data = calculate_adjusted_ratio(data, n)
#     data_frames[symbol] = data
#
# for symbol in selected_symbols:
#     st.write(f"Data for {symbol}:")
#     st.write(data_frames[symbol].head())
