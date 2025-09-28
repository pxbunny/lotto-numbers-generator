from .data.api_mock import get_data
from .simulation import BacktestEngine
from .visualisation import visualise_results

if __name__ == '__main__':
    backtest = BacktestEngine()
    data = get_data()
    backtest.run(data)
    visualise_results(backtest.history)
