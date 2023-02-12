import logging
import os
import time
from argparse import Namespace
from datetime import datetime
from urllib.parse import urljoin, urlparse, unquote

import requests
import requests.exceptions as req_ex
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from classes import Book
import download as dl


def get_image_file_name(url: str) -> str:
    """Функция для получения имени файла из ссылки.
    Args:
        url (str): Cсылка на файл, который хотим скачать.
    Returns:
        str: Имя для сохранения файла.
    """
    parsed_link = unquote(urlparse(url).path)
    return os.path.split(parsed_link)[-1]


def get_txt_url(soup: BeautifulSoup) -> str:
    """Функция для проверки наличия и получения короткой ссылки на текстовый файл.
    Args:
        soup (BeautifulSoup): Объект класса BeautifulSoup.
    Returns:
        str: Ссылка на скачивание текстового файла.
    Raises:
        HTTPError: Если ссылки в документе нет
    """
    if txt_link := soup.select_one('a[href^="/txt.php"]'):
        return txt_link['href']
    else:
        raise req_ex.HTTPError('Отсутствует ссылка на txt файл')


def parse_book_page(response: requests.Response, folders: dict) -> Book:
    """Функция для парсинга страницы с описанием книги.
    Args:
        folders: Папки, куда будут сохраняться файлы книги
        response (str): HTML код страницы.
    Returns:
        Book: Объект книги.
    """

    soup = BeautifulSoup(response.text, 'lxml')

    book_id = urlparse(response.url).path.strip("/").strip('b')
    title, author = soup.select_one('h1').text.split('::')
    sanitized_title = sanitize_filename(title.strip())
    full_img_url = urljoin(
        response.url,
        soup.select_one('div.bookimage img')['src']
    )
    full_txt_url = urljoin(
        response.url,
        get_txt_url(soup)
    )
    comments = [
        comment.select_one('span.black').text
        for comment in soup.select('div.texts')
    ]
    genres = [
        genre.text
        for genre in soup.select('span.d_book a')
    ]
    book_path = os.path.join(
        folders['books'],
        f'{book_id} {sanitized_title}.txt'
    )
    image_path = os.path.join(
        folders['images'],
        get_image_file_name(full_img_url)
    )
    return Book(
        book_id=book_id,
        title=sanitized_title,
        img_url=full_img_url,
        txt_url=full_txt_url,
        comments=comments,
        genres=genres,
        author=author.strip(),
        book_path=book_path,
        image_path=image_path
    )


def get_book_urls_by_caterogy(category_url: str, start_page: int, end_page: int) -> list[str]:
    """Функция для получения ссылок на книги по категории.
    Args:
        category_url (str): Ссылка на страницу с категорией книг.
        start_page (int): страница, с которой начинаем сбор ссылок
        end_page (int): страница, на которой заканчиваем
    Returns:
        books_urls: Список ссылок на книги.
    """
    books_urls = []
    for page in range(start_page, end_page + 1):
        response = requests.get(urljoin(category_url, str(page)))
        soup = BeautifulSoup(response.text, 'lxml')
        books_urls.extend(urljoin(response.url, link['href'])
                          for link in soup.select('.d_book div.bookimage a'))
    return books_urls


def get_book(book_url: str, args: Namespace) -> Book | None:
    """Функция для получения книги. Добавлена устойчивость к ошибкам соединения.
    Args:
        args: Аргументы запуска скрипта
        book_url (str): Ссылка на страницу книги.
    Returns:
        book: Объект класса Book.
    """
    folders = {
        'books': os.path.join(args.dest_folder, 'books'),
        'images': os.path.join(args.dest_folder, 'images')
    }
    delay = 0
    while True:
        delay = min(delay, 30)
        try:
            response = requests.get(book_url)
            dl.check_response(response)
            book = parse_book_page(response, folders)
            if not args.skip_txt:
                os.makedirs(folders['books'], exist_ok=True)
                dl.download_txt(book)
            if not args.skip_imgs:
                os.makedirs(folders['images'], exist_ok=True)
                dl.download_img(book)
        except (req_ex.ChunkedEncodingError, req_ex.ConnectionError) as ex:
            # Проверка на разрыв соединения
            logging.error(f'{datetime.now().strftime("%Y-%m-%d %H.%M.%S")}: {ex}')
            time.sleep(delay)
            delay += 5
            continue
        except req_ex.HTTPError as ex:
            #  Помимо стандартных случаев, исключение также возбуждается в случае обнаружения редиректа,
            #  либо при отсутствии ссылки на txt файл
            logging.warning(f'Книга по ссылке {book_url} недоступна. Причина: {ex}')
            return
        else:
            return book
