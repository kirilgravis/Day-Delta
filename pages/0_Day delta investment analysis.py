import streamlit as st
import pandas as pd
from functions import *


with st.sidebar:
    st.write("The logic: If the current price is higher than it was a number"
             " of days ago, we buy the asset for another number of days. If it's lower,"
             " then we sell.")

st.write('## Day delta investment analysis')

ticker_symbols = ['SPY', 'QQQ', 'DIA']
selected_symbols = st.multiselect('Select the symbols:', ticker_symbols,
                                  default="SPY" if "SPY" in ticker_symbols else ticker_symbols)

# Place start date and end date selection in the same row
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input('Start date:', value=pd.to_datetime('1999-01-01'),
                               max_value=pd.to_datetime('2025-01-01'))

with col2:
    end_date = st.date_input('End date:', value=pd.to_datetime('2023-12-31'),
                             min_value=pd.to_datetime('1999-01-01'))

# Create a single row for sliders
col1, col2 = st.columns(2)
with col1:
    look_back_days = st.slider('Number of days to look back', min_value=1, max_value=30, value=1)

with col2:
    forward_days = st.slider('Number of days to look forward', min_value=1, max_value=30, value=1)
    column_name = f"Future {forward_days} days return"

data_frames = {}
for symbol in selected_symbols:
    data = pd.read_csv(f'./data/{symbol}.csv', index_col='Date')
    data.index = pd.to_datetime(data.index)
    data = data[(data.index.date >= start_date) & (data.index.date <= end_date)]
    data_frames[symbol] = data

# Data transformation with parameters
for symbol in selected_symbols:
    data_frames[symbol] = data_transformation(data_frames[symbol], forward_days, look_back_days)
    data_frames[symbol] = remove_intersections(data_frames[symbol], column_name, look_back_days, forward_days)
    data_frames[symbol]['Cumulative return'] = (data_frames[symbol][column_name] + 1).cumprod() - 1
    data_frames[symbol][column_name] *= 100

count = 0
for symbol in selected_symbols:
    with st.expander(f"Data for {symbol}"):

        part1, part2, part3, part4 = st.tabs(
            ["Cumulative price change graph", "Daily price change graph", "Summary", "Raw data"])
        with part1:
            # Plotting the 'Future {n} days return' column
            on = st.toggle('Include buy and hold strategy', value=False, key=f"{count}")
            if on:
                local_df = data_frames[symbol].copy()
                local_df['Buy and hold'] = local_df['Adj Close'].pct_change()
                local_df['Buy and hold'].iloc[0] = 0
                local_df['Buy and hold'] = (local_df['Buy and hold'] + 1).cumprod() - 1
                st.line_chart(local_df[['Cumulative return', "Buy and hold"]])
            else:
                st.line_chart(data_frames[symbol]['Cumulative return'])

        with part2:

            st.line_chart(data_frames[symbol][f"Future {forward_days} days return"])

        with part3:
            st.write(get_summary(data_frames[symbol], column_name))

        with part4:
            st.write(data_frames[symbol])

        # Displaying time range
        first_date = data_frames[symbol].index[0].strftime('%Y-%m-%d')
        last_date = data_frames[symbol].index[-1].strftime('%Y-%m-%d')
        st.write(f"Time Range: From {first_date} to {last_date}")
    count += 1
