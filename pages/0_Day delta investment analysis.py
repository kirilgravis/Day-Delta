import streamlit as st
import pandas as pd


def data_transformation(data, forward_days, look_back_days):
    data = data[['Adj Close']]
    column_name = f"Future {forward_days} days return"
    data[column_name] = 0  # Initialize Future {forward_days} days return column with zeros
    for i in range(len(data)):
        if i + forward_days < len(data):
            if data['Adj Close'][i] < data['Adj Close'][i - look_back_days]:
                data.at[data.index[i], column_name] = ((data['Adj Close'][i] / data['Adj Close'][i + forward_days]) - 1)
            elif data['Adj Close'][i] > data['Adj Close'][i - look_back_days]:
                data.at[data.index[i], column_name] = ((data['Adj Close'][i + forward_days] / data['Adj Close'][i]) - 1)
    data['Cumulative return'] = (data[column_name] + 1).cumprod() - 1
    data[column_name] *= 100
    return data


def get_summary(df, column_name):
    summary = {'Total wins: ': len(df[df[column_name] > 0]),
               'Total losses: ': len(df[df[column_name] < 0]),
               'Ratio: ': f'{round(len(df[df[column_name] > 0]) / len(df), 3)*100}%',
               'Average: ': df[column_name].mean(),
               'Median: ': df[column_name].median(),
               'Biggest DrawDown: ': df[column_name].min(),
               'Biggest Win: ': df[column_name].max()
               }
    summary_df = pd.DataFrame(list(summary.items()), columns=['Metric', 'Value']).set_index('Metric')
    return summary_df


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

data_frames = {}
for symbol in selected_symbols:
    data = pd.read_csv(f'./data/{symbol}.csv', index_col='Date')
    data.index = pd.to_datetime(data.index)
    data = data[(data.index.date >= start_date) & (data.index.date <= end_date)]
    data_frames[symbol] = data

for symbol in selected_symbols:
    data_frames[symbol] = data_transformation(data_frames[symbol], forward_days, look_back_days)

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
            column_name = f"Future {forward_days} days return"
            st.write(get_summary(data_frames[symbol], column_name))

        with part4:
            st.write(data_frames[symbol])

        # Displaying time range
        first_date = data_frames[symbol].index[0].strftime('%Y-%m-%d')
        last_date = data_frames[symbol].index[-1].strftime('%Y-%m-%d')
        st.write(f"Time Range: From {first_date} to {last_date}")
    count += 1
