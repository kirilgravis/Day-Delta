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
    return data


def remove_intersections(df, column_name, back, forward):
    # Generate the sequence based on index positions
    sequence = []
    value = back
    while value < len(df):
        sequence.append(value)
        value += forward

    # Modify the specified column based on index positions
    new_column = [0] * len(df)
    for i in sequence:
        new_column[i] = df[column_name][i]

    # Update the specified column with the modified values
    df[column_name] = new_column

    return df


def get_summary(df, column_name):
    summary = {'Total wins: ': len(df[df[column_name] > 0]),
               'Total losses: ': len(df[df[column_name] < 0]),
               'Ratio: ': f'{round(len(df[df[column_name] > 0]) / len(df[df[column_name] != 0]), 3)*100}%',
               'Average: ': df[df[column_name] != 0][column_name].mean(),
               'Median: ': df[df[column_name] != 0][column_name].median(),
               'Biggest DrawDown: ': df[column_name].min(),
               'Biggest Win: ': df[column_name].max()
               }
    summary_df = pd.DataFrame(list(summary.items()), columns=['Metric', 'Value']).set_index('Metric')
    return summary_df