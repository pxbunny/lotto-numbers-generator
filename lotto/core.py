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


class AbstractStrategy(ABC):
    def __init__(self, data: list[LottoDrawRecord], params: dict) -> None:
        self._data = data
        self._params = params

    @abstractmethod
    def generate_numbers(self) -> list[int]:
        raise NotImplementedError


class StrategyRegistry:
    _registry: dict[str, tuple[type[AbstractStrategy], bool, bool]] = {}

    def __init__(self, data: list[LottoDrawRecord] | None = None) -> None:
        self._data = data if data is not None else []

    @classmethod
    def register(cls, name: str, *, requires_data: bool = True, has_params: bool = True) -> callable:
        def wrapper(strategy_type: type[AbstractStrategy]) -> type[AbstractStrategy]:
            cls._registry[name] = strategy_type, requires_data, has_params
            return strategy_type

        return wrapper

    @classmethod
    def requires_data(cls, name: str) -> bool:
        _, requires_data, _ = cls._registry.get(name)
        return requires_data

    def resolve(self, name: str, params: dict) -> AbstractStrategy:
        strategy_type, requires_data, has_params = self._registry.get(name)

        match (requires_data, has_params):
            case (True, True):
                return strategy_type(self._data, params)
            case (True, False):
                return strategy_type(self._data)
            case (False, True):
                return strategy_type(params)
            case (False, False):
                return strategy_type()
