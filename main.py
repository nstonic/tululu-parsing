import os

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests


class RedirectError(requests.exceptions.HTTPError):
    pass


def parse_book_title(response: requests.Response) -> str:
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h1').text.split('::')[0].strip()
    return sanitize_filename(title)


def check_for_redirect(response: requests.Response) -> None:
    if len(response.history):
        raise RedirectError


def download_txt(url: str, filename: str, folder: str = 'books') -> str:
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()

    filepath = os.path.join(folder, f'{filename}.txt')
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)
    return filepath


def main():
    folder = 'books'
    os.makedirs(folder, exist_ok=True)
    for id in range(1, 11):  # пробуем скачать книги с 1 по 10
        response = requests.get(f'https://tululu.org/b{id}/')
        try:
            check_for_redirect(response)
        except RedirectError:
            continue
        book_title = parse_book_title(response)

        try:
            filepath = download_txt(
                url=f'https://tululu.org/txt.php?id={id}',
                filename=f'{id:02.0f}. {book_title}',
                folder=folder
            )
            print(filepath)
        except RedirectError:
            continue


if __name__ == '__main__':
    main()
