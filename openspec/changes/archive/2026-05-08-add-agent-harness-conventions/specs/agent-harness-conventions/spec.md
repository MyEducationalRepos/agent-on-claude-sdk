## ADDED Requirements

### Requirement: Project conventions document
The repository SHALL include a root `CLAUDE.md` that defines concise project conventions for agents working in this repository.

#### Scenario: Agent reads conventions
- **WHEN** an agent starts work in the repository
- **THEN** the root `CLAUDE.md` provides the project conventions needed to guide file edits, validation, and communication

### Requirement: Research summary Skill
The repository SHALL include exactly one Skill folder for `research-summary` with a `SKILL.md` that defines the required research-summary output format.

#### Scenario: Skill format is available
- **WHEN** an agent needs to produce a research summary
- **THEN** `.claude/skills/research-summary/SKILL.md` describes the output structure and usage trigger

### Requirement: Ruff formatting hook
The repository SHALL include one `PostToolUse` hook that runs `ruff format` on Python files written or edited by the agent.

#### Scenario: Agent writes Python file
- **WHEN** the agent writes or edits a Python file through a file-writing tool
- **THEN** the hook invokes `ruff format` for that file

### Requirement: Related links sub-agent workflow
The repository SHALL document or configure a Task-tool sub-agent invocation for the task named `find related links`.

#### Scenario: Link discovery is delegated
- **WHEN** an agent follows the project workflow for related link discovery
- **THEN** it can spawn a Task-tool sub-agent with the objective `find related links`

### Requirement: Harness comparison writeup
The repository SHALL include `WRITEUP.md` containing approximately 200 words on "What the harness gave me for free that I wrote myself in agent-from-scratch."

#### Scenario: Writeup exists
- **WHEN** a reader opens `WRITEUP.md`
- **THEN** it contains the requested comparison topic in prose near the requested length