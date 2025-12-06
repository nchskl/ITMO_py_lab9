from typing import Any, List, Optional
import requests
import functools
import logging
import sys

logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('main.log', encoding='utf-8')
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)

def logger_using(func=None, *, handle=sys.stdout):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info('Calling %s args=%s kwargs=%s', func.__name__, args, kwargs)
        try:
            res = func(*args, **kwargs)
            logger.info('%s finished, result len=%s', func.__name__, len(res) if hasattr(res, '__len__') else res)
            return res
        except Exception as e:
            logger.exception('%s raised %s', func.__name__, e)
            raise
    return wrapper

@logger_using
def get_currencies(currency_codes: Optional[List[str]] = None,
                   url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> List[dict]:
    """
    Возвращает список словарей валют в формате:
    [
      {
        'id': 'R01235',
        'num_code': '840',
        'char_code': 'USD',
        'name': 'Доллар США',
        'value': 93.25,
        'nominal': 1,
        'previous': 92.5,
        'date': '2025-12-05'
      },
      ...
    ]
    :param currency_codes: список символьных кодов ('USD','EUR') — если None, возвращает все
    :param url: URL JSON API
    :return: список словарей валют
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        raise ConnectionError('API недоступен')

    try:
        data = resp.json()
    except Exception:
        raise ValueError('JSON некорректен')

    # Дата — в корне JSON, не в Valute
    date_str = data.get("Date") or data.get("Timestamp") or None

    valute = data.get("Valute")
    if not isinstance(valute, dict):
        raise KeyError('Нет ключа "Valute" или он некорректен')

    result: List[dict] = []

    for char_code, info in valute.items():
        try:
            if currency_codes and char_code not in currency_codes:
                continue

            currency_data = {
                'id': info.get('ID', char_code),
                'num_code': info.get('NumCode', ''),
                'char_code': char_code,                     # <- правильный ключ
                'name': info.get('Name', ''),
                'value': float(info.get('Value', 0.0)),
                'nominal': int(info.get('Nominal', 1)),
                'previous': float(info.get('Previous', 0.0)) if info.get('Previous') is not None else None,
                'date': date_str
            }
            result.append(currency_data)
        except (AttributeError, ValueError, TypeError) as e:
            raise ValueError(f'Некорректные данные для валюты {char_code}: {e}')
    return result

if __name__ == '__main__':
    print(get_currencies(["USD", "EUR"])[:2])
