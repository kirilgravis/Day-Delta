from yahoo_fin.stock_info import get_data
import streamlit as st
import pandas as pd

# Retrieving historical data for the given ticker symbol from Yahoo Finance
ticker = "AAPL"  # Ticker symbol for Apple Inc.
start_date = "2023-01-01"
end_date = "2023-12-31"

historical_data = get_data(ticker, start_date, end_date)

# Displaying the retrieved data
historical_data.head()
st.write(historical_data.head())