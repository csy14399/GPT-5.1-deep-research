from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Iterable, List, Protocol


@dataclass
class Message:
    role: str
    content: str


class LLMClient(Protocol):
    """Protocol for chat completion style models."""

    def chat(self, messages: Iterable[Message], **kwargs) -> str:  # pragma: no cover - protocol
        ...


class OpenAIClient:
    """Lightweight wrapper around the OpenAI SDK for GPT-5.1 style models."""

    def __init__(self, model: str = "gpt-5.1", timeout: int | None = None):
        self.model = model
        openai = import_module("openai")
        OpenAI = getattr(openai, "OpenAI")
        self.client = OpenAI(timeout=timeout)

    def chat(self, messages: Iterable[Message], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[message.__dict__ for message in messages],
            **kwargs,
        )
        return response.choices[0].message.content


class EchoLLM:
    """Deterministic LLM used in tests; concatenates contents for inspection."""

    def __init__(self, suffix: str = ""):
        self.suffix = suffix
        self.calls: List[List[Message]] = []

    def chat(self, messages: Iterable[Message], **kwargs) -> str:
        batch = list(messages)
        self.calls.append(batch)
        joined = "\n".join(f"[{m.role}] {m.content}" for m in batch)
        return f"{joined}{self.suffix}"
