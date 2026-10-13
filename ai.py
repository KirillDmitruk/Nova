from google import genai

from config import GEMINI_API_KEY, MODEL_NAME
from logs.logging_config import logger
from ui import (
    ask_user,
    console,
    print_answer,
    shutdown,
    startup,
    thinking,
)
from utils import load_system_prompt


def ask_genai(prompt: str, client: genai.Client, system_prompt: str,) -> str:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=f"{system_prompt}\n\nUser: {prompt}",
        )

        answer = getattr(interaction, "output_text", None)

        if not answer:
            raise ValueError("Gemini returned an empty response")

        return answer


def chat_loop() -> None:
    system_prompt = load_system_prompt()
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
            answer = ask_genai(user_input, client, system_prompt)
            continue

        print_answer(answer)
        console.print()
