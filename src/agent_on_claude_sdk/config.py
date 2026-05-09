"""Fail-fast settings loader. Reads env vars once at import time."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _optional(name: str, default: str) -> str:
    return os.getenv(name, default)


class Settings:
    """Immutable runtime configuration loaded from the environment."""

    anthropic_api_key: str
    tavily_api_key: str
    model: str
    max_turns: int
    max_result_chars: int

    def __init__(self) -> None:
        self.anthropic_api_key = _require("ANTHROPIC_API_KEY")
        self.tavily_api_key = _require("TAVILY_API_KEY")
        self.model = _optional("MODEL", "claude-3-5-haiku-20241022")
        self.max_turns = int(_optional("MAX_TURNS", "10"))
        self.max_result_chars = int(_optional("MAX_RESULT_CHARS", "4096"))


def load_settings() -> Settings:
    """Load and validate settings; raises RuntimeError on missing secrets."""
    return Settings()
