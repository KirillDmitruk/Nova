from google import genai

from config import GEMINI_API_KEY, MODEL_NAME
from ui import (
    ask_user,
    console,
    print_answer,
    shutdown,
    startup,
    thinking,
)
from utils import load_system_prompt


class LLMProvider:
    """LLM Класс"""
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt


class GeminiProvider(LLMProvider):
    """Класс  Gemini"""
    def __init__(
        self,
        api_key: str,
        model_name: str,
        system_prompt: str,
    ):
        super().__init__(system_prompt)
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def ask(self, prompt: str) -> str:
        interaction = self.client.interactions.create(
            model=self.model_name,
            input=f"{self.system_prompt}\n\nUser: {prompt}",
        )

        answer = getattr(interaction, "output_text", None)

        if not answer:
            raise ValueError("Gemini returned an empty response")
        return answer


def chat_loop() -> None:
    system_prompt = load_system_prompt()
    provider = GeminiProvider(
        api_key=GEMINI_API_KEY, model_name=MODEL_NAME, system_prompt=system_prompt
    )

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
            answer = provider.ask(
                prompt=user_input,
            )

        print_answer(answer)
        console.print()
