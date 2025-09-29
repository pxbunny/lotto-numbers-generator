import typer

from .cli import backtest

if __name__ == '__main__':
    app = typer.Typer(add_completion=False)
    app.add_typer(backtest.app, name='backtest')
    app()
