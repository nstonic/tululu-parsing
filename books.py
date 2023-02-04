from typing import NamedTuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


class Book(NamedTuple):
    sanitized_title: str
    img_url: str
    txt_url: str
    genres: list[str]
    comments: list[str]
    author: str


def check_book(response: requests.Response):
    response.raise_for_status()
    if len(response.history):
        raise requests.exceptions.HTTPError


def get_txt_url(soup: BeautifulSoup) -> str:
    if txt_link := soup.find('a', string='скачать txt'):
        return txt_link['href']
    else:
        raise requests.exceptions.HTTPError


def get_book_by_id(book_id: int) -> Book:
    base_url = 'https://tululu.org/'

    response = requests.get(urljoin(base_url, f'b{book_id}/'))
    check_book(response)

    soup = BeautifulSoup(response.text, 'lxml')

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
