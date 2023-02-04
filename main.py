import os
from urllib.parse import unquote, urlparse

from argparse import ArgumentParser
import requests
from requests.exceptions import HTTPError

from books import get_book_by_id


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
    args = parser.parse_args()

    folders = {
        'books': 'books',
        'images': 'images'
    }
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    for book_id in range(args.start_id, args.end_id+1):
        try:
            book = get_book_by_id(book_id)
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
        print(f'Название: {book.sanitized_title}')
        print(f'Автор: {book.author}')
        print(f'Жанры: {book.genres}\n')
        # for comment in book.comments:
        #     print(comment)
        # print()


if __name__ == '__main__':
    main()
