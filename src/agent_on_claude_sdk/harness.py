"""Claude Agent SDK harness — orchestration loop and stop-reason handling."""

from __future__ import annotations

from typing import Any

import anthropic

from agent_on_claude_sdk.models import RunRecord, RunStatus, ToolResult, TraceEvent
from agent_on_claude_sdk.persistence.fs_store import FsStore
from agent_on_claude_sdk.tracing import Tracer
import agent_on_claude_sdk.tools as tool_registry

# Stop reasons that end the loop (model is done, no more tool calls expected).
TERMINAL_STOP_REASONS: frozenset[str] = frozenset({"end_turn"})

# Stop reason that means the model wants to call tools (loop must continue).
TOOL_USE_STOP_REASON: str = "tool_use"


def run(
    task: str,
    settings: Any,
    tracer: Tracer,
    record: RunRecord,
    *,
    store: FsStore | None = None,
    client: anthropic.Anthropic | None = None,
) -> RunRecord:
    """Run the agent loop for *task* until done, max_turns, or error.

    Args:
        task: The user task string.
        settings: A ``Settings`` instance with model/max_turns/max_result_chars.
        tracer: A ``Tracer`` instance for the current run.
        record: A ``RunRecord`` (status=running) to update in place.
        store: Optional ``FsStore`` — if given, persists the record at start and finish.
        client: Optional pre-built Anthropic client (for testing).

    Returns:
        The mutated ``record`` with final status set.
    """
    if client is None:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    if store is not None:
        store.save(record)

    messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
    tracer.emit(TraceEvent(event_type="run_start", turn=0, content={"task": task}))

    for turn in range(1, settings.max_turns + 1):
        record.turns_count = turn
        tracer.emit(TraceEvent(event_type="turn_start", turn=turn, content={}))

        response = client.messages.create(
            model=settings.model,
            max_tokens=1024,
            tools=tool_registry.schemas(),
            messages=messages,
        )

        stop_reason: str = response.stop_reason or "end_turn"
        tracer.emit(
            TraceEvent(
                event_type="turn_end",
                turn=turn,
                content={"stop_reason": stop_reason},
            )
        )

        if stop_reason in TERMINAL_STOP_REASONS:
            record.finish(RunStatus.complete)
            tracer.emit(TraceEvent(event_type="done", turn=turn, content={"status": "complete"}))
            if store is not None:
                store.save(record)
            return record

        if stop_reason != TOOL_USE_STOP_REASON:
            # Unrecognised stop reason — halt safely.
            record.finish(RunStatus.error, error_summary=f"unhandled stop_reason: {stop_reason}")
            tracer.emit(TraceEvent(event_type="done", turn=turn, content={"status": "error"}))
            if store is not None:
                store.save(record)
            return record

        # --- tool_use branch: dispatch all tool calls, collect results ---
        messages.append({"role": "assistant", "content": response.content})

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        tool_results: list[dict[str, Any]] = []

        for block in tool_uses:
            tracer.emit(
                TraceEvent(
                    event_type="tool_call",
                    turn=turn,
                    content={"name": block.name, "input": block.input},
                )
            )
            try:
                raw = tool_registry.dispatch(block.name, block.input)
                truncated = raw[: settings.max_result_chars]
                result = ToolResult(tool_use_id=block.id, content=truncated)
            except Exception as exc:  # noqa: BLE001
                result = ToolResult(
                    tool_use_id=block.id,
                    content=f"[error] {exc}",
                    is_error=True,
                )
            tracer.emit(
                TraceEvent(
                    event_type="tool_result",
                    turn=turn,
                    content={
                        "tool_use_id": result.tool_use_id,
                        "is_error": result.is_error,
                        "content": result.content,
                    },
                )
            )
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": result.tool_use_id,
                    "content": result.content,
                    "is_error": result.is_error,
                }
            )

        # Single follow-up message with all tool results (Anthropic contract).
        messages.append({"role": "user", "content": tool_results})

    # Loop exhausted without a terminal stop reason.
    record.finish(RunStatus.max_turns)
    tracer.emit(TraceEvent(event_type="done", turn=settings.max_turns, content={"status": "max_turns"}))
    if store is not None:
        store.save(record)
    return record
