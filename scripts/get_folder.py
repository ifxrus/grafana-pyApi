import logging
import requests

API_URL = ''
AUTH_TOKEN = ''


def get_folders() -> None:
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {AUTH_TOKEN}'
    }

    response = requests.get(API_URL, headers=headers)

    logging.info(f'Статус код: {response.status_code}')
    if response.status_code == 200:
        logging.info('Запрос успешно выполнен.')

        folders = response.json()
        for folder in folders:
            folder_id: int = folder.get('id')
            folder_uid: str = folder.get('uid')
            folder_title: str = folder.get('title')
            print(f"Название папки: {folder_title}")
            print(f"ID папки: {folder_id}, UID: {folder_uid}")
            print("-" * 20)
    else:
        logging.error(f"Произошла ошибка при выполнении запроса: {response.text}")


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def main() -> None:
    configure_logging()
    get_folders()


if __name__ == '__main__':
    main()