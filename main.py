import os
from pprint import pprint
from urllib.parse import unquote, urlparse

import requests
from requests.exceptions import HTTPError

from books import parse_book_by_id


def download_txt(url: str, filename: str, folder: str) -> str:
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(url)
    response.raise_for_status()

    filepath = os.path.join(folder, f'{filename}')
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)
    return filepath


def download_img(url: str, filename: str, folder: str) -> str:
    """Функция для скачивания бинарных файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(url)
    response.raise_for_status()

    filepath = os.path.join(folder, f'{filename}')
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def get_image_file_name(img_url: str) -> str:
    parsed_link = unquote(urlparse(img_url).path)
    return os.path.split(parsed_link)[-1]


def main():
    folders = {
        'books': 'books',
        'images': 'images',
        'comments': 'comments'
    }
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    for book_id in range(1, 101):  # пробуем скачать книги с 1 по 10
        try:
            book = parse_book_by_id(book_id)
        except HTTPError:
            continue

        download_txt(
            url=book.txt_url,
            filename=f'{book_id:02.0f}. {book.sanitized_title}.txt',
            folder=folders['books']
        )

        download_img(
            url=book.img_url,
            filename=get_image_file_name(book.img_url),
            folder=folders['images']
        )
        print(f'Заголовок: {book.sanitized_title}')
        print(book.genres)
        # for comment in book.comments:
        #     print(comment)
        # print()


if __name__ == '__main__':
    main()
