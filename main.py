import logging
import os
from datetime import datetime

import argparse

from books import get_book_by_id


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
    logging.basicConfig(
        filename=f'books {datetime.now().strftime("%Y-%m-%d %H.%M")}.log',
        level=logging.WARNING
    )

    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)

    for book_id in range(parameters.start_id, parameters.end_id + 1):
        if book := get_book_by_id(book_id):
            print(f'\nНазвание: {book.sanitized_title}\n'
                  f'Автор: {book.author}\n'
                  f'Жанры: {book.genres}\n'
                  'Комментарии: ')
            for comment in book.comments:
                print(comment)


if __name__ == '__main__':
    main()
