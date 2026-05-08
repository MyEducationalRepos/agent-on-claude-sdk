# agent-on-claude-sdk

This repository is a compact agent harness for OpenSpec-driven work around the Claude software development kit (SDK). It defines how an artificial intelligence (AI) agent should plan, implement, validate, and archive changes in this project.

The current project is intentionally small. It contains project conventions, OpenSpec workflow prompts, one custom Skill, one write-formatting hook, and a short reflection writeup.

## What Is Included

- `CLAUDE.md`: project conventions for agent workflow, validation, related-link discovery, and commit behavior.
- `WRITEUP.md`: a 200-word reflection on what the harness provides compared with `agent-from-scratch`.
- `.claude/commands/opsx/`: Claude command files for OpenSpec workflows.
- `.claude/skills/`: local Skill definitions, including `research-summary`.
- `.claude/settings.json`: one `PostToolUse` hook that runs `ruff format` on Python files written or edited by the agent.
- `.github/prompts/`: matching prompt files for OpenSpec workflows.
- `openspec/config.yaml`: OpenSpec project configuration.
- `openspec/specs/agent-harness-conventions/spec.md`: the synced main specification for the harness conventions.
- `openspec/changes/archive/`: archived OpenSpec change history.

## Prerequisites

Install or make available:

- Git for source control.
- OpenSpec command-line interface (CLI) for proposal, apply, archive, and validation workflows.
- Claude Code or another compatible agent that reads `.claude` commands, Skills, and settings.
- `jq`, a JavaScript Object Notation (JSON) processor used by the hook command.
- `ruff`, used to format Python files after agent writes.

Check local availability:

```sh
git --version
openspec --version
jq --version
ruff --version
```

## Quick Start

Open the repository and inspect the current OpenSpec state:

```sh
openspec list
openspec list --specs
openspec validate --all --strict --no-interactive
```

Expected current state:

- No active changes.
- One main spec: `agent-harness-conventions`.
- Strict OpenSpec validation passes.

Read the project conventions before making changes:

```sh
sed -n '1,220p' CLAUDE.md
```

## OpenSpec Workflow

Use OpenSpec for planned changes.

### 1. Propose A Change

From the agent chat, run:

```text
/opsx:propose <short description>
```

The proposal workflow creates a change under `openspec/changes/<change-name>/` with these artifacts:

- `proposal.md`: why the change exists.
- `design.md`: how the change will be implemented.
- `specs/**/*.md`: testable requirements.
- `tasks.md`: implementation checklist.

Shell equivalent for starting a change:

```sh
openspec new change "<change-name>"
openspec status --change "<change-name>" --json
```

### 2. Apply A Change

From the agent chat, run:

```text
/opsx:apply <change-name>
```

The apply workflow must:

- Read the context files returned by `openspec instructions apply`.
- Implement pending tasks one by one.
- Mark each task complete in `tasks.md` immediately after completing it.
- Behavior-validate the changed path, not only structured tests.
- Pause only for real blockers, unclear requirements, or design conflicts.

Shell inspection command:

```sh
openspec instructions apply --change "<change-name>" --json
```

### 3. Archive A Change

From the agent chat, run:

```text
/opsx:archive <change-name>
```

For completed changes, archive with spec syncing:

```sh
openspec archive <change-name> --yes
```

This updates `openspec/specs/` from the change delta specs and moves the completed change to `openspec/changes/archive/YYYY-MM-DD-<change-name>/`.

## Research Summary Skill

The project includes one custom Skill at `.claude/skills/research-summary/SKILL.md`.

Use it when the user asks for a research summary, source roundup, literature scan, or related-links synthesis.

Required output shape:

```markdown
## Research Summary

### Question
State the research question in one sentence.

### Key Findings
- Finding with source or path.

### Related Links
- [Label](path-or-url): why it matters.

### Gaps
- What remains unknown or unverified.

### Next Step
One concrete follow-up action.
```

Rules:

- Keep findings brief and evidence-linked.
- Prefer repository-relative paths for local files.
- Separate confirmed facts from assumptions.
- State plainly when no reliable source is available.

## Related Links Workflow

When related references are needed, spawn a Task sub-agent with the objective `find related links`. A uniform resource locator (URL) is a web address; include URLs only when they already exist in repository materials.

Use this prompt shape:

```text
Find related links for the current change. Search repository-local commands,
Skills, prompts, specs, and documentation. Return relevant paths and any URLs
already present in the repository. Do not edit files.
```

Record useful results in the relevant change artifact, `CLAUDE.md`, or a writeup.

Useful local references:

- `.claude/commands/opsx/`
- `.claude/skills/openspec-apply-change/SKILL.md`
- `.claude/skills/openspec-propose/SKILL.md`
- `.github/prompts/opsx-apply.prompt.md`
- `.github/prompts/opsx-propose.prompt.md`
- `openspec/config.yaml`

## Formatting Hook

The hook in `.claude/settings.json` runs after agent write/edit tools:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "file_path=$(jq -r '.tool_input.file_path // empty'); case \"$file_path\" in *.py|*.pyi) ruff format \"$file_path\" ;; esac"
          }
        ]
      }
    ]
  }
}
```

Behavior:

- Python files ending in `.py` or `.pyi` are formatted with `ruff format`.
- Non-Python files are ignored.
- The hook expects the agent tool input to include `tool_input.file_path`.

Validate hook configuration syntax:

```sh
jq empty .claude/settings.json
```

Validate formatter behavior manually:

```sh
printf '%s\n' '{"tool_input":{"file_path":"example.py"}}' \
  | sh -c 'file_path=$(jq -r '\''.tool_input.file_path // empty'\''); case "$file_path" in *.py|*.pyi) ruff format "$file_path" ;; esac'
```

## Validation Checklist

Before considering a change complete, run the checks that match the touched files.

OpenSpec validation:

```sh
openspec validate --all --strict --no-interactive
```

Hook settings validation:

```sh
jq empty .claude/settings.json
```

Python formatting validation:

```sh
ruff format --check .
```

Writeup word count validation, when editing `WRITEUP.md`:

```sh
wc -w WRITEUP.md
```

Behavior validation examples:

- For an OpenSpec workflow change, run the affected `openspec` command.
- For a hook change, run the hook command against a representative JSON payload.
- For a Skill change, verify the Skill file has valid frontmatter and a clear trigger.

## Git Workflow

This repository has been initialized with Git.

Inspect status:

```sh
git status --short
```

Commit only when explicitly requested. Use Conventional Commits, for example:

```sh
git add README.md
git commit -m "docs: add project readme"
```

Never commit secrets, credentials, or `.env` files.

## Troubleshooting

If `openspec list` shows no active changes, create one with `/opsx:propose` or `openspec new change`.

If `ruff format --check .` says no Python files were found, that is acceptable for the current repository state.

If the hook does not format a file, confirm the file path ends with `.py` or `.pyi`, `jq` is installed, `ruff` is installed, and the hook payload includes `tool_input.file_path`.

If an archived change is needed for reference, inspect `openspec/changes/archive/`.