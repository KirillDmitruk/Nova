from google import genai

from config import GEMINI_API_KEY, MODEL_NAME
from logs.logging_config import logger
from ui import ask_user, console, print_answer, shutdown, startup, thinking
from utils import load_system_prompt

SYSTEM_PROMPT = load_system_prompt()


def ask_genai(prompt: str, client: genai.Client) -> str:
    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
        )

        if hasattr(interaction, "output_text"):
            answer = interaction.output_text
        else:
            answer = "Error: an unexpected type of response was received"

        logger.info(answer)
        return answer

    except Exception:
        logger.exception("Unknown Gemini error")
        raise


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

        with thinking():
            answer = ask_genai(user_input, client)

        print_answer(answer)
        console.print()