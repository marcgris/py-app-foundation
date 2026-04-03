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
7. First-wave overlays for CLI, API, worker, and UI projects.
8. Planning artifacts and handoff process.

## Out of Scope

1. Cloud-specific deployment in v1.
2. Infrastructure provisioning.
3. Standardizing on a database or ORM.
4. Domain-specific business logic.
5. Organization process not required to operate the starter.

## Phase Plan

1. **Phase 1**: Planning artifacts, scope boundaries, and architecture decisions. ✅ Complete
2. **Phase 2**: Core template skeleton and repository structure. 🔄 In Progress
3. **Phase 3**: Agent workflow, validation stack, and CI guardrails.
4. **Phase 4**: CLI, API, worker, and UI overlays.
5. **Phase 5**: Validation, sample generation, and release readiness.

## Current Focus

- **Active Phase**: Phase 2
- **Objective**: Create the repository skeleton, planning documents, and core starter modules with passing validation.
- **Current Owner**: Initial scaffolding

## Upcoming Work

1. Complete core package modules (config.py, logging.py, exceptions.py).
2. Create test infrastructure with working fixtures and smoke tests.
3. Configure and validate the local CI workflow (uv sync, pytest, ruff, pyright, bandit).
4. Create the CLI overlay skeleton.
5. Create the API overlay skeleton.
6. Create the worker overlay skeleton.
7. Create the UI overlay skeleton.
8. Verify all four overlays pass validation.
9. Document the bootstrap and generation process.
10. Prepare v1 release and maintenance guidelines.

## Future Overlay Backlog

1. Scheduled jobs/cron profile.
2. Data/ETL pipeline profile.
3. MCP server profile.
4. Library/package-only profile.

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
5. 🔄 The repository skeleton for implementation is ready.
6. ⏳ All core modules have passing tests.
7. ⏳ All overlays skeleton and pass validation.
8. ⏳ Documentation is complete and current.
9. ⏳ First v1 release is tagged and documented.
