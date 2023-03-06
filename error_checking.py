import logging
import time
from datetime import datetime

import requests
from requests.exceptions import HTTPError, ConnectionError, ChunkedEncodingError


class RedirectError(HTTPError):
    def __str__(self):
        return f'Страница отсутствует'


class NoTxtFound(HTTPError):
    def __str__(self):
        return f'Отсутствует ссылка на текст книги'


def retry_on_network_error(func):
    """Декоратор повторяет запрос, если произошел разрыв соединения"""

    def wrapper(url):
        delay = 0
        while True:
            delay = min(delay, 30)
            try:
                return func(url)
            except (ChunkedEncodingError, ConnectionError) as ex:
                logging.error(f'{datetime.now().strftime("%Y-%m-%d %H.%M.%S")}: {ex}')
                time.sleep(delay)
                delay += 5
                continue

    return wrapper


def check_page_errors(func):
    """Декоратор проверяет отсутствие страницы книги, а также ссылки на текст.
    Первым аргументом у проверяемой функции должен быть url"""

    def wrapper(*args, **kwargs):
        url, *_ = args
        try:
            return func(*args, **kwargs)
        except (RedirectError, NoTxtFound) as ex:
            logging.warning(f'Книга по ссылке {url} не найдена. Причина: {ex}')

    return wrapper


@retry_on_network_error
def get_response(page_url: str) -> requests.Response:
    """Функция для получения ответа по get запросу.
    Args:
        page_url: url страницы
    Returns:
        Response
    """
    response = requests.get(page_url)
    response.raise_for_status()
    if response.history:
        raise RedirectError
    return response
