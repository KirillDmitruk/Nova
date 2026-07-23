from config import PROMPT_PATH
from logs.logging_config import logger


def load_system_prompt():
    try:
        with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.exception('Файл не найден')
        raise
