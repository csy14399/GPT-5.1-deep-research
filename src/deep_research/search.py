from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import import_module
from typing import Iterable, List, Protocol


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


class SearchProvider(Protocol):
    def search(self, query: str, max_results: int) -> List[SearchResult]:  # pragma: no cover - protocol
        ...


class GPTSearchProvider:
    """Uses GPT-5.1's built-in web search capability via the OpenAI Responses API."""

    def __init__(self, model: str = "gpt-5.1", timeout: int | None = None):
        self.model = model
        openai = import_module("openai")
        OpenAI = getattr(openai, "OpenAI")
        self.client = OpenAI(timeout=timeout)

    def search(self, query: str, max_results: int) -> List[SearchResult]:
        prompt = (
            "Use the built-in web search tool to find the most reliable and recent sources for "
            f'"{query}". Return a JSON object with a `results` array where each item has '
            "`title`, `url`, and `snippet`. Limit to {max_results} items."
        )
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                    ],
                }
            ],
            tools=[{"type": "web_search"}],
            max_output_tokens=600,
        )

        raw_text = getattr(response, "output_text", None) or str(response)
        try:
            parsed = json.loads(raw_text)
            rows = parsed.get("results", [])
        except Exception:
            rows = []

        results: List[SearchResult] = []
        for row in rows[:max_results]:
            results.append(
                SearchResult(
                    title=row.get("title", ""),
                    url=row.get("url", ""),
                    snippet=row.get("snippet", ""),
                )
            )

        return results


class StaticSearchProvider:
    """In-memory provider used in tests or deterministic runs."""

    def __init__(self, results: Iterable[SearchResult]):
        self.results = list(results)

    def search(self, query: str, max_results: int) -> List[SearchResult]:
        return self.results[:max_results]
