## Context

The repository currently has OpenSpec scaffolding and a `.claude/` area, but no root `CLAUDE.md`, no project Skill for a reusable research-summary format, no file-write formatting hook, and no requested comparison writeup. The change is a lightweight agent harness bootstrap that should remain easy to inspect and run locally on macOS.

## Goals / Non-Goals

**Goals:**
- Establish root-level agent conventions in `CLAUDE.md`.
- Define a single custom Skill named `research-summary` in its own Skill folder.
- Configure one `PostToolUse` hook that formats agent-written Python files with `ruff format`.
- Include a Task-tool sub-agent workflow for finding related links.
- Produce `WRITEUP.md` at approximately 200 words on the requested comparison topic.

**Non-Goals:**
- Do not add unrelated Skills, agents, hooks, or broad automation.
- Do not change application runtime behavior outside agent customization files.
- Do not install dependencies or commit changes as part of implementation.

## Decisions

- Store project conventions in root `CLAUDE.md` so agent tools discover them without needing workspace-specific prompts. Alternative: keep conventions only under `.claude/`, but that is less visible to readers at the repository root.
- Place the Skill at `.claude/skills/research-summary/SKILL.md` to match the existing Claude Skill folder convention. Alternative: use a prompt file, but the request explicitly asks for a Skill folder.
- Configure the hook in `.claude/settings.json` unless an existing settings file requires merging into another supported settings path. Alternative: use a shell wrapper, but a native `PostToolUse` hook keeps the behavior tied to agent writes.
- Limit the hook matcher to file-write/edit tools and run `ruff format` only on Python paths to avoid formatting unsupported file types. Alternative: run on every written file, but `ruff format` is Python-focused and would fail noisily on markdown or JSON.
- Represent the Task-tool sub-agent invocation as a documented, runnable workflow step in `CLAUDE.md` or a small agent-facing command note, because the repository should preserve how to spawn the sub-agent for "find related links" without requiring live execution during static implementation.

## Risks / Trade-offs

- `ruff` unavailable on a contributor machine -> Document the dependency and let the hook fail visibly rather than silently skipping formatting.
- Hook command receives paths in an unexpected payload shape -> Keep the hook command narrow and test it against an agent-written Python file during implementation.
- Existing `.claude/settings.json` may already contain hooks -> Merge conservatively and preserve unrelated settings.
- The 200-word writeup can drift from the requested length -> Validate word count during implementation.