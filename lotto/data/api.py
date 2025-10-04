from datetime import datetime
from typing import Any

import requests

from ..models import LottoDrawRecord
from ..settings import config


def get_draw_results(date_from: str, date_to: str, top: int) -> list[LottoDrawRecord]:
    url = config.api.base_url
    url = url[:-1] if url.endswith('/') else url
    url = f"{url}/api/draw-results"

    timeout = config.api.timeout_sec

    headers = {
        'Accept': 'application/json',
        'x-functions-key': config.api.api_key
    }
    params = {
        'date_from': date_from,
        'date_to': date_to,
        'top': top
    }

    response = requests.get(url, params, headers=headers, timeout=timeout)
    response.raise_for_status()

    return [_map_record(record) for record in response.json()]


def _map_record(record: Any) -> LottoDrawRecord:
    return LottoDrawRecord(
        draw_date=datetime.strptime(record['draw_date'], '%Y-%m-%d').date(),
        lotto_numbers=record['lotto_numbers'],
        plus_numbers=record['plus_numbers']
    )
