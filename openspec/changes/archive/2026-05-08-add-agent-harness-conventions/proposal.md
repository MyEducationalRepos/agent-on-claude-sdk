## Why

The project needs a small, explicit agent harness layer so future agent runs share the same conventions, output format, formatting behavior, and delegation pattern. Capturing this in OpenSpec keeps the requested scaffold reproducible before implementation.

## What Changes

- Add a root `CLAUDE.md` that records project conventions for agents working in this repository.
- Add one Skill folder containing `SKILL.md` for a `research-summary` output format.
- Add one `PostToolUse` hook that runs `ruff format` on files written by the agent.
- Add a Task-tool sub-agent invocation for finding related links.
- Add a 200-word `WRITEUP.md` comparing what the harness provides for free with what was manually built in `agent-from-scratch`.

## Capabilities

### New Capabilities
- `agent-harness-conventions`: Defines the repository-level agent convention file, custom research-summary Skill, write-formatting hook, Task sub-agent link discovery workflow, and writeup deliverable.

### Modified Capabilities

## Impact

- Affected files: root agent documentation, `.claude/skills/`, `.claude/settings` or equivalent hook configuration, and `WRITEUP.md`.
- Affected workflows: agent file-writing behavior and delegated research/link discovery tasks.
- Dependencies: `ruff` must be available wherever the PostToolUse hook runs.