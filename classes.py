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

    def __str__(self):
        comments_string = '\n'.join(self.comments)
        return f'\nНазвание: {self.title}\nАвтор: {self.author}\nЖанры: {self.genres}\nКомментарии: {comments_string}'
