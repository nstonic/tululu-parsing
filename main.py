import json
import logging
import os
from datetime import datetime

import argparse

from books import get_book, get_book_urls_by_caterogy


def get_arguments() -> argparse.Namespace:
    """Функция для получения параметров запуска скрипта.
    Returns:
        Namespace: Объект параметров argparse.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--start_page',
        type=int,
        default=1,
        help='Начать парсинг с этой страницы'
    )
    parser.add_argument(
        '--end_page',
        type=int,
        default=10,
        help='Закончить парсинг на этой странице (включительно)'
    )
    parser.add_argument(
        '--dest_folder',
        default='downladed_books',
        help='Путь к каталогу с результатами парсинга: картинкам, книгам, JSON'
    )
    parser.add_argument(
        '--json_path',
        help='Свой путь к json файлу с результатами'
    )
    parser.add_argument(
        '--skip_imgs',
        action='store_true',
        help='Не скачивать картинки'
    )
    parser.add_argument(
        '--skip_txt',
        action='store_true',
        help='Не скачивать книги'
    )
    return parser.parse_args()


def main():
    args = get_arguments()
    folders = {
        'books': os.path.join(args.dest_folder, 'books'),
        'images': os.path.join(args.dest_folder, 'images')
    }
    json_path = os.path.join(args.json_path or args.dest_folder, 'books.json')

    logging.basicConfig(
        filename=f'books {datetime.now().strftime("%Y-%m-%d %H.%M")}.log',
        level=logging.WARNING
    )

    books_urls = get_book_urls_by_caterogy(
        'https://tululu.org/l55/',
        start_page=args.start_page,
        end_page=args.end_page
    )
    books = []
    for book_url in books_urls:
        if book := get_book(book_url, folders, args):
            print(book_url)
            books.append(book.__dict__)
    with open(json_path, 'w') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
