import argparse
import logging
import requests

from typing import Optional

API_URL = ''
AUTH_TOKEN = ''
DEFAULT_JSON_FILE_PATH = 'dashboards.txt'


def load_data_from_json(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data


def send_dashboard_request(url: str,
                            folder_id: Optional[int] = None,
                            folder_uid: Optional[str] = None,
                            overwrite: Optional[bool] = None) -> None:
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {AUTH_TOKEN}'
     }

    data = {
        "dashboard": load_data_from_json(url),
        "folderId": folder_id,
        "folderUid": folder_uid,
        "message": "Initial commit.",
        "overwrite": overwrite
     }

    response = requests.post(API_URL, headers=headers, json=data)

    logging.info(f'Статус код: {response.status_code}')
    if response.status_code == 200:
        logging.info('Запрос успешно выполнен.')
    else:
        logging.error(f'Произошла ошибка при выполнении запроса: {response.text}')


def process_dashboard_file(file_path: str, args: argparse.Namespace) -> None:
    try:
        with open(file_path, 'r') as file:
            urls = file.read().splitlines()

        if not urls:
            raise ValueError(f'Файл {file_path} не содержит записей.')

        for url in urls:
            send_dashboard_request(url, args.folderId, args.folderUid, args.overwrite)
    
    except FileNotFoundError as e:
        logging.error(f'Файл {file_path} не существует.')
 
    except ValueError as e:
        logging.error(str(e))
 
    except Exception as e:
        logging.error('Произошла непредвиденная ошибка: ' + str(e))


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('file_path', nargs='?', default=DEFAULT_JSON_FILE_PATH,
                        help='Путь до текстового файла с ссылками на дашборды')
      
    parser.add_argument('--folderId', type=int,
                        help='ID папки')
 
    parser.add_argument('--folderUid', type=str,
                        help='UID папки')
  
    parser.add_argument('--overwrite', action='store_false',
                        help='Перезаписать существующие дашборды')
  
    args = parser.parse_args()
    return args


def main() -> None:
    configure_logging()

    args = parse_arguments()
    process_dashboard_file(args.file_path, args)

if __name__ == '__main__':
    main()