from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class GameType(Enum):
    LOTTO = auto()
    LOTTO_PLUS = auto()


@dataclass
class LottoDrawRecord:
    draw_date: datetime
    lotto_numbers: list[int]
    plus_numbers: list[int]


@dataclass
class GameRecord:
    game_type: GameType
    draw_date: datetime
    draw_result: list[int]
    generated_numbers: list[int]
    matches: int


class AbstractAlgorithm(ABC):
    def __init__(self, data: list[LottoDrawRecord], params: dict) -> None:
        self._data = data
        self._params = params

    @abstractmethod
    def generate_numbers(self) -> list[int]:
        raise NotImplementedError


class AlgorithmFactory:
    _registry: dict[str, tuple[type[AbstractAlgorithm], bool]] = {}

    def __init__(self, data: list[LottoDrawRecord] = []) -> None:
        self._data = data

    @classmethod
    def register(self, name: str, requires_data: bool = True) -> callable:
        def wrapper(algorithm_type: type[AbstractAlgorithm]) -> type[AbstractAlgorithm]:
            self._registry[name] = algorithm_type, requires_data
            return algorithm_type

        return wrapper

    @classmethod
    def requires_data(self, name: str) -> bool:
        _, requires_data = self._registry.get(name)
        return requires_data

    def select(self, name: str, params: dict) -> AbstractAlgorithm:
        algorythm_type, requires_data = self._registry.get(name)
        return algorythm_type(self._data, params) if requires_data else algorythm_type(params)
