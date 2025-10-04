from datetime import datetime

from .settings import config


def is_date_str_valid(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, config.app.date_format)
        return True
    except ValueError:
        return False
