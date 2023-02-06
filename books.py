import logging
import sys
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
import requests.exceptions as req_ex
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename as sf

from classes import Book
import download as dl


def get_txt_url(soup: BeautifulSoup) -> str:
    """Функция для проверки наличия и получения короткой ссылки на текстовый файл.
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


def parse_book_page(response: requests.Response, book_id: int) -> Book:
    """Функция для парсинга страницы с описанием книги.
    Args:
        book_id: Id книги
        response (str): HTML код страницы.
    Returns:
        Book: Объект книги.
    """

    soup = BeautifulSoup(response.text, 'lxml')

    title, author = soup.find('h1').text.split('::')
    full_txt_url = urljoin(
        response.url,
        get_txt_url(soup)
    )
    full_img_url = urljoin(
        response.url,
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
        sanitized_title=sf(title.strip()),
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
        delay = min(delay, 30)
        try:
            response = requests.get(url)
            dl.check_response(response)
            book = parse_book_page(response, book_id)
            dl.download_txt(
                url=book.txt_url,
                filename=f'{book.id:02.0f}. {book.sanitized_title}.txt',
                folder='books'
            )
            dl.download_img(
                url=book.img_url,
                filename=dl.get_image_file_name(book.img_url),
                folder='images'
            )
        except (req_ex.ChunkedEncodingError, req_ex.ConnectionError) as ex:
            # Проверка на разрыв соединения
            logging.warning(f'{datetime.now().strftime("%Y-%m-%d %H.%M.%S")}: {ex}')
            time.sleep(delay)
            delay += 5
            continue
        except req_ex.HTTPError as ex:
            #  Помимо стандартных случаев, исключение также возбуждается в случае обнаружения редиректа,
            #  либо при отсутствии ссылки на txt файл
            msg = f'Книга по ссылке {url} недоступна. Причина: {ex}'
            logging.warning(msg)
            print(f'\n{msg}', file=sys.stderr)
            return
        else:
            return book
