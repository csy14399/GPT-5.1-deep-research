"""Example script showing how to run the research orchestrator.

This script works whether or not the package has been installed. When running it
directly from the repository root, we add the local ``src`` directory to
``sys.path`` so that ``deep_research`` can be imported without an editable
install. If you prefer a cleaner setup, run ``python -m pip install -e .`` from
the repository root and remove the path shim below.
"""

from pathlib import Path
import sys

# Ensure local imports work when running the script from the repo root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from deep_research import (
    EchoLLM,
    GPTSearchProvider,
    ResearchConfig,
    ResearchOrchestrator,
    RequestsFetcher,
)


def main():
    config = ResearchConfig()
    llm = EchoLLM()  # Replace with OpenAIClient(model="gpt-5.1") for live runs
    search = GPTSearchProvider()
    fetcher = RequestsFetcher()
    orchestrator = ResearchOrchestrator(llm=llm, search=search, fetcher=fetcher, config=config)

    topic = "Long-horizon investment outlook for AI infrastructure"
    artifacts = orchestrator.run(topic)
    print(artifacts.report)


if __name__ == "__main__":
    main()
