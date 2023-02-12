import requests
import requests.exceptions as req_ex

from classes import Book


def check_response(response: requests.Response):
    """Функция для проверки отклика на ошибки.
    Args:
        response (Response): Объект отклика сервера.
    Raises:
        HTTPError: Если в отклике были редиректы
    """
    response.raise_for_status()
    if response.history:
        raise req_ex.HTTPError('Страница не найдена.')


def download_txt(book: Book):
    """Функция для скачивания текстовых файлов.
    Args:
        book: Объект книги
    """
    response = requests.get(book.txt_url)
    check_response(response)
    with open(book.book_path, 'w', encoding='utf-8') as file:
        file.write(response.text)


def download_img(book: Book):
    """Функция для скачивания бинарных файлов.
    Args:
        book: Объект книги
    """
    response = requests.get(book.img_url)
    check_response(response)
    with open(book.image_path, 'wb') as file:
        file.write(response.content)
