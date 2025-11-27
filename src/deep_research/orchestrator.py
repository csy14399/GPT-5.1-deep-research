from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .config import ResearchConfig
from .fetch import PageContent, WebPageFetcher
from .llm import LLMClient, Message
from .planner import OutlinePlanner, QueryPlanner, SearchPlan
from .search import SearchProvider, SearchResult
from .summarizer import Summarizer, Summary


@dataclass
class ResearchArtifacts:
    topic: str
    plan: SearchPlan
    searches: List[SearchResult]
    pages: List[PageContent]
    summaries: List[Summary]
    outline_markdown: str
    report: str


class ResearchOrchestrator:
    """Runs an end-to-end research workflow with pluggable tools."""

    def __init__(
        self,
        llm: LLMClient,
        search: SearchProvider,
        fetcher: WebPageFetcher,
        config: ResearchConfig | None = None,
    ):
        self.config = config or ResearchConfig()
        self.llm = llm
        self.search = search
        self.fetcher = fetcher
        self.query_planner = QueryPlanner(llm, self.config)
        self.outline_planner = OutlinePlanner(llm, self.config)
        self.summarizer = Summarizer(llm, self.config)

    def run(self, topic: str) -> ResearchArtifacts:
        plan = self.query_planner.propose_queries(topic)
        search_results = self._execute_search(plan)
        pages = self._fetch_pages(search_results)
        summaries = self.summarizer.summarize(pages)
        outline = self.outline_planner.build_outline(topic, search_results)
        report = self._draft_report(topic, outline, summaries)
        return ResearchArtifacts(
            topic=topic,
            plan=plan,
            searches=search_results,
            pages=pages,
            summaries=summaries,
            outline_markdown=outline.to_markdown(),
            report=report,
        )

    def _execute_search(self, plan: SearchPlan) -> List[SearchResult]:
        aggregated: List[SearchResult] = []
        for query in plan.queries[: self.config.search_results]:
            aggregated.extend(self.search.search(query, max_results=self.config.search_results))
            if len(aggregated) >= self.config.search_results * self.config.max_search_rounds:
                break
        return aggregated[: self.config.search_results * self.config.max_search_rounds]

    def _fetch_pages(self, results: List[SearchResult]) -> List[PageContent]:
        pages: List[PageContent] = []
        for result in results[: self.config.search_results]:
            try:
                pages.append(self.fetcher.fetch(result.url))
            except Exception as exc:  # pragma: no cover - network error path
                pages.append(PageContent(url=result.url, title=result.title, text=f"Fetch error: {exc}"))
        return pages

    def _draft_report(self, topic: str, outline, summaries: List[Summary]) -> str:
        citations = "\n".join(f"- {summary.title}: {summary.url}" for summary in summaries)
        source_notes = "\n".join(summary.summary for summary in summaries)
        system = Message("system", self.config.system_prompt)
        user = Message(
            "user",
            (
                f"Topic: {topic}\n"
                f"Outline:\n{outline.to_markdown()}\n"
                f"Sources:\n{citations}\n\n"
                f"Evidence notes:\n{source_notes}\n\n"
                f"Write a fully cited, deeply analytical report with a target of {self.config.report_word_target} words. "
                "Use markdown, provide an executive summary, bullet-point key findings, risk factors, and an appendix "
                "with methodology."
            ),
        )
        return self.llm.chat([system, user], temperature=0.25, max_tokens=self.config.max_output_tokens)
