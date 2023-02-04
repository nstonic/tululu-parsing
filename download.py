import os

import requests


def download_txt(url: str, filename: str, folder: str):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(url)
    response.raise_for_status()

    filepath = os.path.join(folder, f'{filename}')
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)


def download_img(url: str, filename: str, folder: str):
    """Функция для скачивания бинарных файлов.
    Args:
        url (str): Cсылка на файл, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранено изображение.
    """
    response = requests.get(url)
    response.raise_for_status()

    filepath = os.path.join(folder, f'{filename}')
    with open(filepath, 'wb') as file:
        file.write(response.content)
