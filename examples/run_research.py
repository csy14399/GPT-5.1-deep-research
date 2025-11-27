"""Example script showing how to run the research orchestrator."""

from deep_research import (
    DuckDuckGoSearch,
    EchoLLM,
    ResearchConfig,
    ResearchOrchestrator,
    RequestsFetcher,
)


def main():
    config = ResearchConfig()
    llm = EchoLLM()  # Replace with OpenAIClient(model="gpt-5.1") for live runs
    search = DuckDuckGoSearch()
    fetcher = RequestsFetcher()
    orchestrator = ResearchOrchestrator(llm=llm, search=search, fetcher=fetcher, config=config)

    topic = "Long-horizon investment outlook for AI infrastructure"
    artifacts = orchestrator.run(topic)
    print(artifacts.report)


if __name__ == "__main__":
    main()
