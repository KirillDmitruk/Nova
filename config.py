import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

VERSION = "0.1"

BASE_DIR = Path(__file__).resolve().parent
PROMPT_PATH = BASE_DIR / "prompt" / "system.txt"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
MODEL_NAME = os.getenv("MODEL_NAME", "").strip()


class ConfigurationError(RuntimeError):
    """Raised when required application settings are missing."""


def validate_config() -> None:
    required_variables = {
        "GEMINI_API_KEY": GEMINI_API_KEY,
        "MODEL_NAME": MODEL_NAME,
    }

    missing_variables = [
        name
        for name, value in required_variables.items()
        if not value
    ]

    if missing_variables:
        missing = ", ".join(missing_variables)

        raise ConfigurationError(
            f"Missing required environment variables: {missing}. "
            "Copy .env.sample to .env and fill in the values."
        )
