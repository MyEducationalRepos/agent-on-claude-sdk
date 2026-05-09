# Runbook — agent-on-claude-sdk

Operational reference for setting up, running, testing, and troubleshooting the
harness locally and in Docker.

---

## 1. Prerequisites

| Tool | Minimum version | Install |
|---|---|---|
| Python | 3.12 | [python.org](https://www.python.org/) |
| uv | latest | `pip install uv` or `brew install uv` |
| Docker (optional) | 24+ | [docs.docker.com](https://docs.docker.com/) |
| Anthropic API key | — | [console.anthropic.com](https://console.anthropic.com/) |
| Tavily API key | — | [app.tavily.com](https://app.tavily.com/) |

---

## 2. First-time Setup

```sh
# Clone and enter the repo
git clone <repo-url>
cd agent-on-claude-sdk

# Create the virtual environment and install all dependencies
uv sync --dev

# Copy the environment template and fill in your keys
cp .env.example .env
$EDITOR .env
```

`.env` must contain at minimum:

```
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...
```

---

## 3. Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | — | Anthropic API key for Claude |
| `TAVILY_API_KEY` | Yes | — | Tavily API key for web search |
| `MODEL` | No | `claude-3-5-haiku-20241022` | Claude model identifier |
| `MAX_TURNS` | No | `10` | Maximum agent loop iterations |
| `MAX_RESULT_CHARS` | No | `4096` | Truncation limit for tool results |

The harness fails fast at startup if a required variable is missing.

---

## 4. Running the Agent

### Via the run script (recommended)

```sh
bash scripts/run.sh "Summarise the README"
bash scripts/run.sh "Search the web for the latest Anthropic news"
bash scripts/run.sh "Write 'hello' to a file named out.txt"
```

### Directly via Python

```sh
uv run python -m agent_on_claude_sdk.main "Your task here"
```

### Exit codes

| Code | Meaning |
|---|---|
| `0` | Run completed (`end_turn`) |
| `1` | Run ended with `max_turns` or an unhandled stop reason |
| `2` | Configuration error — missing required env var |

---

## 5. Run Artifacts

Every run writes its output to `runs/<run-id>/`:

```
runs/
└── 20260509T120000-abc12345/
    ├── record.json      # RunRecord with task, model, status, timestamps
    └── trace.jsonl      # Append-only log of every event (one JSON object per line)
```

`trace.jsonl` event types: `run_start`, `turn_start`, `turn_end`, `tool_call`,
`tool_result`, `done`.

---

## 6. Running Tests

```sh
# Unit tests only (no keys required)
uv run pytest tests/unit -q

# Integration tests (no live API calls; uses mocked Anthropic client)
uv run pytest tests/integration -q

# Both together (what CI runs)
uv run pytest tests/unit tests/integration -q

# End-to-end test (requires live keys)
ANTHROPIC_API_KEY=... TAVILY_API_KEY=... uv run pytest tests/e2e -q -s
```

---

## 7. Linting and Formatting

```sh
# Check for lint errors
uv run ruff check .

# Auto-fix lint errors
uv run ruff check --fix .

# Check formatting
uv run ruff format --check .

# Apply formatting
uv run ruff format .
```

---

## 8. Docker

### Build

```sh
docker build -t agent-on-claude-sdk .
```

### Run a task

```sh
docker run --rm \
  --env-file .env \
  -v "$(pwd)/runs:/app/runs" \
  agent-on-claude-sdk \
  "Summarise the README"
```

### docker compose (includes optional PostgreSQL metadata store)

```sh
# Agent only
docker compose up agent

# Agent + PostgreSQL metadata store
docker compose --profile metadata up
```

---

## 9. Validation Scripts

### Secret guard

Scans tracked and untracked files for leaked credentials (excludes test fixtures
and CI placeholders):

```sh
bash scripts/check_secrets.sh
```

Exits `0` on PASS, `1` if any real secret pattern is found.

### Behavior validation

Runs the real CLI path end-to-end and confirms a run directory + trace are written:

```sh
ANTHROPIC_API_KEY=... TAVILY_API_KEY=... bash scripts/verify_behavior.sh
```

Exits `0` on PASS or SKIP (no keys), `1` on FAIL.

---

## 10. CI

GitHub Actions (`.github/workflows/ci.yml`) runs on every push and pull request
to `main`:

1. `uv sync --dev`
2. `ruff check .`
3. `ruff format --check .`
4. `pytest tests/unit tests/integration -q`

End-to-end tests are **not** run in CI (no live keys). Run them manually before
merging work that touches the harness loop or tools.

---

## 11. Project Layout

```
src/agent_on_claude_sdk/
├── __init__.py
├── config.py          # Fail-fast settings loader
├── harness.py         # Claude Agent SDK orchestration loop
├── main.py            # CLI entrypoint
├── models.py          # RunRecord, TraceEvent, RunStatus, ToolResult
├── tracing.py         # Append-only Tracer
├── validation.py      # Post-write ruff formatter hook
├── helpers/
│   ├── related_links.py      # Local-path + external-link collector
│   └── research_summary.py   # Research-summary formatter (Skill contract)
├── persistence/
│   ├── fs_store.py    # Filesystem run store (MVP)
│   └── pg_store.py    # PostgreSQL adapter stub (future)
└── tools/
    ├── registry.py    # Schema registry + dispatcher
    ├── read_file.py   # Read a file from the working directory
    ├── web_search.py  # Tavily web search
    └── write_file.py  # Write a file (cwd-bounded)
```

---

## 12. Troubleshooting

### `RuntimeError: missing required env var: ANTHROPIC_API_KEY`

`.env` is not loaded or the key is missing. Confirm `.env` exists with a valid
key and that `python-dotenv` is installed (`uv sync --dev`).

### `ModuleNotFoundError: No module named 'agent_on_claude_sdk'`

Run via `uv run python -m ...` or activate the venv (`source .venv/bin/activate`)
before using `python` directly.

### Docker build fails at `uv sync`

The `Dockerfile` copies `src/` and `pyproject.toml` together before syncing.
If you customise the Dockerfile, keep `COPY src/ src/` before `RUN uv sync`.

### Trace file is empty after a run

The run likely errored before emitting events. Check the `record.json` field
`error_summary` and the process stderr for the exit code.
