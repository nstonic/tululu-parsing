import os
from urllib.parse import unquote, urlparse

import requests

from classes import Book


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
    response.raise_for_status()

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
    response.raise_for_status()

    filepath = os.path.join(folder, f'{filename}')
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_book(book: Book):
    download_txt(
        url=book.txt_url,
        filename=f'{book.id:02.0f}. {book.sanitized_title}.txt',
        folder='books'
    )
    download_img(
        url=book.img_url,
        filename=get_image_file_name(book.img_url),
        folder='images'
    )
