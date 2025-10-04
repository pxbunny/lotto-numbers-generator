import math
import statistics
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from scipy.stats import chisquare

from .core import GameHistoryRecord, GameType


@dataclass
class BasicMetrics:
    total_draws: int
    hit_rate: float
    max_streak: int
    average_hits_per_bet: float
    match_distribution: dict[int, int]
    match_distribution_pct: dict[int, float]


@dataclass
class MonetaryMetrics:
    total_winnings: int
    total_cost: int
    net_profit: int
    roi_pct: float
    expected_value: float
    variance_of_returns: float
    max_drawdown: int
    winning_distribution: dict[int, int]


@dataclass
class StatisticalMetrics:
    coverage: int
    coverage_pct: float
    number_frequency: dict[int, int]
    chi_square_pvalue: float
    entropy: float
    average_sum: float
    sum_std_dev: float
    parity_distribution: dict[str, int]


@dataclass
class BacktestReport:
    basic_accuracy: BasicMetrics
    monetary_metrics: MonetaryMetrics
    statistical_quality: StatisticalMetrics


class MetricsCalculator:
    PRIZE_TABLES = {
        GameType.LOTTO: {1: 0, 2: 0, 3: 24, 4: 200, 5: 5000, 6: 2000000},
        GameType.LOTTO_PLUS: {1: 0, 2: 0, 3: 20, 4: 180, 5: 4500, 6: 1000000},
    }

    TICKET_COSTS = {GameType.LOTTO: 3.0, GameType.LOTTO_PLUS: 1.0}

    def __init__(self, records: Iterable[GameHistoryRecord]):
        self._lotto_records = [r for r in records if r.game_type == GameType.LOTTO]
        self._lotto_plus_records = [r for r in records if r.game_type == GameType.LOTTO_PLUS]

    def generate_report(self, game_type: GameType) -> BacktestReport:
        return BacktestReport(
            basic_accuracy=self.calculate_basic_metrics(game_type),
            monetary_metrics=self.calculate_monetary_metrics(game_type),
            statistical_quality=self.calculate_statistical_metrics(game_type),
        )

    def calculate_basic_metrics(self, game_type: GameType) -> BasicMetrics:
        records = self._get_records_for_game_type(game_type)
        matches = [r.matches for r in records]

        match_distribution = Counter(matches)
        total_draws = len(records)
        hit_rate = sum(1 for m in matches if m >= 1) / total_draws
        average_hits = statistics.mean(matches)
        max_streak = self._calculate_max_streak(matches, min_hits=1)

        return BasicMetrics(
            total_draws=total_draws,
            hit_rate=hit_rate,
            max_streak=max_streak,
            average_hits_per_bet=average_hits,
            match_distribution=match_distribution,
            match_distribution_pct={k: v / total_draws for k, v in match_distribution.items()},
        )

    def calculate_monetary_metrics(self, game_type: GameType) -> MonetaryMetrics:
        records = self._get_records_for_game_type(game_type)
        ticket_cost = self.TICKET_COSTS[game_type]

        total_cost = len(records) * ticket_cost
        winnings = []

        for record in records:
            prize_table = self.PRIZE_TABLES[record.game_type]
            win_amount = prize_table.get(record.matches, 0)
            winnings.append(win_amount)

        total_winnings = sum(winnings)
        net_profit = total_winnings - total_cost
        roi = (net_profit / total_cost) * 100 if total_cost > 0 else 0
        expected_value = statistics.mean(winnings) if winnings else 0
        variance = statistics.variance(winnings) if len(winnings) > 1 else 0
        win_streaks = [1 if w > 0 else 0 for w in winnings]
        max_drawdown = self._calculate_max_streak(win_streaks, min_hits=0)

        return MonetaryMetrics(
            total_winnings=total_winnings,
            total_cost=total_cost,
            net_profit=net_profit,
            roi_pct=roi,
            expected_value=expected_value,
            variance_of_returns=variance,
            max_drawdown=max_drawdown,
            winning_distribution=Counter(winnings),
        )

    def calculate_statistical_metrics(self, game_type: GameType) -> StatisticalMetrics:
        records = self._get_records_for_game_type(game_type)

        all_generated = []
        sum_metrics = []
        parity_metrics = []

        for record in records:
            numbers = record.generated_numbers
            all_generated.extend(numbers)
            sum_metrics.append(sum(numbers))
            even_count = sum(1 for n in numbers if n % 2 == 0)
            parity_metrics.append((even_count, 6 - even_count))

        coverage = len(set(all_generated))
        coverage_percentage = (coverage / 49) * 100
        number_frequency = Counter(all_generated)
        _, chi2_pvalue = self._chi_square_test(number_frequency)
        entropy = self._calculate_entropy(number_frequency)
        avg_sum = statistics.mean(sum_metrics)
        sum_std = statistics.stdev(sum_metrics) if len(sum_metrics) > 1 else 0
        parity_dist = Counter(parity_metrics)

        return StatisticalMetrics(
            coverage=coverage,
            coverage_pct=coverage_percentage,
            number_frequency=dict(number_frequency),
            chi_square_pvalue=chi2_pvalue,
            entropy=entropy,
            average_sum=avg_sum,
            sum_std_dev=sum_std,
            parity_distribution={f'{even}/{odd}': count for (even, odd), count in parity_dist.items()},
        )

    def _calculate_max_streak(self, matches: list[int], min_hits: int = 1) -> int:
        current_streak = 0
        max_streak = 0

        for match in matches:
            if match >= min_hits:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        return max_streak

    def _chi_square_test(self, frequency: Counter) -> tuple[float, float]:
        expected = sum(frequency.values()) / 49
        observed = [frequency.get(i, 0) for i in range(1, 50)]
        expected_list = [expected] * 49

        if expected > 0:
            chi2, p_value = chisquare(observed, expected_list)
            return chi2, p_value
        return 0, 1

    def _calculate_entropy(self, frequency: Counter) -> float:
        total = sum(frequency.values())
        if total == 0:
            return 0

        probabilities = [count / total for count in frequency.values()]
        entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        return entropy

    def _get_records_for_game_type(self, game_type: GameType) -> list[GameHistoryRecord]:
        return self._lotto_records if game_type == GameType.LOTTO else self._lotto_plus_records
