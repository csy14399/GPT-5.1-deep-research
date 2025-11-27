from deep_research import (
    EchoLLM,
    ResearchConfig,
    ResearchOrchestrator,
    SearchResult,
    StaticFetcher,
    StaticSearchProvider,
    PageContent,
)


def test_orchestrator_runs_end_to_end():
    llm = EchoLLM(suffix=" ::draft")
    config = ResearchConfig(search_results=2, max_search_rounds=1, report_word_target=100)
    search_provider = StaticSearchProvider(
        [
            SearchResult(title="Doc 1", url="http://example.com/1", snippet="Alpha"),
            SearchResult(title="Doc 2", url="http://example.com/2", snippet="Beta"),
        ]
    )
    fetcher = StaticFetcher(PageContent(url="http://example.com/1", title="Doc 1", text="Content A"))
    orchestrator = ResearchOrchestrator(llm=llm, search=search_provider, fetcher=fetcher, config=config)

    artifacts = orchestrator.run("Synthetic Topic")

    assert artifacts.plan.queries
    assert len(artifacts.searches) == 2
    assert artifacts.summaries
    assert "Synthetic Topic" in artifacts.report
    assert artifacts.outline_markdown.startswith("# Synthetic Topic")
