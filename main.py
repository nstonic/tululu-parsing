import json
import logging
import os
from datetime import datetime

import argparse
from pathvalidate.argparse import validate_filepath_arg

from books import get_book, get_book_urls_by_caterogy


def prepare_dests(dest_folder: str, json_path: str, skip_txt: bool, skip_imgs: bool) -> dict:
    """Функция для создания всех необходимых папок, а также получения путей к файлам логов и json
    Args:
        dest_folder (str): Путь к каталогу с результатами парсинга
        json_path (str): Свой путь к json файлу с результатами
        skip_txt (bool): Не скачивать тексты
        skip_imgs (bool): Не скачивать обложки
    Returns:
        dict: словарь, содержащий пути к папкам и файлам
    """
    pathes = {
        'log': os.path.join(dest_folder, f'{datetime.now().strftime("%Y-%m-%d %H.%M")}.log'),
        'json': json_path or os.path.join(dest_folder, 'books.json')
    }
    os.makedirs(os.path.split(pathes['json'])[0], exist_ok=True)
    if not skip_txt:
        pathes['books'] = os.path.join(dest_folder, 'books')
        os.makedirs(pathes['books'], exist_ok=True)
    if not skip_imgs:
        pathes['images'] = os.path.join(dest_folder, 'images')
        os.makedirs(pathes['images'], exist_ok=True)
    return pathes


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
        default=4,
        help='Закончить парсинг на этой странице (включительно)'
    )
    parser.add_argument(
        '--dest_folder',
        default='downladed_books',
        type=validate_filepath_arg,
        help='Путь к каталогу с результатами парсинга: картинкам, книгам, JSON и логами'
    )
    parser.add_argument(
        '--json_path',
        type=validate_filepath_arg,
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
        help='Не скачивать книги. В этом случае будут скачаны обложки даже тех книг, у которых нет ссылки на текст.'
    )
    return parser.parse_args()


def main():
    args = get_arguments()
    pathes = prepare_dests(
        dest_folder=args.dest_folder,
        json_path=args.json_path,
        skip_txt=args.skip_txt,
        skip_imgs=args.skip_imgs
    )
    logging.basicConfig(
        filename=pathes['log'],
        level=logging.WARNING
    )

    category_url = 'https://tululu.org/l55/'
    books_urls = get_book_urls_by_caterogy(
        category_url,
        start_page=args.start_page,
        end_page=args.end_page
    )
    books = []
    for book_url in books_urls:
        if book := get_book(book_url, pathes,
                            skip_txt=args.skip_txt, skip_imgs=args.skip_imgs):
            print(book_url)
            books.append(book.to_dict())
    with open(pathes['json'], 'w') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
