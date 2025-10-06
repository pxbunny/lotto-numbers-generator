from datetime import datetime
from typing import TypedDict, cast

import requests

from .core import LottoDrawRecord
from .settings import config


class RawLottoDrawRecord(TypedDict):
    draw_date: str
    lotto_numbers: list[int]
    plus_numbers: list[int]


def get_draw_results(date_from: str | None, date_to: str | None, top: int | None) -> list[LottoDrawRecord]:
    url = _build_url('/api/draw-results')

    headers = {'Accept': 'application/json', 'x-functions-key': config.api.api_key}

    params = {'dateFrom': date_from, 'dateTo': date_to, 'top': top}
    params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(url, params=params, headers=headers, timeout=config.api.timeout)
    response.raise_for_status()

    body = cast('list[RawLottoDrawRecord]', response.json())
    return [_map_record(record) for record in body]


def _map_record(record: RawLottoDrawRecord) -> LottoDrawRecord:
    return LottoDrawRecord(
        draw_date=datetime.strptime(record['draw_date'], config.app.date_format).date(),
        lotto_numbers=record['lotto_numbers'],
        plus_numbers=record['plus_numbers'],
    )


def _build_url(path: str) -> str:
    url = config.api.base_url
    url = url[:-1] if url.endswith('/') else url
    return f'{url}/{path.lstrip("/")}'
