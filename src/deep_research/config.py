from dataclasses import dataclass, field
from typing import List


@dataclass
class ResearchConfig:
    """Configuration controlling research behavior and budgets."""

    model: str = "gpt-5.1"
    temperature: float = 0.2
    max_output_tokens: int = 6000
    search_results: int = 12
    max_search_rounds: int = 3
    max_tool_calls: int = 64
    concurrent_requests: int = 3
    request_timeout: int = 30
    report_word_target: int = 12000
    outline_depth: int = 3
    include_full_sources: bool = True
    system_prompt: str = field(
        default_factory=lambda: (
            "You are an elite research analyst combining rigorous reasoning, data analysis, "
            "and meticulous citation discipline. Your job is to design and execute a "
            "multi-stage research plan, aggressively using tools (search, browsing, code) "
            "to gather evidence. Always cite sources inline in square brackets and "
            "prioritize factual accuracy."
        )
    )
    safety_warnings: List[str] = field(
        default_factory=lambda: [
            "Confirm data sources before drawing conclusions.",
            "Note assumptions and gaps explicitly.",
            "Prefer primary data and recent publications.",
        ]
    )

    def extended_brief(self) -> str:
        warnings = "\n".join(f"- {item}" for item in self.safety_warnings)
        return (
            f"Model: {self.model}\n"
            f"Temperature: {self.temperature}\n"
            f"Max output tokens: {self.max_output_tokens}\n"
            f"Tool calls allowed: {self.max_tool_calls}\n"
            f"Search results per query: {self.search_results}\n"
            f"Max search rounds: {self.max_search_rounds}\n"
            f"Report target words: {self.report_word_target}\n"
            f"Outline depth: {self.outline_depth}\n"
            f"Operational safety:\n{warnings}"
        )
