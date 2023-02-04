import os
from urllib.parse import unquote, urlparse

import requests
from argparse import ArgumentParser, Namespace
from requests.exceptions import HTTPError

from books import parse_book_page
from download import download_txt, download_img


def check_response(response: requests.Response):
    """Функция для проверки отклика на ошибки.
    Args:
        response (Response): Объект отклика сервера.
    Raises:
        HTTPError: Если в отклике были редиректы
    """
    response.raise_for_status()
    if len(response.history):
        raise requests.exceptions.HTTPError


def get_image_file_name(url: str) -> str:
    """Функция для получения имени файла из ссылки.
    Args:
        url (str): Cсылка на файл, который хотим скачать.
    Returns:
        str: Имя для сохранения файла.
    """
    parsed_link = unquote(urlparse(url).path)
    return os.path.split(parsed_link)[-1]


def get_parameters() -> Namespace:
    """Функция для получения параметров запуска скрипта.
    Returns:
        Namespace: Объект параметров argparse.
    """
    parser = ArgumentParser()
    parser.add_argument(
        '--start_id',
        type=int,
        default=1,
        help='Start book id'
    )
    parser.add_argument(
        '--end_id',
        type=int,
        default=10,
        help='End book id'
    )
    return parser.parse_args()


def main():
    parameters = get_parameters()

    folders = {
        'books': 'books',
        'images': 'images'
    }
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)

    for book_id in range(parameters.start_id, parameters.end_id + 1):

        response = requests.get(f'https://tululu.org/b{book_id}/')
        try:
            check_response(response)
            book = parse_book_page(response.text)
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
        print(f'\nНазвание: {book.sanitized_title}')
        print(f'Автор: {book.author}')
        print(f'Жанры: {book.genres}')
        print('Комментарии: ')
        for comment in book.comments:
            print(comment)


if __name__ == '__main__':
    main()
