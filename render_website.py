import json
from livereload import Server, shell

from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_page():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open('books.json') as file:
        books = json.load(file)

    rendered_page = template.render(
        books=books
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    render_page()
    server = Server()
    server.watch('template.html', render_page)
    server.serve()
