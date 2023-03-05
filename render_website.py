import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

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
