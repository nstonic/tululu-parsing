from typing import NamedTuple


class Book(NamedTuple):
    """Класс книги"""
    id: int
    sanitized_title: str
    img_url: str
    txt_url: str
    genres: list[str]
    comments: list[str]
    author: str
