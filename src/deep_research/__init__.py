"""Framework for running long-horizon GPT-5.1 assisted research pipelines."""

from .config import ResearchConfig
from .llm import LLMClient, OpenAIClient, EchoLLM, Message
from .search import SearchProvider, DuckDuckGoSearch, SearchResult, StaticSearchProvider
from .fetch import WebPageFetcher, PageContent, RequestsFetcher, StaticFetcher
from .planner import QueryPlanner, OutlinePlanner
from .summarizer import Summarizer
from .orchestrator import ResearchOrchestrator, ResearchArtifacts

__all__ = [
    "ResearchConfig",
    "LLMClient",
    "OpenAIClient",
    "EchoLLM",
    "Message",
    "SearchProvider",
    "DuckDuckGoSearch",
    "StaticSearchProvider",
    "SearchResult",
    "WebPageFetcher",
    "RequestsFetcher",
    "StaticFetcher",
    "PageContent",
    "QueryPlanner",
    "OutlinePlanner",
    "Summarizer",
    "ResearchOrchestrator",
    "ResearchArtifacts",
]
