from dataclasses import dataclass


@dataclass
class Book:
    """Класс книги"""
    title: str
    genres: list[str]
    comments: list[str]
    author: str
    img_url: str = None
    txt_url: str = None
    book_path: str = None
    image_path: str = None

    def to_dict(self):
        return dict(
            title=self.title,
            genres=self.genres,
            comments=self.comments,
            author=self.author,
            book_path=self.book_path,
            image_path=self.image_path,
        )
