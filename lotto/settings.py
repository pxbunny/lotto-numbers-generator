import os
import sys
from dataclasses import dataclass, field, fields

import yaml

CONFIG_PATH = 'config.yaml'


@dataclass
class AppConfig:
    name: str = 'lotto'
    date_format: str = '%Y-%m-%d'


@dataclass
class ApiConfig:
    base_url: str = ''
    api_key: str = ''
    timeout: int = 30


@dataclass
class Config:
    app: AppConfig = field(default_factory=AppConfig)
    api: ApiConfig = field(default_factory=ApiConfig)


def load_config(filename: str = CONFIG_PATH) -> Config:
    if os.path.exists(filename):
        with open(filename, encoding='utf-8') as f:
            d = yaml.safe_load(f)
    else:
        file_path = os.path.abspath(os.path.dirname(sys.executable))
        file_path = os.path.join(file_path, filename)

        with open(file_path, encoding='utf-8') as f:
            d = yaml.safe_load(f)

    c = Config()

    for f in fields(Config):
        if f.name not in d:
            continue
        setattr(c, f.name, f.type(**d[f.name]))

    return c


config = load_config()
