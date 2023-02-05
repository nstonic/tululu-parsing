import logging
import sys
import time
from urllib.parse import urljoin

import requests
from requests.exceptions import ChunkedEncodingError, ConnectionError, HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from classes import Book
from download import download_book


def check_response(response: requests.Response):
    """Функция для проверки отклика на ошибки.
    Args:
        response (Response): Объект отклика сервера.
    Raises:
        HTTPError: Если в отклике были редиректы
    """
    response.raise_for_status()
    if len(response.history):
        raise requests.exceptions.HTTPError('Страница не найдена.')


def get_txt_url(soup: BeautifulSoup) -> str:
    """Функция для проверки наличия и получения ссылки на текстовый файл.
    Args:
        soup (BeautifulSoup): Объект класса BeautifulSoup.
    Returns:
        str: Ссылка на скачивание текстового файла.
    Raises:
        HTTPError: Если ссылки в документе нет
    """
    if txt_link := soup.find('a', string='скачать txt'):
        return txt_link['href']
    else:
        raise requests.exceptions.HTTPError('Отсутствует ссылка на txt файл')


def parse_book_page(html: str, book_id: int) -> Book:
    """Функция для парсинга страницы сайта с описание книги.
    Args:
        html (str): HTML код страницы.
    Returns:
        Book: Объект книги.
    """
    base_url = 'https://tululu.org/'

    soup = BeautifulSoup(html, 'lxml')

    title, author = soup.find('h1').text.split('::')
    full_txt_url = urljoin(
        base_url,
        get_txt_url(soup)
    )
    full_img_url = urljoin(
        base_url,
        soup.find('div', class_='bookimage').find('img')['src']
    )
    comments = [
        comment.find('span', class_='black').text
        for comment in soup.find_all('div', class_='texts')
    ]
    genres = [
        genre.text
        for genre in soup.find('span', class_='d_book').find_all('a')
    ]

    return Book(
        id=book_id,
        sanitized_title=sanitize_filename(title.strip()),
        img_url=full_img_url,
        txt_url=full_txt_url,
        comments=comments,
        genres=genres,
        author=author.strip()
    )


def get_book_by_id(book_id: int) -> Book | None:
    """Функция для получения книги. Добавлена устойчивость к ошибкам соединения.
    Args:
        book_id (str): Id книги.
    Returns:
        book: Объект класса Book.
    """
    url = f'https://tululu.org/b{book_id}/'
    delay = 0
    while True:
        delay = min(delay, 30)  # ограничим время задержи 30 секундами
        try:
            response = requests.get(url)
            check_response(response)
            book = parse_book_page(response.text, book_id)
            download_book(book)
            return book
        except (ChunkedEncodingError, ConnectionError):
            time.sleep(delay)
            delay += 5
            continue
        except HTTPError as ex:
            msg = f'Книга по ссылке {url} недоступна. Причина: {ex}'
            logging.warning(msg)
            print(f'\n{msg}', file=sys.stderr)
            return
