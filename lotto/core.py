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
    POOL_MAX = 49
    TAKE = 6

    @abstractmethod
    def prepare_data(self, data: list[LottoDrawRecord]) -> None:
        raise NotImplementedError

    @abstractmethod
    def generate_numbers(self) -> list[int]:
        raise NotImplementedError


class StrategyRegistry:
    _registry: dict[str, tuple[type[AbstractStrategy], bool, bool]] = {}

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

    @classmethod
    def resolve(cls, name: str, params: dict) -> AbstractStrategy:
        strategy_type, _, has_params = cls._registry.get(name)
        return strategy_type(params) if has_params else strategy_type()
