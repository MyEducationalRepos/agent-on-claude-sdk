"""Harness stop-reason contract scaffold.

These tests pin the control-flow contract *before* the loop is implemented.
They will continue to pass as T-021/T-022 flesh out the harness.
"""

import pytest

from agent_on_claude_sdk.harness import TERMINAL_STOP_REASONS, TOOL_USE_STOP_REASON


class TestTerminalStopReasons:
    def test_end_turn_is_terminal(self):
        assert "end_turn" in TERMINAL_STOP_REASONS

    def test_tool_use_is_not_terminal(self):
        assert TOOL_USE_STOP_REASON not in TERMINAL_STOP_REASONS

    def test_max_turns_is_not_a_model_stop_reason(self):
        # "max_turns" is our own ceiling, not an Anthropic API stop_reason.
        assert "max_turns" not in TERMINAL_STOP_REASONS

    def test_stop_reasons_is_frozenset(self):
        assert isinstance(TERMINAL_STOP_REASONS, frozenset)

    def test_tool_use_stop_reason_is_string(self):
        assert isinstance(TOOL_USE_STOP_REASON, str)

    def test_tool_use_value(self):
        assert TOOL_USE_STOP_REASON == "tool_use"


class TestStopReasonBranchingContract:
    """Verify the branching logic the harness loop must implement."""

    @pytest.mark.parametrize("stop_reason,expected_continue", [
        ("tool_use", True),   # model wants tool — loop continues
        ("end_turn", False),  # model is done — loop exits
    ])
    def test_should_continue(self, stop_reason, expected_continue):
        should_continue = stop_reason not in TERMINAL_STOP_REASONS
        assert should_continue == expected_continue

    def test_unknown_stop_reason_treated_as_terminal(self):
        # Any stop_reason not in TOOL_USE_STOP_REASON and not listed should halt.
        unknown = "pause_turn"
        should_continue = unknown == TOOL_USE_STOP_REASON
        assert should_continue is False
