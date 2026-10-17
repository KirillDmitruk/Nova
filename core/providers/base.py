from abc import ABC, abstractmethod


class LLMProvider(ABC):
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    @abstractmethod
    def ask(self, prompt: str) -> str:
        pass