from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class GameType(Enum):
    LOTTO = auto()
    LOTTO_PLUS = auto()


@dataclass
class GameHistoryRecord:
    # draw_system_id: int
    game_type: GameType
    draw_date: datetime
    draw_result: list[int]
    selected_numbers: list[int]
    number_of_matches: int
