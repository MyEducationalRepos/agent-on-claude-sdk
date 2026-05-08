# Project Conventions

## Workflow

- Use OpenSpec for planned changes. Start with `/opsx:propose`, implement with `/opsx:apply`, and archive with `/opsx:archive` when the change is complete.
- Keep edits minimal, scoped to the active OpenSpec task, and consistent with the existing `.claude` command and Skill layout.
- Preserve user changes. Do not reset, overwrite, or remove unrelated files.
- Use Conventional Commits if a commit is requested.

## Validation

- Structured tests are required when behavior is risky, but they are not enough by themselves.
- Behavior-validate the actual path the task changes: run the command, hook, script, or workflow that demonstrates the acceptance criteria.
- When fixing a bug, reproduce it first, then patch, then rerun the focused validation.
- For Python formatting, use `ruff format` through the configured `PostToolUse` hook or directly when validating changed Python files.

## Related Links Task

When related references are needed, spawn a Task sub-agent with the objective `find related links`.

Use this prompt shape:

```text
Find related links for the current change. Search repository-local commands,
Skills, prompts, specs, and documentation. Return relevant paths and any URLs
already present in the repository. Do not edit files.
```

Record useful results in the relevant change artifact or writeup. Current local references:

- `.claude/commands/opsx/`
- `.claude/skills/openspec-apply-change/SKILL.md`
- `.claude/skills/openspec-propose/SKILL.md`
- `.github/prompts/opsx-apply.prompt.md`
- `.github/prompts/opsx-propose.prompt.md`
- `openspec/config.yaml`

No external URLs were found in the repository during the initial related-links task.