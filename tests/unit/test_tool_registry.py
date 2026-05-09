"""Unit tests for the tool schema registry and dispatcher."""

import pytest

import agent_on_claude_sdk.tools as tools


@pytest.fixture(autouse=True)
def clean_registry():
    """Reset the global registry before and after every test."""
    tools.clear()
    yield
    tools.clear()


def _echo_handler(tool_input: dict) -> str:
    return tool_input.get("text", "")


_ECHO_SCHEMA = {
    "name": "echo",
    "description": "Returns the input text unchanged.",
    "input_schema": {
        "type": "object",
        "properties": {"text": {"type": "string"}},
        "required": ["text"],
    },
}


class TestRegisterAndSchemas:
    def test_empty_by_default(self):
        assert tools.schemas() == []

    def test_registered_schema_appears(self):
        tools.register(_ECHO_SCHEMA, _echo_handler)
        assert any(s["name"] == "echo" for s in tools.schemas())

    def test_multiple_tools(self):
        tools.register(_ECHO_SCHEMA, _echo_handler)
        tools.register({**_ECHO_SCHEMA, "name": "other"}, _echo_handler)
        assert len(tools.schemas()) == 2

    def test_schema_content_preserved(self):
        tools.register(_ECHO_SCHEMA, _echo_handler)
        schema = next(s for s in tools.schemas() if s["name"] == "echo")
        assert schema["description"] == "Returns the input text unchanged."


class TestDispatch:
    def test_calls_handler(self):
        tools.register(_ECHO_SCHEMA, _echo_handler)
        result = tools.dispatch("echo", {"text": "hello"})
        assert result == "hello"

    def test_unknown_tool_raises(self):
        with pytest.raises(KeyError, match="no_such_tool"):
            tools.dispatch("no_such_tool", {})

    def test_handler_return_is_string(self):
        tools.register(_ECHO_SCHEMA, _echo_handler)
        assert isinstance(tools.dispatch("echo", {"text": "x"}), str)


class TestClear:
    def test_clear_empties_registry(self):
        tools.register(_ECHO_SCHEMA, _echo_handler)
        tools.clear()
        assert tools.schemas() == []
