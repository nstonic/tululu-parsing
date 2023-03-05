import json
import os

from livereload import Server

from jinja2 import Environment, FileSystemLoader, select_autoescape
from setuptools._vendor.more_itertools import chunked

ROOT_DIR = 'pages'


def render_page():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('books.json') as file:
        books = json.load(file)

    books_by_pages = chunked(books, 20)
    for page_number, books in enumerate(books_by_pages):
        rendered_page = template.render(
            books=chunked(books, 2)
        )
        os.makedirs(ROOT_DIR, exist_ok=True)
        page_path = os.path.join(ROOT_DIR, f'index{page_number + 1}.html')
        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    render_page()
    server = Server()
    server.watch('template.html', render_page)
    server.serve(root=ROOT_DIR)
