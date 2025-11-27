from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .llm import LLMClient, Message
from .config import ResearchConfig
from .search import SearchResult


@dataclass
class SearchPlan:
    queries: List[str]


class QueryPlanner:
    def __init__(self, llm: LLMClient, config: ResearchConfig):
        self.llm = llm
        self.config = config

    def propose_queries(self, topic: str) -> SearchPlan:
        system = Message("system", self.config.system_prompt)
        user = Message(
            "user",
            (
                "You need to design a set of aggressive web search queries to research the following topic:\n"
                f"{topic}\n"
                "Return 6-10 diverse queries covering background, data, contrarian views, risks, and forecasts."
            ),
        )
        response = self.llm.chat([system, user], temperature=0.2)
        queries = [line.strip("- ") for line in response.splitlines() if line.strip()]
        return SearchPlan(queries=queries[: self.config.search_results])


@dataclass
class OutlineSection:
    heading: str
    children: List["OutlineSection"]

    def to_markdown(self, level: int = 1) -> str:
        prefix = "#" * min(level, 6)
        lines = [f"{prefix} {self.heading}"]
        for child in self.children:
            lines.append(child.to_markdown(level=level + 1))
        return "\n".join(lines)


class OutlinePlanner:
    def __init__(self, llm: LLMClient, config: ResearchConfig):
        self.llm = llm
        self.config = config

    def build_outline(self, topic: str, evidence: List[SearchResult]) -> OutlineSection:
        evidence_bullets = "\n".join(f"- {item.title}: {item.snippet}" for item in evidence[:6])
        system = Message("system", self.config.system_prompt)
        user = Message(
            "user",
            (
                "Create a hierarchical outline for a deeply sourced analytical report."
                f" Target words: {self.config.report_word_target}. Outline depth: {self.config.outline_depth}.\n"
                f"Topic: {topic}\n"
                f"Evidence summary:\n{evidence_bullets}"
            ),
        )
        response = self.llm.chat([system, user], temperature=0.4)
        headings = [line.strip("- ") for line in response.splitlines() if line.strip()]
        children = [OutlineSection(heading=title, children=[]) for title in headings]
        return OutlineSection(heading=topic, children=children)
