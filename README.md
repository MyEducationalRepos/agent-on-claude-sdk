# agent-on-claude-sdk

This repository is a compact learning project for rebuilding the behavior of `agent-from-scratch` on top of the Claude Agent SDK harness. The current focus is the MVP scaffold: package layout, project conventions, validation rules, and the documentation that explains how the repo is meant to grow.

## Project Map

- `CLAUDE.md`: active state hub, task index, validators, and commit targets.
- `user-stories.md`: source of truth for scope and acceptance criteria.
- `architecture.md`: the implementation plan and runtime shape.
- `WRITEUP.md`: the 200-word comparison with `agent-from-scratch`.
- `skills/research-summary/SKILL.md`: the reusable research-summary contract.

## Quickstart

1. Create or refresh the local environment:

   ```sh
   uv sync
   ```

2. Run the current focused test slice:

   ```sh
   uv run pytest tests/unit/test_project_metadata.py -q
   ```

3. Use the planned application entrypoint once it lands in the later tasks:

   ```sh
   python -m agent_on_claude_sdk.main
   ```

## Current Status

- The package manifest, lockfile, and source skeleton are in place.
- The CLI entrypoint is planned but not implemented yet, so the command above is the target run path rather than a completed feature.
- Docker support is part of the roadmap and will arrive through the later Dockerfile and compose tasks.

## Reading Order

If you are new to the repo, read `user-stories.md` first, then `architecture.md`, then `CLAUDE.md`. After that, use `WRITEUP.md` for the harness comparison and `skills/research-summary/SKILL.md` for the standard summary output shape.