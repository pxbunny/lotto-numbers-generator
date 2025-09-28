from .data.api_mock import get_data
from .simulation import BacktestEngine


if __name__ == '__main__':
    backtest = BacktestEngine()
    data = get_data()
    history = backtest.run(data)

    for record in history:
        print(record)
