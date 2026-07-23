import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

VERSION = "0.1"

BASE_DIR = Path(__file__).resolve().parent

PROMPT_PATH = BASE_DIR / "prompt" / "system.txt"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME")
