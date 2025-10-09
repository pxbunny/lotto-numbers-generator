import datetime
from collections.abc import Iterator

from .core import AbstractStrategy, GameRecord, GameType, LottoDrawRecord


class BacktestEngine:
    def __init__(self, strategy: AbstractStrategy) -> None:
        self._history: list[GameRecord] = []
        self._strategy = strategy

    @property
    def history(self) -> list[GameRecord]:
        return self._history

    def run(self, data: list[LottoDrawRecord]) -> list[GameRecord]:
        return list(self.results_gen(data))

    def results_gen(self, data: list[LottoDrawRecord]) -> Iterator[GameRecord]:
        self._history = []

        for record in data:
            generated_numbers = self._strategy.generate_numbers()

            datasets = [
                (GameType.LOTTO, record.lotto_numbers),
                (GameType.LOTTO_PLUS, record.plus_numbers),
            ]

            for game_type, draw_result in datasets:
                yield self._handle_game(record.draw_date, game_type, draw_result, generated_numbers)

    def _handle_game(
        self,
        draw_date: datetime.date,
        game_type: GameType,
        draw_result: list[int],
        generated_numbers: list[int] | None = None,
    ) -> GameRecord:
        generated_numbers = generated_numbers or self._strategy.generate_numbers()
        matches = self._count_matches(draw_result, generated_numbers)

        new_record = GameRecord(
            game_type=game_type,
            draw_date=draw_date,
            draw_result=draw_result,
            generated_numbers=generated_numbers,
            matches=matches,
        )

        self._history.append(new_record)
        return new_record

    def _count_matches(self, draw_result: list[int], generated_numbers: list[int]) -> int:
        return len(set(draw_result) & set(generated_numbers))
