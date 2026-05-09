"""Unit tests for the web_search tool (Tavily mocked — no live API calls)."""

from unittest.mock import MagicMock, patch

import pytest

from agent_on_claude_sdk.tools import web_search as ws


@pytest.fixture(autouse=True)
def reset_client():
    ws._reset_client()
    yield
    ws._reset_client()


class TestSchema:
    def test_name(self):
        assert ws.SCHEMA["name"] == "web_search"

    def test_required_query(self):
        assert "query" in ws.SCHEMA["input_schema"]["required"]


class TestHandlerNoApiKey:
    def test_missing_key_returns_error(self, monkeypatch):
        monkeypatch.delenv("TAVILY_API_KEY", raising=False)
        result = ws.handler({"query": "test"})
        assert result.startswith("[error]")
        assert "TAVILY_API_KEY" in result


class TestHandlerWithResults:
    def _make_client(self, results):
        mock = MagicMock()
        mock.search.return_value = {"results": results}
        return mock

    def test_formats_results(self, monkeypatch):
        monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")
        fake = self._make_client([
            {"title": "T1", "url": "https://a.com", "content": "body1"},
            {"title": "T2", "url": "https://b.com", "content": "body2"},
        ])
        with patch("agent_on_claude_sdk.tools.web_search._get_client", return_value=fake):
            result = ws.handler({"query": "python"})
        assert "T1" in result
        assert "https://a.com" in result
        assert "body2" in result

    def test_empty_results_returns_no_results(self, monkeypatch):
        monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")
        fake = self._make_client([])
        with patch("agent_on_claude_sdk.tools.web_search._get_client", return_value=fake):
            result = ws.handler({"query": "nothing"})
        assert "No results" in result

    def test_api_exception_returns_error(self, monkeypatch):
        monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")
        mock = MagicMock()
        mock.search.side_effect = RuntimeError("timeout")
        with patch("agent_on_claude_sdk.tools.web_search._get_client", return_value=mock):
            result = ws.handler({"query": "fail"})
        assert result.startswith("[error]")
        assert "timeout" in result

    def test_returns_string(self, monkeypatch):
        monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")
        fake = self._make_client([{"title": "x", "url": "u", "content": "c"}])
        with patch("agent_on_claude_sdk.tools.web_search._get_client", return_value=fake):
            assert isinstance(ws.handler({"query": "q"}), str)
