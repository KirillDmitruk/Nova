from google import genai

from config import GEMINI_API_KEY, MODEL_NAME
from logs.logging_config import logger
from ui import (
    ask_user,
    console,
    print_answer,
    print_error,
    shutdown,
    startup,
    thinking,
)
from utils import load_system_prompt

SYSTEM_PROMPT = load_system_prompt()


class GeminiRequestError(RuntimeError):
    """Raised when Gemini cannot process a request."""


def ask_genai(prompt: str, client: genai.Client) -> str:
    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
        )
    except Exception as error:
        logger.exception("Gemini request failed")

        raise GeminiRequestError(
            "Could not get a response from Gemini. "
            "Check the API key, model name, and internet connection."
        ) from error

    answer = getattr(interaction, "output_text", None)

    if not answer:
        logger.error("Gemini returned an empty response")

        raise GeminiRequestError(
            "Gemini returned an empty response. Please try again."
        )

    logger.info(answer)
    return answer


def chat_loop() -> None:
    client = genai.Client(api_key=GEMINI_API_KEY)

    startup()

    while True:
        user_input = ask_user()

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "bye"}:
            shutdown()
            break

        console.print()

        try:
            with thinking():
                answer = ask_genai(user_input, client)
        except GeminiRequestError as error:
            print_error(str(error))
            continue

        print_answer(answer)
        console.print()
