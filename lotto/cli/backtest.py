import typer

from ..data.api_mock import get_data
from ..simulation import BacktestEngine
from ..visualisation import visualise_results

app = typer.Typer()


@app.command(name='run')
def run_backtest(skip_plus: bool = False):
    backtest = BacktestEngine()
    data = get_data()
    backtest.run(data, skip_plus)
    visualise_results(backtest.history)
