import json
import os

from livereload import Server

from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked

ROOT_DIR = 'site'


def render_page():
    env = Environment(
        loader=FileSystemLoader('site'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('site/books.json') as file:
        books = json.load(file)
    books_on_page = 10
    books_by_pages = list(chunked(books, books_on_page))
    for index, books in enumerate(books_by_pages):
        page_number = index + 1
        number_of_columns = 2
        rendered_page = template.render(
            books=chunked(books, number_of_columns),
            total_pages=len(books_by_pages),
            current_page=page_number
        )
        pages_dir = os.path.join(ROOT_DIR, 'pages')
        os.makedirs(pages_dir, exist_ok=True)
        page_path = os.path.join(pages_dir, f'index{page_number}.html')
        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    render_page()
    server = Server()
    server.watch(os.path.join(ROOT_DIR, 'template.html'), render_page)
    server.serve(root=ROOT_DIR)
