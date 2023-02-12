from dataclasses import dataclass


@dataclass
class Book:
    """Класс книги"""
    book_id: str
    title: str
    img_url: str
    txt_url: str
    genres: list[str]
    comments: list[str]
    author: str
    book_path: str
    image_path: str
