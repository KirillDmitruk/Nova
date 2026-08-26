from config import PROMPT_PATH
from logs.logging_config import logger


class SystemPromptError(RuntimeError):
    """Raised when the system prompt cannot be loaded."""


def load_system_prompt() -> str:
    try:
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        logger.exception("System prompt file not found")

        raise SystemPromptError(
            f"System prompt file was not found: {PROMPT_PATH}"
        ) from error
    except UnicodeError as error:
        logger.exception("System prompt has an invalid encoding")

        raise SystemPromptError(
            "System prompt must be saved in UTF-8 encoding."
        ) from error
    except OSError as error:
        logger.exception("System prompt could not be read")

        raise SystemPromptError(
            f"System prompt could not be read: {PROMPT_PATH}"
        ) from error

    prompt = prompt.strip()

    if not prompt:
        logger.error("System prompt file is empty")

        raise SystemPromptError(
            f"System prompt file is empty: {PROMPT_PATH}"
        )

    return prompt