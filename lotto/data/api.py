from datetime import datetime
from typing import Any

import requests

from ..models import LottoDrawRecord
from .config import TIMEOUT_SECONDS, URL


def get_data() -> list[LottoDrawRecord]:
    params = {
        'dateFrom': '2015-01-01',
    }
    response = requests.get(URL, params=params, timeout=TIMEOUT_SECONDS)
    return [_map_data(record) for record in response.json()]


def _map_data(record: Any) -> LottoDrawRecord:
    return LottoDrawRecord(
        draw_date=datetime.strptime(record['draw_date'], '%Y-%m-%d').date(),
        lotto_numbers=record['lotto_numbers'],
        plus_numbers=record['plus_numbers']
    )
