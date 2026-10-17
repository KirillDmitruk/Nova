from config import PROMPT_PATH


def load_system_prompt() -> str:
    """Загружает системный промпт из файла и возвращает его в виде строки. Если файл пустой, выбрасывает исключение."""
    prompt = PROMPT_PATH.read_text(encoding="utf-8").strip()
    
    if not prompt:
        raise ValueError("System prompt file is empty")

    return prompt