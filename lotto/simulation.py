from typing import Iterator
import pandas as pd

from .algorithms.random_data import generate_numbers
from .models import GameHistoryRecord, GameType


class BacktestEngine:
    def __init__(self):
        self._history: list[GameHistoryRecord] = []

    @property
    def history(self) -> list[GameHistoryRecord]:
        return self._history

    def run(self, data: pd.DataFrame) -> Iterator[GameHistoryRecord]:
        for index, row in data.iterrows():
            generated_numbers = generate_numbers()

            new_record = GameHistoryRecord(
                game_type=GameType.LOTTO,
                draw_date=index,
                draw_result=list(map(int, row['LottoNumbers'].split(','))),
                selected_numbers=generated_numbers,
                number_of_matches=1
            )

            self._history.append(new_record)
            yield new_record
