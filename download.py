import requests
import requests.exceptions as req_ex


def check_response(response: requests.Response):
    """Функция для проверки отклика на ошибки.
    Args:
        response (Response): Объект отклика сервера.
    Raises:
        HTTPError: Если в отклике были редиректы
    """
    response.raise_for_status()
    if response.history:
        raise req_ex.HTTPError('Страница не найдена.')


def download_txt(txt_url: str, book_path: str):
    """Функция для скачивания текстовых файлов.
    Args:
        txt_url (str): Ссылка на книгу
        book_path (str): Путь к файлу, куда скачивать
    """
    response = requests.get(txt_url)
    check_response(response)
    with open(book_path, 'w', encoding='utf-8') as file:
        file.write(response.text)


def download_img(img_url: str, image_path: str):
    """Функция для скачивания бинарных файлов.
    Args:
        img_url (str): Ссылка на обложку
        image_path (str): Путь к файлу, куда скачивать
    """
    response = requests.get(img_url)
    check_response(response)
    with open(image_path, 'wb') as file:
        file.write(response.content)
