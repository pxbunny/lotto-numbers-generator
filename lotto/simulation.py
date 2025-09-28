import datetime
from typing import Iterator

from .algorithms.random_data import generate_numbers
from .models import GameHistoryRecord, GameType, LottoDrawRecord


class BacktestEngine:
    def __init__(self):
        self._history: list[GameHistoryRecord] = []

    @property
    def history(self) -> list[GameHistoryRecord]:
        return self._history

    def run(self, data: list[LottoDrawRecord], skip_plus: bool = False) -> list[GameHistoryRecord]:
        return list(self.results_gen(data, skip_plus))

    def results_gen(self, data: list[LottoDrawRecord], skip_plus: bool = False) -> Iterator[GameHistoryRecord]:
        self._history = []

        for record in data:
            generated_numbers = generate_numbers()

            use_lotto_numbers = True
            use_plus_numbers = not skip_plus

            datasets = [
                (use_lotto_numbers, GameType.LOTTO, record.lotto_numbers),
                (use_plus_numbers, GameType.LOTTO_PLUS, record.plus_numbers)
            ]

            for _, game_type, draw_result in [dataset for dataset in datasets if dataset[0]]:
                yield self._handle_game(record.draw_date, game_type, draw_result, generated_numbers)

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
