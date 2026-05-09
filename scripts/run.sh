#!/usr/bin/env bash
# scripts/run.sh — Run the agent harness for a task string.
# Usage: bash scripts/run.sh "your task here"
#        bash scripts/run.sh --help
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

usage() {
  cat <<EOF
Usage: $(basename "$0") <task>

Run the agent-on-claude-sdk harness for the given task string.

Options:
  --help    Show this message and exit.

Environment:
  ANTHROPIC_API_KEY   Required. Anthropic API key.
  TAVILY_API_KEY      Required. Tavily search API key.
  MODEL               Optional. Claude model (default: claude-3-5-haiku-20241022).
  MAX_TURNS           Optional. Maximum agent turns (default: 10).

Examples:
  bash scripts/run.sh "Summarise the README"
  bash scripts/run.sh "Search the web for the latest anthropic news"
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

if [[ $# -eq 0 ]]; then
  echo "Error: task string is required." >&2
  echo "" >&2
  usage >&2
  exit 1
fi

cd "${REPO_ROOT}"
exec uv run python -m agent_on_claude_sdk.main "$@"
