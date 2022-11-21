import logging
import os
import time

FORMAT = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
DATEFMT = '%Y-%m-%dT%H:%M:%S'

logging.basicConfig(
    format=FORMAT,
    datefmt=DATEFMT,
    level=logging.INFO,
)

formatter = logging.Formatter(
    FORMAT,
    datefmt=DATEFMT
)


logger = logging.getLogger(__name__)


def make_directory():
    """Переносит файл data.json из текущей директории в results/"""
    if os.path.isfile('data.json'):
        if not os.path.isdir('results'):
            os.makedirs('results')
            logger.info('Created directory "results/"')
        os.replace('data.json', 'results/data.json')
        logger.info('File "data.json" now in "results/"')
    else:
        logger.error('There is no "data.json" file in current directory')


def make_gitignore_file():
    """
    Создает файл .gitignore. При его наличии, добавляет
    в конец файла строку '*.json', если там её не было до этого
    """
    if os.path.isfile('.gitignore'):
        with open('.gitignore', 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()
            if '*.json' not in last_line:
                with open('.gitignore', 'a', encoding='utf-8') as outfile:
                    outfile.write('\n')
                    outfile.write('*.json')
    else:
        with open('.gitignore', 'a', encoding='utf-8') as outfile:
            outfile.write('.idea/ \n')
            outfile.write('__pycache__/ \n')
            outfile.write('*.pyc \n')
            outfile.write('venv/ \n')
            outfile.write('*.json \n')
    logger.info('.gitignore file is ready')


def func_that_sleeps():
    logger.info('Func starts sleeping')
    time.sleep(5)
    logger.error('Func woke up')
