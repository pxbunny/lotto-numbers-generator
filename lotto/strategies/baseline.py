import random

from ..core import AbstractStrategy, LottoDrawRecord, StrategyMetadata, StrategyRegistry

_metadata = StrategyMetadata(
    requires_data=False,
    has_params=False,
)


@StrategyRegistry.register('baseline', _metadata)
class Baseline(AbstractStrategy):
    def prepare_data(self, _: list[LottoDrawRecord]) -> None:
        pass

    def generate_numbers(self) -> list[int]:
        numbers = random.sample(range(1, self.POOL_MAX + 1), k=self.TAKE)
        numbers.sort()
        return numbers
