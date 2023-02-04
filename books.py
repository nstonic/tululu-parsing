from typing import NamedTuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


class Book(NamedTuple):
    """Класс книги"""
    sanitized_title: str
    img_url: str
    txt_url: str
    genres: list[str]
    comments: list[str]
    author: str


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
        raise requests.exceptions.HTTPError


def parse_book_page(html: str) -> Book:
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
        sanitized_title=sanitize_filename(title.strip()),
        img_url=full_img_url,
        txt_url=full_txt_url,
        comments=comments,
        genres=genres,
        author=author.strip()
    )
