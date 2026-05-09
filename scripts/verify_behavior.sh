#!/usr/bin/env bash
# Behavior validation: run the real CLI path and confirm a run ID + artifact land.
# Exits 0 on PASS or SKIP (no keys); 1 on FAIL.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# ── key guard ─────────────────────────────────────────────────────────────────
if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
    echo "SKIP: ANTHROPIC_API_KEY not set — skipping behavior validation"
    exit 0
fi
if [[ -z "${TAVILY_API_KEY:-}" ]]; then
    echo "SKIP: TAVILY_API_KEY not set — skipping behavior validation"
    exit 0
fi

# ── run ────────────────────────────────────────────────────────────────────────
TASK="Write the text 'behavior-check-ok' to a file named verify_output.txt"
echo "[verify] running: python -m agent_on_claude_sdk.main \"${TASK}\""

set +e
uv run python -m agent_on_claude_sdk.main "${TASK}"
EXIT_CODE=$?
set -e

# ── checks ────────────────────────────────────────────────────────────────────
# 1. exit code must be 0 (complete) or 1 (max_turns reached but ran)
if [[ "${EXIT_CODE}" -eq 2 ]]; then
    echo "FAIL: harness exited with config error (exit 2)"
    exit 1
fi

# 2. a run directory must exist with a trace
LATEST_RUN="$(ls -td runs/*/ 2>/dev/null | head -1 || true)"
if [[ -z "${LATEST_RUN}" ]]; then
    echo "FAIL: no run directory found under runs/"
    exit 1
fi

RUN_ID="$(basename "${LATEST_RUN}")"
TRACE="${LATEST_RUN}trace.jsonl"

if [[ ! -f "${TRACE}" ]]; then
    echo "FAIL: trace.jsonl missing in ${LATEST_RUN}"
    exit 1
fi

echo "PASS"
echo "  Run ID   : ${RUN_ID}"
echo "  Trace    : ${TRACE} ($(wc -l < "${TRACE}") events)"
echo "  Exit code: ${EXIT_CODE}"
