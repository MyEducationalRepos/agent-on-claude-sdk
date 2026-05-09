"""Claude Agent SDK harness — orchestration loop and stop-reason handling.

T-020: stop-reason contract constants only.
T-021: full loop implementation.
"""

from __future__ import annotations

# Stop reasons that end the loop (model is done, no more tool calls expected).
TERMINAL_STOP_REASONS: frozenset[str] = frozenset({"end_turn"})

# Stop reason that means the model wants to call tools (loop must continue).
TOOL_USE_STOP_REASON: str = "tool_use"
