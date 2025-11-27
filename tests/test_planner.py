from deep_research import EchoLLM, QueryPlanner, OutlinePlanner, ResearchConfig, SearchResult


def test_query_planner_generates_queries():
    llm = EchoLLM()
    config = ResearchConfig(search_results=5)
    planner = QueryPlanner(llm=llm, config=config)

    plan = planner.propose_queries("Test Topic")

    assert len(plan.queries) <= config.search_results
    assert "Test Topic" in "\n".join(llm.calls[-1][1].content for _ in range(1))


def test_outline_planner_wraps_topic():
    llm = EchoLLM()
    config = ResearchConfig(report_word_target=500, outline_depth=2)
    planner = OutlinePlanner(llm=llm, config=config)
    evidence = [SearchResult(title="Source A", url="http://example.com", snippet="Insight")]  # type: ignore[arg-type]

    outline = planner.build_outline("Important Theme", evidence)

    md = outline.to_markdown()
    assert md.startswith("# Important Theme")
    assert "Source A" in llm.calls[-1][1].content
