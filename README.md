# agent-on-claude-sdk

A compact learning project that rebuilds the behavior of `agent-from-scratch` on
top of the Claude Agent SDK harness — demonstrating what the SDK removes versus
what you control when you wire the loop yourself.

## Quickstart

```sh
# 1. Install dependencies
uv sync --dev

# 2. Copy env template and add your keys
cp .env.example .env && $EDITOR .env

# 3. Run the agent
bash scripts/run.sh "Summarise the README"
```

See [RUNBOOK.md](RUNBOOK.md) for full setup, Docker, testing, and troubleshooting
instructions.

## Project Map

| File / Directory | Purpose |
|---|---|
| `RUNBOOK.md` | Operational reference — setup, run, test, Docker, CI |
| `CLAUDE.md` | Active state hub — task index, validators, commit log |
| `user-stories.md` | Scope and acceptance criteria |
| `architecture.md` | Implementation plan and runtime shape |
| `WRITEUP.md` | 200-word harness comparison |
| `WHAT_IS_A_HARNESS.md` | Plain-language explainer for learners |
| `src/agent_on_claude_sdk/` | Package source |
| `tests/` | Unit, integration, and e2e test suites |
| `scripts/` | `run.sh`, `verify_behavior.sh`, `check_secrets.sh` |
| `skills/research-summary/` | Reusable research-summary Skill contract |

## Reading Order

New to the repo → `user-stories.md` → `architecture.md` → `CLAUDE.md` →
`WRITEUP.md` → `RUNBOOK.md`.