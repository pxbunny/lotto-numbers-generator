import random

from ..core import AbstractAlgorithm, AlgorithmFactory


@AlgorithmFactory.register('random')
class RandomAlgorithm(AbstractAlgorithm):
    _POOL_MAX = 49
    _TAKE = 6

    def __init__(self, data: list = [], params: dict = {}) -> None:
        super().__init__(data, params)

    def generate_numbers(self) -> list[int]:
        numbers = random.sample(range(1, self._POOL_MAX + 1), k=self._TAKE)
        numbers.sort()
        return numbers
