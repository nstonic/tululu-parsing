from error_checking import get_response


def download_txt(txt_url: str, book_path: str):
    """Функция для скачивания текстовых файлов.
    Args:
        txt_url (str): Ссылка на книгу
        book_path (str): Путь к файлу, куда скачивать
    """
    response = get_response(txt_url)
    with open(book_path, 'w', encoding='utf-8') as file:
        file.write(response.text)


def download_img(img_url: str, image_path: str):
    """Функция для скачивания бинарных файлов.
    Args:
        img_url (str): Ссылка на обложку
        image_path (str): Путь к файлу, куда скачивать
    """
    response = get_response(img_url)
    with open(image_path, 'wb') as file:
        file.write(response.content)
