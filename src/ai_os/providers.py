from __future__ import annotations

import os
from typing import Protocol


class ModelProvider(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class RuleBasedProvider:
    def generate(self, prompt: str) -> str:
        text = prompt.strip().lower()
        if not text:
            return "Hello! I am your assistant."
        if text in {"hello", "hi", "hey"}:
            return "Hello! Nice to meet you."
        if "thanks" in text or "thank you" in text:
            return "You are very welcome."
        if "name" in text:
            return "I can help you remember your name and preferences."
        if "remember" in text:
            return "I can store notes and preferences for you."
        return "I am listening. Tell me more."


class ApiModelProvider:
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return RuleBasedProvider().generate(prompt)

        try:
            import openai
        except ImportError:
            return RuleBasedProvider().generate(prompt)

        client = openai.OpenAI(api_key=self.api_key)
        response = client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text
