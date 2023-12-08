import streamlit as st
import yfinance as yf
import pandas as pd


def calculate_adjusted_ratio(data, n, x):
    column_name = f"Future {n} days return"
    data[column_name] = 0  # Initialize Future {n} days return column with zeros
    for i in range(len(data)):
        if i + n < len(data):
            if data['Adj Close'][i] < data['Adj Close'][i - x]:
                data.at[data.index[i], column_name] = ((data['Adj Close'][i + n] / data['Adj Close'][i]) - 1) * -100
            elif data['Adj Close'][i] > data['Adj Close'][i - x]:
                data.at[data.index[i], column_name] = ((data['Adj Close'][i + n] / data['Adj Close'][i]) - 1) * 100
    # data = data[data[column_name] != 0]  # Remove rows where Future {n} days return is still zero
    return data


st.title('Day delta investment analysis')

ticker_symbols = ['SPY', 'QQQ', 'DIA']
selected_symbols = st.multiselect('Select stock symbols:', ticker_symbols, default=ticker_symbols)

n = st.slider('Number of days to look forward (x):', min_value=1, max_value=30, value=1)
x = st.slider('Number of days to look back (x):', min_value=1, max_value=30, value=1)

start_date = st.date_input('Select start date:', value=pd.to_datetime('1999-01-01'))
end_date = st.date_input('Select end date:', value=pd.to_datetime('2023-12-31'))

data_frames = {}
for symbol in selected_symbols:
    data = yf.download(symbol, start=start_date, end=end_date)
    data = calculate_adjusted_ratio(data, n, x)
    data_frames[symbol] = data

for symbol in selected_symbols:
    st.write(f"Data for {symbol}:")
    st.write(data_frames[symbol].head(10))
