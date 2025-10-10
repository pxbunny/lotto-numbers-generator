from datetime import datetime
from functools import reduce
from typing import Annotated

import typer
from rich.columns import Columns
from rich.console import Console
from rich.progress import track
from rich.style import Style
from rich.table import Table

from . import lotto_client
from .core import GameType, StrategyRegistry
from .metrics import BacktestReport, MetricsCalculator
from .settings import config
from .simulation import BacktestEngine
from .visualisation import visualise_results

_app = typer.Typer(name=config.app.name, add_completion=False, no_args_is_help=True)
_console = Console()

_spinner_type = 'arc'
_spinner_style = Style(color='bright_cyan', bold=True)


def _is_date_str_valid(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, config.app.date_format)
        return True
    except ValueError:
        return False


def _validate_date_options(date_from: str | None, date_to: str | None) -> None:
    if date_from and not _is_date_str_valid(date_from):
        raise typer.BadParameter(f'Invalid date format for --date-from. Expected format: {config.app.date_format}')
    if date_to and not _is_date_str_valid(date_to):
        raise typer.BadParameter(f'Invalid date format for --date-to. Expected format: {config.app.date_format}')


def _parse_params(params: str | None) -> dict[str, str]:
    if params is None:
        return {}

    return dict(param_item.split('=', 1) for param_item in params)


def _get_metrics_table(title: str, report: BacktestReport) -> Table:
    table = Table(title=title)
    table.add_column('Metric', style='cyan', no_wrap=True)
    table.add_column('Value', style='magenta', justify='right')

    ba = report.basic_accuracy

    table.add_row('total_draws', f'{ba.total_draws:.2f}')
    table.add_row('hit_rate', f'{ba.hit_rate:.2f}')
    table.add_row('max_streak', f'{ba.max_streak:.2f}')
    table.add_row('average_hits_per_bet', f'{ba.average_hits_per_bet:.2f}')
    table.add_section()

    mm = report.monetary_metrics

    table.add_row('total_winnings', f'{mm.total_winnings:.2f}')
    table.add_row('total_cost', f'{mm.total_cost:.2f}')
    table.add_row('net_profit', f'{mm.net_profit:.2f}')
    table.add_row('roi_pct', f'{mm.roi_pct:.2f}')
    table.add_row('expected_value', f'{mm.expected_value:.2f}')
    table.add_row('variance_of_returns', f'{mm.variance_of_returns:.2f}')
    table.add_row('max_drawdown', f'{mm.max_drawdown:.2f}')
    table.add_section()

    sq = report.statistical_quality

    table.add_row('coverage', f'{sq.coverage:.2f}')
    table.add_row('coverage_pct', f'{sq.coverage_pct:.2f}')
    table.add_row('chi_square_pvalue', f'{sq.chi_square_pvalue:.2f}')
    table.add_row('entropy', f'{sq.entropy:.2f}')
    table.add_row('average_sum', f'{sq.average_sum:.2f}')
    table.add_row('sum_std_dev', f'{sq.sum_std_dev:.2f}')

    return table


@_app.command()
def run_backtest(
    strategy: Annotated[str, typer.Option('--strategy', '-s')],
    param: Annotated[list[str] | None, typer.Option('--param', '-p')] = None,
    date_from: Annotated[str | None, typer.Option('--date-from')] = None,
    date_to: Annotated[str | None, typer.Option('--date-to')] = None,
    top: Annotated[int | None, typer.Option('--top', min=1)] = None,
) -> None:
    _validate_date_options(date_from, date_to)

    with _console.status('Fetching data', spinner=_spinner_type, spinner_style=_spinner_style):
        data = lotto_client.get_draw_results(date_from, date_to, top)

    params = _parse_params(param)
    strategy = StrategyRegistry.resolve(strategy, params)
    backtest = BacktestEngine(strategy)

    results_iterator = backtest.results_gen(data)
    total_games = reduce(lambda x, y: x + (2 if y.plus_numbers else 1), data, 0)
    results = []

    for result in track(results_iterator, 'Backtest', total_games, console=_console):
        results.append(result)

    metrics_calculator = MetricsCalculator(backtest.history)
    lotto_metrics = metrics_calculator.generate_report(GameType.LOTTO)
    lotto_plus_metrics = metrics_calculator.generate_report(GameType.LOTTO_PLUS)

    lotto_table = _get_metrics_table('Lotto - metrics', lotto_metrics)
    lotto_plus_table = _get_metrics_table('Lotto Plus - metrics', lotto_plus_metrics)

    _console.print()
    _console.print(Columns([lotto_table, lotto_plus_table]))
    _console.print()

    visualise_results(results)


@_app.command()
def generate_numbers(
    strategy: Annotated[str, typer.Option('--strategy', '-s')],
    param: Annotated[list[str] | None, typer.Option('--param', '-p')] = None,
    date_from: Annotated[str | None, typer.Option('--date-from')] = None,
    date_to: Annotated[str | None, typer.Option('--date-to')] = None,
    top: Annotated[int, typer.Option('--top', min=1)] = 100,
) -> None:
    _validate_date_options(date_from, date_to)

    params = _parse_params(param)
    requires_data = StrategyRegistry.requires_data(strategy)

    if requires_data:
        with _console.status('Fetching data', spinner=_spinner_type, spinner_style=_spinner_style):
            data = lotto_client.get_draw_results(date_from, date_to, top)
    else:
        data = []

    strategy = StrategyRegistry.resolve(strategy, params)
    strategy.prepare_data(data)
    numbers = strategy.generate_numbers()

    _console.print(f'Generated numbers: [bold green]{", ".join(map(str, numbers))}[/]')


def run_typer_app() -> None:
    _app()
