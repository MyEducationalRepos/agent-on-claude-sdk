## 1. Agent Convention Files

- [x] 1.1 Create root `CLAUDE.md` with concise project conventions for agents, including validation expectations and the related-links delegation workflow.
- [x] 1.2 Create `.claude/skills/research-summary/SKILL.md` defining the `research-summary` Skill trigger and output format.

## 2. Hook Configuration

- [x] 2.1 Inspect existing `.claude` settings and preserve unrelated configuration.
- [x] 2.2 Add one `PostToolUse` hook for file write/edit tools that runs `ruff format` on agent-written Python files.
- [x] 2.3 Behavior-validate the hook by writing or editing a Python file through the supported agent path and confirming `ruff format` runs on that file.

## 3. Sub-Agent Workflow

- [x] 3.1 Spawn one Task-tool sub-agent with the objective `find related links`.
- [x] 3.2 Record the resulting related-links workflow or links in the project conventions or another appropriate repository artifact.

## 4. Writeup

- [x] 4.1 Create `WRITEUP.md` with approximately 200 words on what the harness provided for free compared with `agent-from-scratch`.
- [x] 4.2 Validate the writeup word count and confirm the prose addresses the exact requested topic.

## 5. Final Validation

- [x] 5.1 Run relevant formatting or lint checks for changed files.
- [x] 5.2 Verify every added path matches the spec and no extra Skills, hooks, or unrelated files were introduced.