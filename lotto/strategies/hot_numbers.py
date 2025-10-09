from collections import Counter

from ..core import AbstractStrategy, StrategyRegistry


@StrategyRegistry.register('hot-numbers', requires_data=False)
class HotNumbers(AbstractStrategy):
    _POOL_MAX = 49
    _TAKE = 6

    def __init__(self, params: dict) -> None:
        super().__init__([], {})
        self._lookback = params.get('lookback')

    def generate_numbers(self) -> list[int]:
        draws = self._data[-self._lookback :] if self._lookback else self._data
        counter = Counter()

        for record in draws:
            counter.update([n for n in record.numbers if 1 <= n <= self._POOL_MAX])

        ranked = [n for n, _ in counter.most_common()]
        pool = list(range(1, self._POOL_MAX + 1))
        ranked += [n for n in pool if n not in ranked]

        pick = ranked[: self._TAKE]
        pick.sort()

        return pick
