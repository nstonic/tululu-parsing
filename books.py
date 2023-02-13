import os
from urllib.parse import urljoin, urlparse, unquote

import requests
import requests.exceptions as req_ex
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from classes import Book
from decorators import check_response
from download import download_txt, download_img, raise_for_status_or_redirect


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


def parse_book_page(response: requests.Response, txt_path: str, image_path: str) -> Book:
    """Функция для парсинга страницы с описанием книги.
    Args:
        image_path (str): Папка для сохранения обложки книги
        txt_path (str): Папка для сохранения текста книги
        response (str): HTML код страницы.
    Returns:
        Book: Объект книги.
    """

    soup = BeautifulSoup(response.text, 'lxml')

    title, author = soup.select_one('h1').text.split('::')
    sanitized_title = sanitize_filename(title.strip())
    comments = [
        comment.select_one('span.black').text
        for comment in soup.select('div.texts')
    ]
    genres = [
        genre.text
        for genre in soup.select('span.d_book a')
    ]

    book = Book(
        title=sanitized_title,
        comments=comments,
        genres=genres,
        author=author.strip(),
    )

    if txt_path:
        book_id = urlparse(response.url).path.strip("/").strip('b')
        book.txt_url = urljoin(response.url, get_txt_url(soup))
        book.book_path = os.path.join(
            txt_path,
            f'{book_id} {sanitized_title}.txt'
        )

    if image_path:
        book.img_url = urljoin(response.url, soup.select_one('div.bookimage img')['src'])
        book.image_path = os.path.join(
            image_path,
            get_image_file_name(book.img_url)
        )

    return book


@check_response
def get_category_page(page_url: str) -> requests.Response:
    """Функция для получения страницы категории.
    Args:
        page_url: url страницы
    Returns:
        Response
    """
    response = requests.get(page_url)
    raise_for_status_or_redirect(response)
    return response


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
        response = get_category_page(urljoin(category_url, str(page)))
        soup = BeautifulSoup(response.text, 'lxml')
        books_urls.extend(urljoin(response.url, link['href'])
                          for link in soup.select('.d_book div.bookimage a'))
    return books_urls


@check_response
def get_book(book_url: str, pathes: dict) -> Book | None:
    """Функция для получения книги.
    Args:
        pathes (dict): Пути к папкам
        book_url (str): Ссылка на страницу книги.
    Returns:
        book: Объект класса Book.
    """
    response = requests.get(book_url)
    raise_for_status_or_redirect(response)
    book = parse_book_page(
        response,
        txt_path=pathes.get('books'),
        image_path=pathes.get('images')
    )
    if book.txt_url:
        download_txt(txt_url=book.txt_url, book_path=book.book_path)
    if book.img_url:
        download_img(img_url=book.img_url, image_path=book.image_path)
    return book
