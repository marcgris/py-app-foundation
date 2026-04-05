# Py App Foundation Roadmap

## Purpose

This repository defines Py App Foundation, a reusable foundation for building professional, well-designed, secure, and agent-friendly Python applications. It gives teams strong defaults for code quality, security, testing, documentation, and autonomous development workflows without forcing unnecessary framework or deployment choices.

## Vision

1. Teams can bootstrap a production-grade Python project quickly.
2. The base project enforces strong engineering defaults without excessive friction.
3. Agent workflows are explicit, predictable, and bounded by validation and review.
4. The starter is composable: one core foundation plus targeted overlays.
5. Downstream projects inherit a consistent quality and security posture.

## Design Principles

1. Keep the core framework-light.
2. Prefer explicit conventions over implicit magic.
3. Make validation cheap and automatic.
4. Treat security as a default, not an optional add-on.
5. Design for human readability first and agent usability second.
6. Separate enduring architecture from session-by-session progress.

## In Scope

1. Python project structure and packaging defaults.
2. Dependency and environment management.
3. Linting, formatting, typing, and test standards.
4. Security scanning and supply-chain checks.
5. CI workflows and local validation workflow.
6. Agent instruction files and guardrails.
7. First-wave overlays for CLI, UI, API, and worker projects.
8. Planning artifacts and handoff process.

## Out of Scope

1. Cloud-specific deployment in v1.
2. Infrastructure provisioning.
3. Standardizing on a database or ORM.
4. Domain-specific business logic.
5. Organization process not required to operate the starter.

## Phase Plan

1. **Phase 1**: Planning artifacts, scope boundaries, and architecture decisions. ✅ Complete
2. **Phase 2**: Core template skeleton and repository structure. ✅ Complete
3. **Phase 3**: Agent workflow, validation stack, and CI guardrails.
4. **Phase 4**: CLI, UI, API, and worker overlays.
5. **Phase 5**: Validation, sample generation, and release readiness.

## Current Focus

- **Active Phase**: Phase 5 (Release readiness)
- **Objective**: Finalize v1 release documentation, maintenance standards, and release governance.
- **Current Owner**: Release preparation

## Copilot Capability Adoption Plan

This plan introduces Copilot tools, agents, and skills in controlled phases. The intent is to adopt capabilities incrementally, validate impact, and then fold successful patterns into standard project documentation.

### Source Reference

Adoption guidance in this section is informed by the local reference project `python-copilot-skill-library`, specifically its Copilot operating assets:

1. Project overview and workflow docs (`README.md`, `GETTING-STARTED.md`, `python-vscode-copilot-guide.md`)
2. Project instruction baseline (`.github/copilot-instructions.md`)
3. Skill catalog under `.github/skills/`
4. Agent personas under `.github/agents/`
5. Workspace enablement configuration under `.vscode/` (settings, extensions, MCP)

### Phase A — Foundation (now)

1. Define baseline Copilot usage rules in contributor and guide docs.
2. Adopt quality-focused workflows first: planning prompts, code review prompts, testing prompts, and security review prompts.
3. Add an AI-assisted pre-release quality gate that runs before tagging.

### Phase B — Overlay-Aware Enablement

1. Add overlay-specific guidance for CLI and UI work first.
2. Define required prompt contracts for overlay changes (scope, constraints, tests, risks).
3. Add acceptance checks for overlay-level documentation and test coverage.

### Phase C — Advanced Workflows

1. Add API and worker-focused skill workflows when those overlays are implemented.
2. Introduce migration, observability, and deeper architecture-review workflows where applicable.
3. Expand MCP-backed workflows only where they provide measurable quality gains.

### Exit and Retirement Rule for This Plan

Retire this roadmap subsection when all of the following are true:

1. Copilot workflows are represented in standard contributor and release documentation.
2. Overlay-specific guidance exists in the relevant overlay docs.
3. Pre-release quality gates include the adopted AI-assisted checks.
4. The team is using the embedded workflows consistently without referencing this temporary plan.

### Checkpoint Contract (Definition of Done)

Every skill-library checkpoint in this roadmap must produce the same minimum artifacts so decisions are auditable and repeatable.

1. Trigger: a defined project event occurs (for example, skeleton merged or promotion review started).
2. Scope: only the target overlay/profile and the next delivery milestone are evaluated.
3. Assessment Output: classify each candidate skill as `Adopt now`, `Defer`, or `Skip` with a one-line rationale.
4. Documentation Update: record outcomes in this roadmap and, when release-impacting, in `docs/guide/release-checklist.md`.
5. Action Binding: any `Adopt now` skill must be reflected in practical guidance (for example cookbook prompts in `docs/guide/contributing.md`) before checkpoint close.

Checkpoint completion criteria:

1. Outcome summary exists under the checkpoint section.
2. At least one concrete workflow/prompt update exists for each adopted skill.
3. Deferred skills include a named re-evaluation checkpoint.
4. Any beta-promotion blockers discovered at the checkpoint are captured in release checklist status tables.

### Recommendation Register (Governance)

Use this register to track skill-library and agentic workflow recommendations so deferred items are revisited at the right milestone.

| ID | Recommendation | Status | Trigger To Act | Target Checkpoint | Evidence To Close |
|---|---|---|---|---|---|
| REC-001 | Align installed capabilities with adopted-now cookbook prompts (skills/agents). | ✅ Adopted | Immediate | Completed | Skills and agents present under `.github/skills/` and `.github/agents/` |
| REC-002 | Keep dependency guidance aligned with `pyproject.toml` conventions (`[dependency-groups]`). | ✅ Adopted | Immediate | Completed | Local dependency-management skill examples updated |
| REC-003 | Adopt migration-first workflows (`db-migrations` skill and `db-architect` agent). | ⏳ Deferred | First persistence-backed API resource or first Alembic migration introduced | API Checkpoint 2 (or first persistence milestone) | Skill/agent added and referenced in contributor cookbook + release checklist |
| REC-004 | Expand observability from logging baseline to metrics/tracing rollout. | ⏳ Deferred | API or worker promotion from Experimental to Beta | API Checkpoint 2 / Worker Checkpoint 2 | Explicit metrics/tracing contract and validation checks documented |
| REC-005 | Enforce recommendation review gate in release and promotion workflows. | ✅ Adopted | Every release-prep or promotion PR | Continuous | Release checklist and PR traceability sections reference recommendation IDs |

### UI Skill-Library Checkpoints

Use these checkpoints to evaluate opportunities to adopt content from `python-copilot-skill-library` for UI overlays.

1. ✅ Checkpoint 1 (current): Run a gap assessment immediately after UI Shared Base + Web profile merge.
2. ✅ Checkpoint 2: Re-run assessment before starting UI Desktop profile implementation.
3. ✅ Checkpoint 3 (hardening): Re-run assessment before promoting UI Shared Base or Web profile from Experimental to Beta.

Checkpoint 1 outcome summary:

1. Adopt now: `python-testing`, `security-audit`, and `github-actions` guidance for UI profile smoke checks, release gating, and CI hardening.
2. Defer to Checkpoint 3: `observability`, `dependency-management`, and `python-refactor` guidance after Desktop profile runtime/tooling decisions are concrete.
3. Skip for current UI scope: `python-api-endpoint`, `pydantic-models`, and `db-migrations` because current UI work is static/profile-shell focused.

Checkpoint 2 outcome summary:

1. Continue adopted set: `python-testing`, `security-audit`, and `github-actions` for Desktop profile smoke checks and CI gating.
2. Keep deferred set for later hardening: `observability`, `dependency-management`, and `python-refactor`.

Checkpoint 3 outcome summary:

1. Keep adopted set unchanged for current UI profile scope: `python-testing`, `security-audit`, and `github-actions`.
2. Keep `observability` deferred until UI runtime instrumentation requirements are introduced (for example, telemetry/correlation for a production UI runtime layer).
3. Keep `dependency-management` and `python-refactor` deferred to API/worker overlay implementation phases where toolchain and architectural complexity increase.
4. UI profiles remain `Experimental` until Beta freeze notes and one full release-cycle stability evidence are documented.

### API Skill-Library Checkpoints

Use these checkpoints to evaluate opportunities to adopt content from `python-copilot-skill-library` for API overlays.

1. ✅ Checkpoint 1: Run a gap assessment immediately after API skeleton merge.
2. ⏳ Checkpoint 2: Re-run assessment before promoting API overlay from Experimental to Beta.

Checkpoint 1 outcome summary:

1. Adopt now: `python-testing`, `security-audit`, and `github-actions` guidance for API smoke checks and CI gating.
2. Adopt now for API-specific implementation phases: `python-api-endpoint` and `pydantic-models`.
3. Defer: `observability`, `dependency-management`, and `python-refactor` until API runtime complexity and integration depth increase.

### Worker Skill-Library Checkpoints

Use these checkpoints to evaluate opportunities to adopt content from `python-copilot-skill-library` for worker overlays.

1. ✅ Checkpoint 1: Run a gap assessment immediately after worker skeleton merge.
2. ⏳ Checkpoint 2: Re-run assessment before promoting worker overlay from Experimental to Beta.

Checkpoint 1 outcome summary:

1. Adopt now: `python-testing`, `security-audit`, and `github-actions` guidance for worker smoke checks and CI gating.
2. Adopt now for worker implementation phases: `python-refactor` for execution flow extraction and boundary hardening when worker complexity expands.
3. Defer: `observability` and `dependency-management` until worker runtime topology (scheduler/queue/log transport) is finalized.

## Upcoming Work

1. ✅ Complete core package modules (config.py, logging.py, exceptions.py).
2. ✅ Create test infrastructure with working fixtures and smoke tests.
3. ✅ Configure and validate the local CI workflow (uv sync, pytest, ruff, pyright, bandit).
4. ✅ Create the CLI overlay skeleton.
5. ✅ Create the UI Shared Base + Web profile skeleton aligned to `docs/guide/ui-overlay-contract.md`.
6. ✅ Create the UI Desktop profile skeleton aligned to `docs/guide/ui-overlay-contract.md`.
7. ✅ Create the UI Mobile profile skeleton aligned to `docs/guide/ui-overlay-contract.md`.
8. ✅ Create the API overlay skeleton.
9. ✅ Create the worker overlay skeleton.
10. ✅ Verify all planned overlays and UI profiles pass validation.
11. ✅ Document the bootstrap and generation process.
12. ✅ Prepare v1 release and maintenance guidelines.

## CLI Overlay Milestones (Phase 4 Kickoff)

1. ✅ Add `starter` command entrypoint and parser scaffold.
2. ✅ Implement `starter health` command and smoke coverage.
3. ✅ Implement `starter config show` command with JSON output.
4. ✅ Add deterministic config-error handling (stderr + non-zero exit).
5. ✅ Add `starter --version` support from package metadata.

## Future Overlay Backlog

1. Scheduled jobs/cron profile.
2. Data/ETL pipeline profile.
3. MCP server profile.
4. Library/package-only profile.

## Deferred Compatibility Work

1. Add a version-resolution model that maps required overlay combinations to compatible release tags.
2. Keep this deferred until at least three non-core overlays are implemented so compatibility rules are based on real release history rather than speculation.
3. Implementation target:
	- single machine-readable compatibility source of truth
	- generated human-readable matrix/view
	- deterministic query workflow for architects (for example: required overlays + minimum maturity -> recommended tag)

## Recommended Overlay Implementation Order

1. CLI overlay (first proof-of-concept for overlay model)
2. UI overlay (high anticipated project demand)
3. API overlay (service boundary patterns)
4. Worker overlay (background execution patterns)
5. MCP server profile (backlog)
6. Scheduled jobs/cron profile (backlog)
7. Data/ETL pipeline profile (backlog)
8. Library/package-only profile (backlog)

## Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Core too opinionated | Reduces adoption | Keep framework and deployment choices out of core |
| Core too abstract | Not useful | Add concrete overlays with minimal dependencies |
| Agents too autonomous | Quality issues | Require tests, type checks, linting, and human review |
| Maintenance burden | Scaling issues | Clear separation of concerns; overlays are additive |

## Open Questions

1. **API Framework Selection**: Should the API overlay standardize on FastAPI, or remain abstract? *Recommendation: Standardize only when the API overlay is designed.*
2. **Generation Mechanism**: Should overlay generation be file-copy based or template-engine based? *Recommendation: Defer until core skeleton is stable.*
3. **Task Wrapper**: Should task execution use plain `uv` commands only or include a wrapper task runner? *Recommendation: Prefer uv first, add wrapper only if cross-platform ergonomics clearly improve.*

## Exit Criteria for v1

1. ✅ The core starter boundary is agreed.
2. ✅ The initial overlay set is agreed.
3. ✅ The validation stack is agreed.
4. ✅ Planning and handoff documents exist and are seeded.
5. ✅ The repository skeleton for implementation is ready.
6. ✅ All core modules have passing tests.
7. ✅ All overlays skeleton and pass validation.
8. ✅ Documentation is complete and current.
9. ✅ First v1 release is tagged (`v1.0.0`) and documented.
