import datetime
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

    def run(
        self,
        data: pd.DataFrame,
        use_lotto_numbers: bool = True,
        use_plus_numbers: bool = True
    ) -> Iterator[GameHistoryRecord]:
        for index, row in data.iterrows():
            generated_numbers = generate_numbers()

            datasets = [
                (use_lotto_numbers, GameType.LOTTO, row['LottoNumbers']),
                (use_plus_numbers, GameType.LOTTO_PLUS, row['PlusNumbers'])
            ]

            for _, game_type, draw_result in [dataset for dataset in datasets if dataset[0]]:
                yield self._handle_game(index, game_type, draw_result, generated_numbers)

    def _handle_game(
        self,
        draw_date: datetime.date,
        game_type: GameType,
        draw_result: list[int],
        generated_numbers: list[int] | None = None
    ) -> GameHistoryRecord:
        generated_numbers = generated_numbers or generate_numbers()
        matches = self._count_matches(draw_result, generated_numbers)

        new_record = GameHistoryRecord(
            game_type,
            draw_date,
            draw_result,
            generated_numbers,
            matches
        )

        self._history.append(new_record)
        return new_record

    def _count_matches(self, draw_result: list[int], generated_numbers: list[int]) -> int:
        return len(set(draw_result) & set(generated_numbers))
