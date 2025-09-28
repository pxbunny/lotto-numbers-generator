import pandas as pd


def get_data():
    df = pd.read_csv('lotto/data/data.csv')
    df['DrawDate'] = pd.to_datetime(df['DrawDate']).dt.date
    df.set_index('DrawDate', inplace=True)
    return df
