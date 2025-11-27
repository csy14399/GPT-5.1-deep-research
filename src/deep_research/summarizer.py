from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .config import ResearchConfig
from .fetch import PageContent
from .llm import LLMClient, Message


@dataclass
class Summary:
    url: str
    title: str
    summary: str


class Summarizer:
    def __init__(self, llm: LLMClient, config: ResearchConfig):
        self.llm = llm
        self.config = config

    def summarize(self, pages: Iterable[PageContent]) -> List[Summary]:
        summaries: List[Summary] = []
        for page in pages:
            prompt = (
                "Summarize the following source with key datapoints, claims, and quoted snippets. "
                "Highlight credibility signals and potential biases."
            )
            system = Message("system", self.config.system_prompt)
            user = Message(
                "user",
                f"URL: {page.url}\nTitle: {page.title}\nContent: {page.text[:4000]}",
            )
            content = self.llm.chat([system, Message("assistant", prompt), user], temperature=0.3)
            summaries.append(Summary(url=page.url, title=page.title, summary=content))
        return summaries
