"""CLI entrypoint for the agent-on-claude-sdk harness."""

from __future__ import annotations

import sys
from pathlib import Path

from agent_on_claude_sdk.config import load_settings
from agent_on_claude_sdk.harness import run
from agent_on_claude_sdk.models import RunRecord
from agent_on_claude_sdk.persistence.fs_store import FsStore
from agent_on_claude_sdk.tracing import Tracer
import agent_on_claude_sdk.tools as tool_registry
from agent_on_claude_sdk.tools.read_file import (
    SCHEMA as READ_SCHEMA,
    handler as read_handler,
)
from agent_on_claude_sdk.tools.write_file import (
    SCHEMA as WRITE_SCHEMA,
    handler as write_handler,
)
from agent_on_claude_sdk.tools.web_search import (
    SCHEMA as SEARCH_SCHEMA,
    handler as search_handler,
)

_RUNS_ROOT = Path("runs")


def _register_tools() -> None:
    tool_registry.clear()
    tool_registry.register(READ_SCHEMA, read_handler)
    tool_registry.register(WRITE_SCHEMA, write_handler)
    tool_registry.register(SEARCH_SCHEMA, search_handler)


def main(argv: list[str] | None = None) -> int:
    """Run the agent for a task given on the command line.

    Usage: python -m agent_on_claude_sdk.main <task string>
    """
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("Usage: python -m agent_on_claude_sdk.main <task>", file=sys.stderr)
        return 1

    task = " ".join(args)

    try:
        settings = load_settings()
    except RuntimeError as exc:
        print(f"[config error] {exc}", file=sys.stderr)
        return 2

    _register_tools()

    record = RunRecord(task=task, model=settings.model)
    store = FsStore(_RUNS_ROOT)
    tracer = Tracer(store.run_dir(record.run_id))

    print(f"run_id: {record.run_id}")
    print(f"task:   {task}")
    print(f"model:  {settings.model}")
    print("---")

    result = run(task, settings=settings, tracer=tracer, record=record, store=store)

    print(f"status:      {result.status.value}")
    print(f"turns_used:  {result.turns_count}")
    if result.error_summary:
        print(f"error:       {result.error_summary}")

    return 0 if result.status.value == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
