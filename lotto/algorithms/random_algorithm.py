import random

from ..core import AbstractAlgorithm, AlgorithmFactory


@AlgorithmFactory.register('random', requires_data=False, has_params=False)
class RandomAlgorithm(AbstractAlgorithm):
    _POOL_MAX = 49
    _TAKE = 6

    def __init__(self) -> None:
        super().__init__([], {})

    def generate_numbers(self) -> list[int]:
        numbers = random.sample(range(1, self._POOL_MAX + 1), k=self._TAKE)
        numbers.sort()
        return numbers
