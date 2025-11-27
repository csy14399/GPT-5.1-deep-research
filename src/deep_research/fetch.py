from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import requests
from bs4 import BeautifulSoup


@dataclass
class PageContent:
    url: str
    title: str
    text: str


class WebPageFetcher(Protocol):
    def fetch(self, url: str) -> PageContent:  # pragma: no cover - protocol
        ...


class RequestsFetcher:
    """Fetches HTML pages and extracts readable text."""

    def __init__(self, timeout: int = 20):
        self.timeout = timeout

    def fetch(self, url: str) -> PageContent:
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else url
        for script in soup(["script", "style"]):
            script.decompose()
        text = " ".join(part.strip() for part in soup.get_text(separator=" ").split())
        return PageContent(url=url, title=title, text=text)


class StaticFetcher:
    """Returns preset content for deterministic testing."""

    def __init__(self, page: PageContent):
        self.page = page

    def fetch(self, url: str) -> PageContent:
        return self.page
