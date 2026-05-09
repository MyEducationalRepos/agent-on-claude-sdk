"""Unit tests for config loading and fail-fast validation."""

import os
import pytest

from agent_on_claude_sdk.config import Settings, load_settings


def _set_valid_env(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")


class TestSettingsDefaults:
    def test_defaults(self, monkeypatch):
        _set_valid_env(monkeypatch)
        monkeypatch.delenv("MODEL", raising=False)
        monkeypatch.delenv("MAX_TURNS", raising=False)
        monkeypatch.delenv("MAX_RESULT_CHARS", raising=False)
        s = Settings()
        assert s.model == "claude-3-5-haiku-20241022"
        assert s.max_turns == 10
        assert s.max_result_chars == 4096

    def test_overrides(self, monkeypatch):
        _set_valid_env(monkeypatch)
        monkeypatch.setenv("MODEL", "claude-opus-4-5")
        monkeypatch.setenv("MAX_TURNS", "5")
        monkeypatch.setenv("MAX_RESULT_CHARS", "1024")
        s = Settings()
        assert s.model == "claude-opus-4-5"
        assert s.max_turns == 5
        assert s.max_result_chars == 1024

    def test_secrets_stored(self, monkeypatch):
        _set_valid_env(monkeypatch)
        s = Settings()
        assert s.anthropic_api_key == "sk-ant-test"
        assert s.tavily_api_key == "tvly-test"


class TestFailFast:
    def test_missing_anthropic_key(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")
        with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
            Settings()

    def test_missing_tavily_key(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
        monkeypatch.delenv("TAVILY_API_KEY", raising=False)
        with pytest.raises(RuntimeError, match="TAVILY_API_KEY"):
            Settings()

    def test_empty_string_treated_as_missing(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "")
        monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")
        with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
            Settings()


class TestLoadSettings:
    def test_returns_settings(self, monkeypatch):
        _set_valid_env(monkeypatch)
        s = load_settings()
        assert isinstance(s, Settings)
