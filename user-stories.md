# User Stories

> Generated: 2026-05-08
> Project: agent-on-claude-sdk

---

## Epic: Public Learning Project

### US-001: Open the public harness project

**As a** learner,
**I want to** access a public project that rebuilds the scratch agent with the Claude Agent software development kit (SDK),
**so that** I can compare the harness approach with the from-scratch approach.

**Acceptance Criteria:**
- [ ] The public project is named `agent-on-claude-sdk`.
- [ ] The project names `agent-from-scratch` as the comparison point.
- [ ] A reader can find the conventions, writeup, reusable summary guide, and current stories from the root.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

### US-002: Reproduce the learning agent behavior

**As a** learner,
**I want to** run a harness-based agent that can search, read local text, write an artifact, and stop clearly,
**so that** I can see the same learning outcome delivered with less hand-written control code.

**Acceptance Criteria:**
- [ ] The default run completes with visible progress and a final completion marker.
- [ ] A custom task can ask the agent to search, read, and write during one run.
- [ ] Missing credentials or settings are reported clearly instead of ending silently.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

### US-003: Read project conventions first

**As a** maintainer,
**I want to** see the project conventions at the top level,
**so that** future changes follow the same workflow, validation, and safety rules.

**Acceptance Criteria:**
- [ ] `CLAUDE.md` is visible from the project root.
- [ ] The conventions explain validation, formatting, helper-agent use, related-link discovery, and commit behavior.
- [ ] The conventions warn readers not to overwrite unrelated work or share secrets.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

## Epic: Harness Automation And Reuse

### US-004: Receive automatic formatting after writes

**As a** maintainer,
**I want to** have Python files formatted after the agent writes them,
**so that** shared examples stay tidy without manual cleanup.

**Acceptance Criteria:**
- [ ] A Python file written by the agent is passed to `ruff format`.
- [ ] A non-Python file written by the agent is ignored by the formatter.
- [ ] If `ruff` is unavailable, the failure is visible to the operator.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

### US-005: Use a standard research summary

**As a** researcher,
**I want to** use a reusable research-summary format,
**so that** findings from different sessions are easy to compare.

**Acceptance Criteria:**
- [ ] A Skill folder contains `SKILL.md` for `research-summary`.
- [ ] The summary format includes the question, key findings, related links, evidence gaps, and next step.
- [ ] Missing or unverified evidence is labeled plainly.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

### US-006: Delegate related-link discovery

**As a** researcher,
**I want to** ask a separate helper agent to find related links,
**so that** source discovery stays focused and easy to review.

**Acceptance Criteria:**
- [ ] The helper is given the objective `find related links`.
- [ ] The helper returns useful local paths and relevant external links when available.
- [ ] The helper does not change project files while searching.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

## Epic: Public Sharing And Safety

### US-007: Keep shared materials clean

**As a** maintainer,
**I want to** keep local clutter out while keeping agent materials visible,
**so that** the public project stays clean and complete.

**Acceptance Criteria:**
- [ ] Local system files, caches, generated traces, and secret files are excluded from the shared project state.
- [ ] Example settings contain placeholders only.
- [ ] A status check does not show local cache or secret files as pending work.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

### US-008: Verify behavior, not only structure

**As a** project owner,
**I want to** confirm the agent works through a real run,
**so that** the deliverable is proven by behavior instead of file presence alone.

**Acceptance Criteria:**
- [ ] A successful run shows the agent searching, reading, writing, and stopping clearly.
- [ ] The produced artifact matches the task given to the agent.
- [ ] A failed run names the missing setting, file, or command that blocked completion.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

### US-009: Find useful references quickly

**As a** course instructor,
**I want to** see related project materials listed clearly,
**so that** I can point students to the right comparison files and links.

**Acceptance Criteria:**
- [ ] The references include the scratch-agent comparison, conventions, research-summary guide, writeup, and blog-post work.
- [ ] References are grouped as local paths and external links.
- [ ] If no external link is available yet, the project states that plainly.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

## Epic: Phase 1 Reflection And Publication

### US-010: Read the 200-word comparison

**As a** technical reader,
**I want to** read a concise comparison of the harness and `agent-from-scratch`,
**so that** I understand what the harness saves me from building manually.

**Acceptance Criteria:**
- [ ] The writeup is exactly 200 words.
- [ ] The writeup compares the harness with `agent-from-scratch`.
- [ ] The writeup is understandable without reading the source code first.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

### US-011: Verify the Phase 1b deliverable

**As a** project owner,
**I want to** verify the Phase 1b deliverable in one place,
**so that** I can confirm the public project and 200-word writeup are complete.

**Acceptance Criteria:**
- [ ] The project is named `agent-on-claude-sdk`.
- [ ] The rebuild includes conventions, a research-summary Skill, automatic formatting after agent writes, helper-agent link discovery, and a 200-word writeup.
- [ ] The verification note clearly marks the Phase 1b deliverable as complete or blocked.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.

### US-012: Learn the harness idea before the deadline

**As a** blog reader,
**I want to** read "From-scratch vs Claude Agent SDK: what a harness is" before May 25,
**so that** I can learn the concept while the Phase 1 work is fresh.

**Acceptance Criteria:**
- [ ] The post explains what a harness is in plain language.
- [ ] The post contrasts the from-scratch path with the Claude Agent SDK path.
- [ ] The post is ready to publish before 2026-05-25.

**INVEST check:** Independent, negotiable, valuable, estimable, small, and testable.