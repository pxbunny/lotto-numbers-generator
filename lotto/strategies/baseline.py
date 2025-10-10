import random

from ..core import AbstractStrategy, LottoDrawRecord, StrategyRegistry


@StrategyRegistry.register('baseline', requires_data=False, has_params=False)
class Baseline(AbstractStrategy):
    def prepare_data(self, _: list[LottoDrawRecord]) -> None:
        pass

    def generate_numbers(self) -> list[int]:
        numbers = random.sample(range(1, self.POOL_MAX + 1), k=self.TAKE)
        numbers.sort()
        return numbers
