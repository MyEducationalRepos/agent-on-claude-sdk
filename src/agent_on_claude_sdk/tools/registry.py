"""Tool schema registry and dispatcher."""

from __future__ import annotations

from typing import Any, Callable

# A tool handler is a plain callable: (tool_input: dict) -> str
ToolHandler = Callable[[dict[str, Any]], str]

_registry: dict[str, tuple[dict[str, Any], ToolHandler]] = {}


def register(schema: dict[str, Any], handler: ToolHandler) -> None:
    """Register a tool by its schema and callable handler.

    Args:
        schema: Anthropic-style tool schema with at least a ``name`` key.
        handler: Callable that accepts the tool input dict and returns a string.
    """
    name: str = schema["name"]
    _registry[name] = (schema, handler)


def schemas() -> list[dict[str, Any]]:
    """Return all registered tool schemas (for passing to the Anthropic API)."""
    return [schema for schema, _ in _registry.values()]


def dispatch(name: str, tool_input: dict[str, Any]) -> str:
    """Call the handler registered under *name*.

    Raises:
        KeyError: If no tool with that name is registered.
    """
    if name not in _registry:
        raise KeyError(f"No tool registered: {name!r}")
    _, handler = _registry[name]
    return handler(tool_input)


def clear() -> None:
    """Remove all registered tools (used in tests to reset state)."""
    _registry.clear()
