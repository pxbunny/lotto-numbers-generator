import typer

from ..data.api import get_data
from ..simulation import BacktestEngine
from ..visualisation import visualise_results

app = typer.Typer()


@app.command(name='run')
def run_backtest(skip_plus: bool = False):
    backtest = BacktestEngine()
    data = get_data()
    backtest.run(data, skip_plus)

    # metrics_calculator = MetricsCalculator(backtest.history)
    # lotto_metrics = metrics_calculator.generate_report(GameType.LOTTO)
    # lotto_plus_metrics = metrics_calculator.generate_report(GameType.LOTTO_PLUS)

    # print(f'Basic metrics for Lotto: {lotto_metrics.basic_accuracy}')
    # print(f'Basic metrics for Lotto Plus: {lotto_plus_metrics.basic_accuracy}')

    # print(f'Monetary metrics for Lotto: {lotto_metrics.monetary_metrics}')
    # print(f'Monetary metrics for Lotto Plus: {lotto_plus_metrics.monetary_metrics}')

    # print(f'Statistical quality metrics for Lotto: {lotto_metrics.statistical_quality}')
    # print(f'Statistical quality metrics for Lotto Plus: {lotto_plus_metrics.statistical_quality}')

    visualise_results(backtest.history)
