import logging
import time
from datetime import datetime

import requests.exceptions as req_ex


def check_response(func):
    """Декоратор повторяет запрос, если произошел разрыв соединения, обрабатывает ошибки парсинга книги.
    А также логирует это всё. Первым аргументом функции func должна быть url обрабатываемой страницы."""

    def wrapper(*args, **kwargs):
        delay = 0
        while True:
            delay = min(delay, 30)
            try:
                return func(*args, **kwargs)
            except (req_ex.ChunkedEncodingError, req_ex.ConnectionError) as ex:
                # Проверка на разрыв соединения
                logging.error(f'{datetime.now().strftime("%Y-%m-%d %H.%M.%S")}: {ex}')
                time.sleep(delay)
                delay += 5
                continue
            except req_ex.HTTPError as ex:
                #  Помимо стандартных случаев, исключение также возбуждается в случае обнаружения редиректа,
                #  либо при отсутствии ссылки на txt файл
                logging.warning(f'Книга по ссылке {args[0]} недоступна. Причина: {ex}')
                return

    return wrapper

