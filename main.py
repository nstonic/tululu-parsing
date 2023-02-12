import json
import logging
import os
from datetime import datetime

import argparse

from books import get_book, get_book_urls_by_caterogy


def get_parameters() -> argparse.Namespace:
    """Функция для получения параметров запуска скрипта.
    Returns:
        Namespace: Объект параметров argparse.
    """
    parser = argparse.ArgumentParser()
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

    logging.basicConfig(
        filename=f'books {datetime.now().strftime("%Y-%m-%d %H.%M")}.log',
        level=logging.WARNING
    )

    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    books_urls = get_book_urls_by_caterogy('https://tululu.org/l55/', 1, 1)
    books = []
    for book_url in books_urls:
        if book := get_book(book_url, folders):
            print(book)
            books.append(book.__dict__)
    with open('books.json', 'w') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
