from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Protocol

from duckduckgo_search import DDGS


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


class SearchProvider(Protocol):
    def search(self, query: str, max_results: int) -> List[SearchResult]:  # pragma: no cover - protocol
        ...


class DuckDuckGoSearch:
    """DuckDuckGo instant answer search provider."""

    def __init__(self, region: str = "us-en", safesearch: str = "moderate"):
        self.region = region
        self.safesearch = safesearch

    def search(self, query: str, max_results: int) -> List[SearchResult]:
        results: List[SearchResult] = []
        with DDGS() as ddgs:
            for row in ddgs.text(query, region=self.region, safesearch=self.safesearch, max_results=max_results):
                results.append(
                    SearchResult(
                        title=row.get("title", ""),
                        url=row.get("href", ""),
                        snippet=row.get("body", ""),
                    )
                )
        return results


class StaticSearchProvider:
    """In-memory provider used in tests or deterministic runs."""

    def __init__(self, results: Iterable[SearchResult]):
        self.results = list(results)

    def search(self, query: str, max_results: int) -> List[SearchResult]:
        return self.results[:max_results]
