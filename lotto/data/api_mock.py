import pandas as pd

from ..models import LottoDrawRecord


def get_data() -> list[LottoDrawRecord]:
    df = pd.read_csv('lotto/data/data.csv')

    dates = pd.to_datetime(df['DrawDate']).dt.date
    lotto_numbers = df['LottoNumbers'].apply(lambda x: list(map(int, x.split(','))))
    plus_numbers = df['PlusNumbers'].apply(lambda x: list(map(int, x.split(','))))

    return [LottoDrawRecord(date, lotto, plus) for date, lotto, plus in zip(dates, lotto_numbers, plus_numbers)]
