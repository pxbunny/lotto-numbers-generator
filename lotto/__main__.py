import importlib
import pkgutil
from types import ModuleType

from .cli import run_app


def run_modules_discovery(package: str) -> None:
    pkg: ModuleType = importlib.import_module(package)
    for _, modname, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
        importlib.import_module(modname)


if __name__ == '__main__':
    run_modules_discovery('lotto.algorithms')
    run_app()
