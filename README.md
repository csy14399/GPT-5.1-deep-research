# GPT-5.1 Deep Research

A pluggable framework for running long-horizon GPT-5.1 research pipelines with web search, browsing, summarization, and report drafting. It is designed for use with API relays such as 柏拉图AI and supports aggressive tool use, high token budgets, and deep evidence collection.

## Features

- **Configurable research budgets**: tune model, temperature, max tool calls, search breadth, and report length via `ResearchConfig`.
- **Search + browse pipeline**: generate diverse queries, run DuckDuckGo search, fetch pages, and summarize sources.
- **Outline and drafting**: build hierarchical outlines and synthesize fully cited markdown reports.
- **Pluggable components**: swap search providers, fetchers, and LLM clients (OpenAI or offline `EchoLLM`).
- **Deterministic tests**: unit tests rely on stubbed components for offline validation.

## Quickstart

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a script (or modify `examples/run_research.py`) to use the orchestrator:

```python
from deep_research import (
    DuckDuckGoSearch,
    OpenAIClient,
    ResearchConfig,
    ResearchOrchestrator,
    RequestsFetcher,
)

config = ResearchConfig(
    model="gpt-5.1",
    search_results=12,
    max_search_rounds=3,
    report_word_target=12000,
)
llm = OpenAIClient(model=config.model)
search = DuckDuckGoSearch()
fetcher = RequestsFetcher()
orchestrator = ResearchOrchestrator(llm=llm, search=search, fetcher=fetcher, config=config)

artifacts = orchestrator.run("投资研究：AI 基础设施的长期前景")
print(artifacts.report)
```

3. For offline experimentation or tests, swap `OpenAIClient` for `EchoLLM` and `StaticSearchProvider` / `StaticFetcher` to avoid network/API calls.

## Architecture

- `deep_research.config`: central configuration with research budgets and safety guidance.
- `deep_research.llm`: LLM protocol plus OpenAI and Echo implementations.
- `deep_research.search`: DuckDuckGo-backed search and a static provider for tests.
- `deep_research.fetch`: HTTP fetcher using `requests` + `BeautifulSoup`, plus static fetcher.
- `deep_research.planner`: query planner and outline generator to shape the report.
- `deep_research.summarizer`: per-source summarization with bias checks.
- `deep_research.orchestrator`: end-to-end pipeline wiring everything together.

## Testing

Run the unit suite:

```bash
pytest
```

The tests use stubbed components and do not make network calls.

## Notes

- To run live against GPT-5.1 through 柏拉图AI or OpenAI-compatible endpoints, ensure the relevant environment variables (e.g., `OPENAI_API_KEY`, `OPENAI_BASE_URL`) are set before invoking the orchestrator.
- Increase `ResearchConfig.max_output_tokens`, `search_results`, and `max_search_rounds` to pursue multi-thousand-word reports with broad evidence coverage.
