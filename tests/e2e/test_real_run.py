"""End-to-end test: real CLI path with live API keys.

Skipped automatically when ANTHROPIC_API_KEY or TAVILY_API_KEY are absent.
Run manually:
    ANTHROPIC_API_KEY=... TAVILY_API_KEY=... uv run pytest tests/e2e/test_real_run.py -q -s
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")

needs_keys = pytest.mark.skipif(
    not ANTHROPIC_API_KEY or not TAVILY_API_KEY,
    reason="ANTHROPIC_API_KEY and TAVILY_API_KEY required for e2e tests",
)

REPO_ROOT = Path(__file__).resolve().parents[2]


@needs_keys
def test_real_run_completes(tmp_path: Path):
    """The CLI completes a simple task and writes a run directory with a trace."""
    task = "Write the text 'e2e-ok' to a file named e2e_output.txt"

    result = subprocess.run(
        [sys.executable, "-m", "agent_on_claude_sdk.main", task],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, "RUNS_DIR": str(tmp_path / "runs")},
        timeout=120,
    )

    # Exit 0 = complete, 1 = max_turns (both acceptable — run happened)
    assert result.returncode in (0, 1), (
        f"Unexpected exit {result.returncode}\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )

    # A run directory must exist with a trace
    runs_dir = tmp_path / "runs"
    run_dirs = sorted(runs_dir.iterdir()) if runs_dir.exists() else []
    assert run_dirs, "No run directory created"

    latest = run_dirs[-1]
    trace = latest / "trace.jsonl"
    assert trace.exists(), f"trace.jsonl missing in {latest}"
    events = trace.read_text().strip().splitlines()
    assert len(events) >= 1, "trace.jsonl is empty"

    print(
        f"\n[e2e] run_id={latest.name}  events={len(events)}  exit={result.returncode}"
    )
