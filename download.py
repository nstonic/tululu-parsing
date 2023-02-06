import os
from urllib.parse import unquote, urlparse

import requests
import requests.exceptions as req_ex


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


def get_image_file_name(url: str) -> str:
    """Функция для получения имени файла из ссылки.
    Args:
        url (str): Cсылка на файл, который хотим скачать.
    Returns:
        str: Имя для сохранения файла.
    """
    parsed_link = unquote(urlparse(url).path)
    return os.path.split(parsed_link)[-1]


def download_txt(url: str, filename: str, folder: str):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    """
    response = requests.get(url)
    check_response(response)

    filepath = os.path.join(folder, f'{filename}')
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)


def download_img(url: str, filename: str, folder: str):
    """Функция для скачивания бинарных файлов.
    Args:
        url (str): Cсылка на файл, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    """
    response = requests.get(url)
    check_response(response)

    filepath = os.path.join(folder, f'{filename}')
    with open(filepath, 'wb') as file:
        file.write(response.content)
