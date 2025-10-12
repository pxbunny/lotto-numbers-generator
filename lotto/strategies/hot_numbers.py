from collections import Counter

from ..core import AbstractStrategy, LottoDrawRecord, StrategyRegistry

default_params: dict[str, str] = {
    'lookback': '100',
}


@StrategyRegistry.register('hot-numbers')
class HotNumbers(AbstractStrategy):
    def __init__(self, params: dict[str, str]) -> None:
        self._lookback = int(params.get('lookback', default_params['lookback']))
        self._data: list[LottoDrawRecord] = []

    def prepare_data(self, data: list[LottoDrawRecord]) -> None:
        self._data = data

    def generate_numbers(self) -> list[int]:
        draws = self._data[-self._lookback :] if self._lookback else self._data
        counter = Counter()

        for record in draws:
            counter.update([n for n in record.lotto_numbers if 1 <= n <= self.POOL_MAX])

        ranked = [n for n, _ in counter.most_common()]
        pool = list(range(1, self.POOL_MAX + 1))
        ranked += [n for n in pool if n not in ranked]

        pick = ranked[: self.TAKE]
        pick.sort()

        return pick
