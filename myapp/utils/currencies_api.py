import requests
import sys
import functools
import logging


logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('main.log', encoding='utf-8')
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)

def logger_using(func=None, *, handle=sys.stdout):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info('Calling %s args = %s kwargs = %s', func.__name__, args, kwargs)
        try:
            res = func(*args, **kwargs)
            logger.info('%s is finished, result is: %s', func.__name__, res)
            return res
        except Exception as e:
            logger.error('%s is raised %s', func.__name__, e)
            raise
    return wrapper

@logger_using
def get_currencies(
        currency_codes: list,
        url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> dict:
    """
    Получает курсы валют по списку кодов через API ЦБ РФ.

    :param currency_codes: список кодов валют, например ["USD", "EUR"]
    :param url: URL API ЦБ РФ
    :return: словарь вида {"USD": 93.25, "EUR": 101.7}
    """

    try:
        response = requests.get(url)
    except Exception as e:
        raise ConnectionError('API недоступен')

    try:
        data = response.json()
    except:
        raise ValueError('JSON некорректен')

    try:
        valute = data.get("Valute", {})
    except:
        raise KeyError('Нет ключа "Valute"')


    result = {}

    for code in currency_codes:
        info = valute.get(code)
        if info is None:
            raise KeyError('Валюта отсутствует в списке')
        else:
            result[code] = info["Value"]
            if not isinstance(result[code], (int, float)):
                raise TypeError('Курс валюты имеет неверный тип')
    return result


if __name__ == '__main__':
    get_currencies(["USD", "EUR"])