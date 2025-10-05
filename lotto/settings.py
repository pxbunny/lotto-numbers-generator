import json
from dataclasses import dataclass, field, fields

CONFIG_PATH = 'config.json'


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


def load_config(path: str = CONFIG_PATH) -> Config:
    with open(path, encoding='utf-8') as f:
        d = json.load(f)

    c = Config()

    for f in fields(Config):
        if f.name not in d:
            continue
        setattr(c, f.name, f.type(**d[f.name]))

    return c


config = load_config()
