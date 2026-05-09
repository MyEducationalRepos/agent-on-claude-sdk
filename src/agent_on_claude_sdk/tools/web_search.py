"""web_search tool — Tavily-backed web search.

External API failures are normalized into error strings so the model can
react gracefully without crashing the harness.
"""

from __future__ import annotations

import os
from typing import Any

SCHEMA: dict[str, Any] = {
    "name": "web_search",
    "description": "Search the web via Tavily and return up to 5 results as plain text.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query string.",
            }
        },
        "required": ["query"],
    },
}

# Module-level client cache; populated lazily on first use.
_client: Any = None


def _get_client() -> Any | None:
    global _client
    if _client is not None:
        return _client
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return None
    from tavily import TavilyClient

    _client = TavilyClient(api_key=api_key)
    return _client


def _reset_client() -> None:
    """Force the next call to re-create the client (used in tests)."""
    global _client
    _client = None


def handler(tool_input: dict[str, Any]) -> str:
    """Search Tavily for *tool_input['query']* and return formatted results.

    Returns an ``[error]`` string on missing API key or network failure.
    """
    query: str = tool_input["query"]
    client = _get_client()
    if client is None:
        return "[error] TAVILY_API_KEY is not set"
    try:
        response = client.search(query=query, max_results=5)
        results = response.get("results", []) if isinstance(response, dict) else []
        if not results:
            return "No results found."
        return "\n\n".join(
            f"{item.get('title', '')}\n{item.get('url', '')}\n{item.get('content', '')}"
            for item in results
        )
    except Exception as exc:  # noqa: BLE001
        return f"[error] web search failed: {exc}"
