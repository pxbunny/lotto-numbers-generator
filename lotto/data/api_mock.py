import pandas as pd


def get_data():
    df = pd.read_csv('lotto/data/data.csv')

    df['DrawDate'] = pd.to_datetime(df['DrawDate']).dt.date
    df.set_index('DrawDate', inplace=True)

    df['LottoNumbers'] = df['LottoNumbers'].apply(lambda x: list(map(int, x.split(','))))
    df['PlusNumbers'] = df['PlusNumbers'].apply(lambda x: list(map(int, x.split(','))))

    return df
