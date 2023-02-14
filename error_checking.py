import logging
import time
from datetime import datetime

import requests
import requests.exceptions as req_ex


class RedirectError(req_ex.HTTPError):
    def __str__(self):
        return f'Страница отсутствует'


class NoTxtFound(req_ex.HTTPError):
    def __str__(self):
        return f'Отсутствует ссылка на текст книги'


def check_response(func):
    """Декоратор повторяет запрос, если произошел разрыв соединения"""

    def wrapper(url):
        delay = 0
        while True:
            delay = min(delay, 30)
            try:
                return func(url)
            except (req_ex.ChunkedEncodingError, req_ex.ConnectionError) as ex:
                logging.error(f'{datetime.now().strftime("%Y-%m-%d %H.%M.%S")}: {ex}')
                time.sleep(delay)
                delay += 5
                continue

    return wrapper


def check_page_errors(func):
    """Декоратор проверяет отсутствие страницы книги, а также ссылки на текст.
    Первым аргументом у проверяемой функции должен быть url"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (RedirectError, NoTxtFound) as ex:
            logging.warning(f'Книга по ссылке {args[0]} не найдена. Причина: {ex}')

    return wrapper


@check_response
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
