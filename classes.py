from dataclasses import dataclass


@dataclass
class Book:
    """Класс книги"""
    title: str
    img_url: str
    txt_url: str
    genres: list[str]
    comments: list[str]
    author: str
    book_path: str
    image_path: str

    def to_dict(self):
        return dict(
            title=self.title,
            genres=self.genres,
            comments=self.comments,
            author=self.author,
            book_path=self.book_path,
            image_path=self.image_path,
        )
