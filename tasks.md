# MVP Task List

> Project: agent-on-claude-sdk
> Generated: 2026-05-09
> Total tasks: 39

---

## Phase 1: Project Bootstrap And Public Assets

### T-001: Create the Python project manifest

**User story ref:** Architecture: Stack Summary, File & Folder Structure, Testing Strategy
**Start condition:** The repository contains `architecture.md` and `user-stories.md` only as planning inputs.
**End condition:** `pyproject.toml` declares `agent-on-claude-sdk`, `requires-python = ">=3.12"`, runtime dependencies, dev tooling, and `uv.lock` exists.

**Test first:**
- [ ] Create `tests/unit/test_project_metadata.py::test_project_metadata_and_dependencies`; run `uv run pytest tests/unit/test_project_metadata.py -q`; assert it fails before `pyproject.toml` and `uv.lock` exist and passes after both files are present.
- [ ] Run `uv sync`; assert dependency resolution completes without errors.

**Implementation notes:**
- [ ] Use the Composition Root pattern for project-level toolchain configuration.
- [ ] Create `pyproject.toml`, `uv.lock`, and `tests/unit/test_project_metadata.py`.
- [ ] Keep the manifest aligned with Python 3.12, `uv`, `pytest`, and `ruff` requirements.

---

### T-002: Create the source and test package skeleton

**User story ref:** Architecture: File & Folder Structure
**Start condition:** T-001 is complete.
**End condition:** `src/agent_on_claude_sdk/`, `tests/unit/`, `tests/integration/`, and `tests/e2e/` exist with the required `__init__.py` files.

**Test first:**
- [ ] Run `test -d src/agent_on_claude_sdk && test -d tests/unit && test -d tests/integration && test -d tests/e2e`; assert the command fails before the directories exist and passes after creation.
- [ ] Run `uv run python -c "import agent_on_claude_sdk"`; assert the package import succeeds from the editable environment.

**Implementation notes:**
- [ ] Use Package-by-Feature with clear module boundaries from the architecture.
- [ ] Create the directory tree and only the minimal `__init__.py` files in this task.
- [ ] Keep structure changes separate from business logic to satisfy Single Responsibility Principle.

---

### T-003: Add ignore rules and placeholder environment settings

**User story ref:** US-007
**Start condition:** T-001 is complete.
**End condition:** `.gitignore` excludes secrets, caches, and generated traces, and `.env.example` contains placeholders only.

**Test first:**
- [ ] Run `test -f .gitignore && rg -n "^\.env$|^\.pytest_cache/|^__pycache__/|^runs/" .gitignore`; assert all required ignore rules exist.
- [ ] Run `test -f .env.example && rg -n "ANTHROPIC_API_KEY=|TAVILY_API_KEY=" .env.example && ! rg -n "sk-ant-|tvly-" .env.example`; assert the file contains placeholders and no real credential patterns.

**Implementation notes:**
- [ ] Use Fail-Safe Defaults for ignore and secret-handling policy.
- [ ] Create `.gitignore` and `.env.example` only.
- [ ] Cover the shared-material hygiene and placeholder rules from US-007.

---

### T-004: Add the root README navigation and quickstart

**User story ref:** US-001, Architecture: File & Folder Structure
**Start condition:** T-002 is complete.
**End condition:** `README.md` links to the scratch comparison, conventions, writeup, Skill, and stories, and includes a minimal local quickstart.

**Test first:**
- [ ] Run `test -f README.md && rg -n "agent-from-scratch|CLAUDE.md|WRITEUP.md|skills/research-summary|user-stories.md" README.md`; assert all root navigation targets are present.
- [ ] Run `rg -n "uv sync|python -m agent_on_claude_sdk.main|Docker" README.md`; assert the README documents local and container run paths.

**Implementation notes:**
- [ ] Use Documentation-as-Interface for the public project entry point.
- [ ] Create `README.md`.
- [ ] Keep the README learner-focused and traceable to US-001.

---

### T-005: Add the root project conventions file

**User story ref:** US-003
**Start condition:** T-002 is complete.
**End condition:** `CLAUDE.md` exists at the project root and documents validation, formatting, helper-agent use, related-link discovery, safety, and commit behavior.

**Test first:**
- [ ] Run `test -f CLAUDE.md && rg -n "Validation Rules|Formatting|Helper-Agent Use|Related-Link Discovery|Safety and Sharing|Commit Behavior" CLAUDE.md`; assert all required sections exist.
- [ ] Run `rg -n "Never commit secrets|Do not overwrite unrelated local changes" CLAUDE.md`; assert explicit safety warnings are present.

**Implementation notes:**
- [ ] Use the Policy Document pattern for repo-level guardrails.
- [ ] Create `CLAUDE.md`.
- [ ] Mirror the root-level conventions called out in US-003.

---

### T-006: Add the research-summary Skill contract

**User story ref:** US-005, Architecture: File & Folder Structure
**Start condition:** T-002 is complete.
**End condition:** `skills/research-summary/SKILL.md` exists and defines Question, Key Findings, Related Links, Evidence Gaps, and Next Step sections.

**Test first:**
- [ ] Run `test -f skills/research-summary/SKILL.md && rg -n "^1\. Question|^2\. Key Findings|^3\. Related Links|^4\. Evidence Gaps|^5\. Next Step" skills/research-summary/SKILL.md`; assert the required output sections exist in order.
- [ ] Run `rg -n "Label uncertain|Do not fabricate" skills/research-summary/SKILL.md`; assert the Skill explicitly handles weak evidence.

**Implementation notes:**
- [ ] Use Template Method for a fixed, reusable output shape.
- [ ] Create `skills/research-summary/SKILL.md`.
- [ ] Keep the Skill concise and directly aligned to US-005.

---

### T-007: Write the 200-word harness comparison

**User story ref:** US-010, US-011
**Start condition:** T-004 is complete.
**End condition:** `WRITEUP.md` exists, is exactly 200 words, compares the harness with `agent-from-scratch`, and is understandable without source code.

**Test first:**
- [ ] Run `test -f WRITEUP.md && [ "$(wc -w < WRITEUP.md)" -eq 200 ]`; assert the word count is exact.
- [ ] Run `rg -n "agent-from-scratch|harness" WRITEUP.md`; assert the comparison is explicit.

**Implementation notes:**
- [ ] Use Plain-Language Documentation rather than implementation detail dumping.
- [ ] Create `WRITEUP.md` only.
- [ ] Keep the reflection concrete, concise, and readable for non-implementers.

---

### T-008: Add the publishable harness explainer draft

**User story ref:** US-012
**Start condition:** T-004 is complete.
**End condition:** A root blog draft explains what a harness is in plain language, contrasts scratch versus SDK, and is ready to publish before 2026-05-25.

**Test first:**
- [ ] Run `test -f WHAT_IS_A_HARNESS.md && rg -n "What a harness is|agent-from-scratch|Claude Agent SDK|2026-05-25" WHAT_IS_A_HARNESS.md`; assert the topic, comparison, and deadline marker are present.
- [ ] Run `rg -n "plain language|publish" WHAT_IS_A_HARNESS.md`; assert the draft explicitly targets public publication.

**Implementation notes:**
- [ ] Use Audience-First Writing to keep the explainer accessible.
- [ ] Create `WHAT_IS_A_HARNESS.md`.
- [ ] Keep this artifact distinct from the short comparison in `WRITEUP.md`.

---

## Phase 2: Shared Contracts And Runtime Foundations

### T-009: Add shared runtime models

**User story ref:** Architecture: File & Folder Structure, State Management
**Start condition:** T-002 is complete.
**End condition:** `models.py` defines typed contracts for tool results, trace events, artifacts, references, and run records.

**Test first:**
- [ ] Create `tests/unit/test_models.py::test_tool_result_and_run_record_contracts`; run `uv run pytest tests/unit/test_models.py -q`; assert it fails before `models.py` exists and passes after the contracts are implemented.
- [ ] Assert the test checks `is_error`, artifact path, and trace event fields explicitly.

**Implementation notes:**
- [ ] Use Value Object pattern and Single Responsibility Principle for shared contracts.
- [ ] Create `src/agent_on_claude_sdk/models.py` and `tests/unit/test_models.py`.
- [ ] Keep models serialization-friendly for traces and optional DB indexing.

---

### T-010: Add config loading and fail-fast validation

**User story ref:** US-002, Architecture: Stack Summary, State Management, Service Connections
**Start condition:** T-009 is complete.
**End condition:** `config.py` loads env values, applies defaults, and raises clear errors naming missing settings without exposing secret values.

**Test first:**
- [ ] Create `tests/unit/test_config.py::test_missing_required_keys_are_named` and `tests/unit/test_config.py::test_defaults_are_applied`; run `uv run pytest tests/unit/test_config.py -q`; assert the tests fail before implementation and pass after.
- [ ] Assert one test verifies that secret values are not echoed in error messages.

**Implementation notes:**
- [ ] Use the Options Object pattern for immutable run configuration.
- [ ] Create `src/agent_on_claude_sdk/config.py` and `tests/unit/test_config.py`.
- [ ] Follow the fail-fast startup behavior defined in the architecture.

---

### T-011: Add structured tracing

**User story ref:** Architecture: File & Folder Structure, State Management, Long-Term Considerations
**Start condition:** T-009 is complete.
**End condition:** `tracing.py` emits append-only JSONL-compatible events with step id, action type, timestamps, and truncated payloads.

**Test first:**
- [ ] Create `tests/unit/test_tracing.py::test_trace_event_is_serialized_to_jsonl`; run `uv run pytest tests/unit/test_tracing.py -q`; assert one event produces one line with the required keys.
- [ ] Add `tests/unit/test_tracing.py::test_tracing_truncates_large_payloads`; assert long values are truncated predictably.

**Implementation notes:**
- [ ] Use the Audit Log pattern for reproducible run traces.
- [ ] Create `src/agent_on_claude_sdk/tracing.py` and `tests/unit/test_tracing.py`.
- [ ] Keep tracing append-only and safe for behavior validation.

---

### T-012: Add the filesystem run store

**User story ref:** Architecture: File & Folder Structure, State Management, Database Schema
**Start condition:** T-009 and T-011 are complete.
**End condition:** `fs_store.py` can create a run directory, append trace events, persist artifacts, and write reference files under `runs/<run-id>/`.

**Test first:**
- [ ] Create `tests/unit/test_fs_store.py::test_start_run_creates_expected_layout`; run `uv run pytest tests/unit/test_fs_store.py -q`; assert `trace.jsonl`, `artifacts/`, and `references.jsonl` locations are created.
- [ ] Add `tests/unit/test_fs_store.py::test_save_artifact_returns_relative_path`; assert saved artifact metadata matches the filesystem path.

**Implementation notes:**
- [ ] Use Repository pattern over the filesystem.
- [ ] Create `src/agent_on_claude_sdk/persistence/fs_store.py` and `tests/unit/test_fs_store.py`.
- [ ] Treat the filesystem as the MVP source of truth.

---

### T-013: Add the PostgreSQL metadata adapter stub

**User story ref:** Architecture: File & Folder Structure, Database Schema
**Start condition:** T-009 is complete.
**End condition:** `pg_store.py` exists behind a feature flag and returns a clear disabled/not-configured response when metadata mode is off.

**Test first:**
- [ ] Create `tests/unit/test_pg_store.py::test_pg_store_is_disabled_without_database_url`; run `uv run pytest tests/unit/test_pg_store.py -q`; assert the adapter fails closed with a clear message.
- [ ] Add `tests/unit/test_pg_store.py::test_pg_store_accepts_configured_engine_factory`; assert engine construction is isolated from the filesystem store.

**Implementation notes:**
- [ ] Use Adapter plus Null Object patterns for optional infrastructure.
- [ ] Create `src/agent_on_claude_sdk/persistence/pg_store.py` and `tests/unit/test_pg_store.py`.
- [ ] Do not make PostgreSQL a runtime requirement for the MVP.

---

## Phase 3: Tool Layer And Formatting

### T-014: Add the tool schema registry and dispatcher

**User story ref:** Architecture: File & Folder Structure, State Management, Service Connections
**Start condition:** T-009 is complete.
**End condition:** `tools/registry.py` exports the tool schema list and a dispatcher that routes by tool name and always returns a structured tool result.

**Test first:**
- [ ] Create `tests/unit/test_tool_registry.py::test_dispatch_unknown_tool_returns_error_result`; run `uv run pytest tests/unit/test_tool_registry.py -q`; assert unknown tool names do not raise.
- [ ] Add `tests/unit/test_tool_registry.py::test_tools_schema_names_are_stable`; assert `web_search`, `read_file`, and `write_file` are present.

**Implementation notes:**
- [ ] Use a Command/Strategy registry for tool dispatch.
- [ ] Create `src/agent_on_claude_sdk/tools/registry.py`, `src/agent_on_claude_sdk/tools/__init__.py`, and `tests/unit/test_tool_registry.py`.
- [ ] Keep dispatch free of tool-specific business logic beyond routing.

---

### T-015: Add the read_file tool

**User story ref:** US-002, Architecture: Service Connections
**Start condition:** T-014 is complete.
**End condition:** `read_file.py` returns UTF-8 text, reports file-not-found clearly, and rejects binary content.

**Test first:**
- [ ] Create `tests/unit/test_read_file.py::test_read_file_returns_text`, `tests/unit/test_read_file.py::test_read_file_reports_missing_path`, and `tests/unit/test_read_file.py::test_read_file_rejects_binary`; run `uv run pytest tests/unit/test_read_file.py -q`.
- [ ] Assert the missing-file message includes the requested path.

**Implementation notes:**
- [ ] Use Guard Clauses for predictable file error handling.
- [ ] Create `src/agent_on_claude_sdk/tools/read_file.py` and `tests/unit/test_read_file.py`.
- [ ] Preserve the scratch-agent behavior where it still matches the new architecture.

---

### T-016: Add the write_file tool

**User story ref:** US-002, Architecture: State Management, Service Connections, Long-Term Considerations
**Start condition:** T-012 and T-014 are complete.
**End condition:** `write_file.py` writes artifacts under the run store, blocks unsafe paths, and returns structured success and error results.

**Test first:**
- [ ] Create `tests/unit/test_write_file.py::test_write_file_persists_artifact`, `tests/unit/test_write_file.py::test_write_file_rejects_parent_escape`, and `tests/unit/test_write_file.py::test_write_file_reports_missing_parent`; run `uv run pytest tests/unit/test_write_file.py -q`.
- [ ] Assert the success result contains a path under `runs/<run-id>/artifacts/`.

**Implementation notes:**
- [ ] Use the Policy pattern plus Guard Clauses for path safety.
- [ ] Create `src/agent_on_claude_sdk/tools/write_file.py` and `tests/unit/test_write_file.py`.
- [ ] Keep write concerns separate from formatting side effects.

---

### T-017: Add the post-write formatter runner

**User story ref:** US-004, Architecture: File & Folder Structure, Service Connections
**Start condition:** T-016 is complete.
**End condition:** `validation.py` formats written `.py` files with `ruff format`, skips non-Python files, and surfaces missing-ruff failures to the operator.

**Test first:**
- [ ] Create `tests/unit/test_validation.py::test_python_file_invokes_ruff_format`, `tests/unit/test_validation.py::test_non_python_file_is_skipped`, and `tests/unit/test_validation.py::test_missing_ruff_is_reported`; run `uv run pytest tests/unit/test_validation.py -q`.
- [ ] Assert the missing-ruff branch returns a visible warning string rather than raising.

**Implementation notes:**
- [ ] Use Strategy-by-Extension to isolate formatting behavior.
- [ ] Create `src/agent_on_claude_sdk/validation.py` and `tests/unit/test_validation.py`.
- [ ] Keep validation independent from the file writer and hook configuration.

---

### T-018: Add the PostToolUse hook wiring

**User story ref:** US-004, Architecture: File & Folder Structure, Service Connections
**Start condition:** T-017 is complete.
**End condition:** `.claude/settings.json` contains a PostToolUse hook that invokes `ruff format` on written Python files.

**Test first:**
- [ ] Run `test -f .claude/settings.json && rg -n "PostToolUse|ruff format|Write\|Edit\|MultiEdit" .claude/settings.json`; assert the hook declaration exists.
- [ ] Run `rg -n "tool_input.path|tool_input.filePath" .claude/settings.json`; assert the hook resolves the written file path from tool input.

**Implementation notes:**
- [ ] Use Declarative Configuration for agent hook wiring.
- [ ] Create `.claude/settings.json`.
- [ ] Keep the hook thin and let `validation.py` own the operational behavior.

---

### T-019: Add the web_search tool

**User story ref:** US-002, Architecture: Stack Summary, Service Connections
**Start condition:** T-010 and T-014 are complete.
**End condition:** `web_search.py` calls Tavily, returns normalized search results, and converts API failures into tool errors.

**Test first:**
- [ ] Create `tests/unit/test_web_search.py::test_web_search_returns_results` and `tests/unit/test_web_search.py::test_web_search_reports_tavily_error`; run `uv run pytest tests/unit/test_web_search.py -q`.
- [ ] Assert the failure branch preserves the reason and yields an error result through the dispatcher.

**Implementation notes:**
- [ ] Use an Adapter around the Tavily client.
- [ ] Create `src/agent_on_claude_sdk/tools/web_search.py` and `tests/unit/test_web_search.py`.
- [ ] Do not let Tavily exceptions escape the tool layer.

---

## Phase 4: Harness Orchestration And CLI

### T-020: Add the harness stop-reason test scaffold

**User story ref:** US-002, Architecture: Service Connections, Testing Strategy
**Start condition:** T-014, T-015, T-016, and T-019 are complete.
**End condition:** A unit test file exists that mocks Claude SDK responses for `end_turn`, `tool_use`, and max-turn scenarios.

**Test first:**
- [ ] Create `tests/unit/test_harness_stop_reasons.py` with one failing case per branch; run `uv run pytest tests/unit/test_harness_stop_reasons.py -q`; assert it fails because `harness.py` is absent or incomplete.
- [ ] Ensure the scaffold asserts message ordering and loop termination conditions.

**Implementation notes:**
- [ ] Use Test Double pattern for Claude SDK responses.
- [ ] Create `tests/unit/test_harness_stop_reasons.py` only.
- [ ] Keep the scaffold limited to branch behavior rather than full filesystem integration.

---

### T-021: Implement the base harness loop

**User story ref:** US-002, US-008, Architecture: State Management, Service Connections
**Start condition:** T-020 is complete.
**End condition:** `harness.py` can start a run, call the Claude Agent SDK, stop on `end_turn`, and halt cleanly at the configured turn ceiling.

**Test first:**
- [ ] Run `uv run pytest tests/unit/test_harness_stop_reasons.py -q`; assert `test_end_turn_returns_final_answer` and `test_max_turns_halts_cleanly` pass.
- [ ] Assert the max-turn branch returns a blocked status instead of looping indefinitely.

**Implementation notes:**
- [ ] Use Template Method for the run loop.
- [ ] Create `src/agent_on_claude_sdk/harness.py`.
- [ ] Keep stop branches explicit and easy to trace during behavior validation.

---

### T-022: Implement tool_use aggregation in the harness

**User story ref:** US-002, Architecture: State Management, Service Connections
**Start condition:** T-021 and T-014 are complete.
**End condition:** The harness dispatches all tool calls in a turn and appends one combined tool-result message before the next model call.

**Test first:**
- [ ] Extend `tests/unit/test_harness_stop_reasons.py` with `test_multiple_tool_calls_are_returned_in_one_user_message`; run `uv run pytest tests/unit/test_harness_stop_reasons.py -q`.
- [ ] Assert the dispatcher is called once per tool request and the next message contains the full result array.

**Implementation notes:**
- [ ] Use Batch Command pattern for grouped tool results.
- [ ] Modify `src/agent_on_claude_sdk/harness.py`.
- [ ] Preserve the single-follow-up-message contract from the scratch reference behavior.

---

### T-023: Persist run state and trace from the harness

**User story ref:** US-008, Architecture: File & Folder Structure, State Management
**Start condition:** T-021, T-022, and T-012 are complete.
**End condition:** Each harness run creates a run id, writes trace events, and stores artifacts and references through `fs_store.py`.

**Test first:**
- [ ] Create `tests/integration/test_harness_persistence.py::test_run_writes_trace_and_artifact_metadata`; run `uv run pytest tests/integration/test_harness_persistence.py -q`.
- [ ] Assert the integration test checks for `trace.jsonl`, `artifacts/`, and a persisted run id.

**Implementation notes:**
- [ ] Use Orchestrator plus Repository patterns.
- [ ] Modify `src/agent_on_claude_sdk/harness.py` and `src/agent_on_claude_sdk/persistence/fs_store.py`.
- [ ] Keep persistence writes outside the tool dispatcher for better isolation.

---

### T-024: Add the CLI entrypoint

**User story ref:** US-002, Architecture: File & Folder Structure, Service Connections, Docker & Deployment
**Start condition:** T-021 and T-010 are complete.
**End condition:** `main.py` loads config, accepts an optional task override, and exits with clear status codes on success or blocked startup.

**Test first:**
- [ ] Create `tests/unit/test_main.py::test_default_task_is_used_without_cli_arg` and `tests/unit/test_main.py::test_missing_keys_exit_nonzero`; run `uv run pytest tests/unit/test_main.py -q`.
- [ ] Assert one test checks that a custom CLI task string is passed through unchanged.

**Implementation notes:**
- [ ] Use Composition Root to keep construction at the edge.
- [ ] Create `src/agent_on_claude_sdk/main.py` and `tests/unit/test_main.py`.
- [ ] Keep CLI parsing minimal and explicit.

---

### T-025: Add visible progress and completion output

**User story ref:** US-002, US-008, Architecture: Testing Strategy
**Start condition:** T-021 through T-024 are complete.
**End condition:** Stdout shows step progress, tool activity, blocked causes, and a final completion marker that a human can verify quickly.

**Test first:**
- [ ] Create `tests/unit/test_console_output.py::test_run_prints_step_headers_and_done_marker`; run `uv run pytest tests/unit/test_console_output.py -q`.
- [ ] Assert the test also checks that blocked runs print the missing setting, file, or command name.

**Implementation notes:**
- [ ] Use Presenter pattern to separate console formatting from the core loop.
- [ ] Modify `src/agent_on_claude_sdk/harness.py`, `src/agent_on_claude_sdk/tracing.py`, and `tests/unit/test_console_output.py`.
- [ ] Match the visibility requirements in US-002 and US-008.

---

## Phase 5: Helper Workflows And Reference Outputs

### T-026: Add the research summary helper formatter

**User story ref:** US-005, Architecture: File & Folder Structure
**Start condition:** T-009 and T-006 are complete.
**End condition:** `helpers/research_summary.py` can render the canonical summary sections from structured inputs.

**Test first:**
- [ ] Create `tests/unit/test_research_summary.py::test_summary_sections_render_in_required_order`; run `uv run pytest tests/unit/test_research_summary.py -q`.
- [ ] Add `tests/unit/test_research_summary.py::test_missing_evidence_is_rendered_as_gap`; assert weak evidence is labeled plainly.

**Implementation notes:**
- [ ] Use Builder pattern for deterministic markdown assembly.
- [ ] Create `src/agent_on_claude_sdk/helpers/research_summary.py` and `tests/unit/test_research_summary.py`.
- [ ] Keep the helper aligned with the research-summary Skill contract.

---

### T-027: Add the related-links helper

**User story ref:** US-006, US-009, Architecture: Service Connections
**Start condition:** T-024 is complete.
**End condition:** `helpers/related_links.py` invokes one read-only Task sub-agent with objective `find related links` and normalizes the result into local-path and external-link buckets.

**Test first:**
- [ ] Create `tests/unit/test_related_links.py::test_helper_uses_find_related_links_objective`; run `uv run pytest tests/unit/test_related_links.py -q`.
- [ ] Add `tests/unit/test_related_links.py::test_helper_is_read_only`; assert the helper call contract requests no file mutation.

**Implementation notes:**
- [ ] Use Adapter pattern over the Task/sub-agent interface.
- [ ] Create `src/agent_on_claude_sdk/helpers/related_links.py` and `tests/unit/test_related_links.py`.
- [ ] Keep the objective string exact: `find related links`.

---

### T-028: Add the root related-links artifact

**User story ref:** US-009
**Start condition:** T-027 is complete.
**End condition:** `RELATED_LINKS.md` exists at the project root and groups references into Local Paths and External Links, including the scratch comparison and current project materials.

**Test first:**
- [ ] Run `test -f RELATED_LINKS.md && rg -n "^## Local Paths|^## External Links|agent-from-scratch|CLAUDE.md|WRITEUP.md|research-summary" RELATED_LINKS.md`; assert the required sections and references exist.
- [ ] Run `rg -n "No external link available yet" RELATED_LINKS.md`; assert the empty-external case is documented if there are no external links.

**Implementation notes:**
- [ ] Use Report Generator pattern for a stable, reviewable artifact.
- [ ] Create `RELATED_LINKS.md`.
- [ ] Keep the artifact human-readable and easy to diff.

---

### T-029: Add the Phase 1b verification note

**User story ref:** US-011
**Start condition:** T-007, T-018, T-025, and T-028 are complete.
**End condition:** A single root verification note exists and marks the Phase 1b deliverable as complete or blocked with evidence links.

**Test first:**
- [ ] Run `test -f PHASE_1B_VERIFICATION.md && rg -n "Phase 1b|Complete|Blocked|CLAUDE.md|WRITEUP.md|research-summary|related links" PHASE_1B_VERIFICATION.md`; assert status and evidence fields exist.
- [ ] Assert the note has exactly one place where a human can see the current MVP completion state.

**Implementation notes:**
- [ ] Use Checklist / Status Report pattern.
- [ ] Create `PHASE_1B_VERIFICATION.md`.
- [ ] Keep status evidence-based rather than aspirational.

---

## Phase 6: Containerization And Project Automation

### T-030: Add the Dockerfile

**User story ref:** Architecture: Docker & Deployment, Long-Term Considerations
**Start condition:** T-024 is complete.
**End condition:** `Dockerfile` builds a non-root Python 3.12 image that installs dependencies via `uv` and runs the CLI entrypoint.

**Test first:**
- [ ] Run `docker build -t agent-on-claude-sdk:test .`; assert the image builds successfully.
- [ ] Run `docker run --rm agent-on-claude-sdk:test python --version`; assert the container reports Python 3.12.

**Implementation notes:**
- [ ] Use the Multi-Stage Build pattern for a lean image.
- [ ] Create `Dockerfile`.
- [ ] Keep image layers free of embedded secrets or local caches.

---

### T-031: Add docker-compose orchestration

**User story ref:** Architecture: Docker & Deployment, Database Schema
**Start condition:** T-030 and T-013 are complete.
**End condition:** `docker-compose.yml` defines the `agent` service and an optional `postgres` metadata profile with the documented volumes and network.

**Test first:**
- [ ] Run `docker compose config`; assert the compose file is valid.
- [ ] Run `docker compose --profile metadata config`; assert the optional `postgres` profile renders successfully.

**Implementation notes:**
- [ ] Use Composition Root for service wiring.
- [ ] Create `docker-compose.yml`.
- [ ] Keep PostgreSQL optional and disabled by default for the MVP.

---

### T-032: Add the standard run script

**User story ref:** Architecture: File & Folder Structure, Docker & Deployment
**Start condition:** T-024 and T-031 are complete.
**End condition:** `scripts/run.sh` executes the standard local entrypoint and forwards an optional task string safely.

**Test first:**
- [ ] Run `bash scripts/run.sh --help` or `bash scripts/run.sh "test task"` in a stubbed environment; assert the script invokes `uv run python -m agent_on_claude_sdk.main`.
- [ ] Assert the script exits non-zero when required env vars are missing.

**Implementation notes:**
- [ ] Use Wrapper Script pattern.
- [ ] Create `scripts/run.sh`.
- [ ] Keep quoting strict so task strings with spaces stay intact.

---

### T-033: Add the behavior verification script

**User story ref:** US-008, Architecture: Docker & Deployment, Testing Strategy
**Start condition:** T-025 and T-032 are complete.
**End condition:** `scripts/verify_behavior.sh` runs the real code path and asserts search, read, write, and stop behavior through observable outputs and generated artifacts.

**Test first:**
- [ ] Run `bash scripts/verify_behavior.sh` in a fixture or mocked environment; assert it checks for the completion marker and artifact existence.
- [ ] Assert the script exits non-zero with a named blocker when credentials or commands are missing.

**Implementation notes:**
- [ ] Use Smoke Test pattern for real-path validation.
- [ ] Create `scripts/verify_behavior.sh`.
- [ ] This script is the primary behavior-validation gate required by project conventions.

---

### T-034: Add the secret and clutter guard script

**User story ref:** US-007, Architecture: Long-Term Considerations
**Start condition:** T-003 is complete.
**End condition:** `scripts/check_secrets.sh` fails on committed secret patterns and verifies ignored clutter paths are excluded from shared state.

**Test first:**
- [ ] Run `bash scripts/check_secrets.sh`; assert it passes on placeholder-only files and fails on a temp fixture containing `sk-ant-` or `tvly-`.
- [ ] Run `git check-ignore .env .pytest_cache/example runs/example/trace.jsonl`; assert all listed paths are ignored.

**Implementation notes:**
- [ ] Use Guard Rail pattern.
- [ ] Create `scripts/check_secrets.sh`.
- [ ] Keep checks deterministic and fast enough for pre-commit use.

---

### T-035: Add the CI workflow

**User story ref:** Architecture: Testing Strategy
**Start condition:** T-001 through T-034 are complete.
**End condition:** `.github/workflows/ci.yml` runs `uv sync`, Ruff, and pytest for unit and integration scopes on push and pull request.

**Test first:**
- [ ] Run `test -f .github/workflows/ci.yml && rg -n "uv sync|ruff check \.|ruff format --check \.|pytest tests/unit tests/integration" .github/workflows/ci.yml`; assert all required steps exist.
- [ ] Run `uv run python -c "import yaml, pathlib; yaml.safe_load(pathlib.Path('.github/workflows/ci.yml').read_text())"`; assert the workflow file parses.

**Implementation notes:**
- [ ] Use CI Pipeline pattern.
- [ ] Create `.github/workflows/ci.yml`.
- [ ] Keep end-to-end execution out of the default workflow unless secrets are available.

---

## Phase 7: QA And Final Verification

### T-036: Add the integration harness loop test

**User story ref:** US-002, US-008, Architecture: Testing Strategy
**Start condition:** T-025 is complete.
**End condition:** `tests/integration/test_harness_loop.py` covers a full multi-turn run with mocked Claude SDK and the real local tool dispatcher wiring.

**Test first:**
- [ ] Create `tests/integration/test_harness_loop.py::test_default_task_searches_reads_writes_and_stops`; run `uv run pytest tests/integration/test_harness_loop.py -q`; assert it fails before the full loop is wired and passes after.
- [ ] Assert the test verifies progress output, artifact creation, and single-message aggregation of tool results.

**Implementation notes:**
- [ ] Use Sociable Integration Test pattern.
- [ ] Create `tests/integration/test_harness_loop.py`.
- [ ] Keep the Claude SDK mocked and the local tool wiring real.

---

### T-037: Add the end-to-end real-run test

**User story ref:** US-008, Architecture: Testing Strategy
**Start condition:** T-036 is complete.
**End condition:** `tests/e2e/test_real_run.py` runs the actual CLI path behind env-gated secrets and asserts a real artifact is produced.

**Test first:**
- [ ] Create `tests/e2e/test_real_run.py::test_real_run_produces_artifact`; run `uv run pytest tests/e2e/test_real_run.py -q`; assert it is skipped cleanly without secrets and runnable with secrets.
- [ ] Assert the test checks for a completion marker and a non-empty artifact file.

**Implementation notes:**
- [ ] Use End-to-End Test pattern.
- [ ] Create `tests/e2e/test_real_run.py`.
- [ ] Never hardcode secrets; rely on runtime env injection only.

---

### T-038: Execute behavior validation and record evidence

**User story ref:** US-008, US-011
**Start condition:** T-033, T-036, and T-037 are complete.
**End condition:** A real run has been executed through the standard path and its evidence is recorded in `PHASE_1B_VERIFICATION.md`.

**Test first:**
- [ ] Run `bash scripts/verify_behavior.sh`; assert it exits 0 and prints the run id, completion marker, and artifact path.
- [ ] Run `rg -n "Behavior validation: PASS|Run ID|Artifact" PHASE_1B_VERIFICATION.md`; assert the evidence block is updated.

**Implementation notes:**
- [ ] Use Evidence-Based Verification rather than file-presence checking.
- [ ] Modify `PHASE_1B_VERIFICATION.md` only.
- [ ] This task is not done until the real runtime path has been exercised.

---

### T-039: Execute final repo hygiene validation and close MVP status

**User story ref:** US-007, US-011
**Start condition:** T-028, T-034, T-035, and T-038 are complete.
**End condition:** The verification note reflects final complete or blocked status and the repo passes placeholder, ignore, and CI-config sanity checks.

**Test first:**
- [ ] Run `bash scripts/check_secrets.sh && git check-ignore .env .pytest_cache/example runs/example/trace.jsonl`; assert secret and clutter guards pass.
- [ ] Run `rg -n "Phase 1b status: COMPLETE|Phase 1b status: BLOCKED" PHASE_1B_VERIFICATION.md`; assert one final status is set.

**Implementation notes:**
- [ ] Use Release Checklist pattern for the final close-out gate.
- [ ] Modify `PHASE_1B_VERIFICATION.md` only.
- [ ] Do not mark COMPLETE unless docs, hooks, helper workflow, tests, and behavior evidence all exist.