# Design Decisions

Lightweight ADR-style log. Newest first.

---

## Decision D-008

**Date**: 2026-04-03  
**Status**: Accepted  
**Decision**: Expand near-term overlays to four (CLI, API, worker, UI) and track four additional overlay candidates as backlog (scheduled jobs, data/ETL, MCP server, library-only).

**Context**: Near-term project demand includes UI-heavy work, while several additional project shapes are likely but not immediate implementation priorities.

**Alternatives Considered**:
- Keep only three overlays until all are implemented
- Add many overlays immediately

**Consequences**: The roadmap reflects near-term priorities clearly while preserving focus by separating planned overlays from future candidates.

**Follow-up**: Keep the overlay compatibility matrix current as overlays move from planned to implemented and stable.

---

## Decision D-007

**Date**: 2026-03-29  
**Status**: Superseded by D-008  
**Decision**: Start with three overlays only: CLI, API, and worker.

**Context**: The starter must be reusable without becoming too abstract or too fragmented.

**Alternatives Considered**:
- Core only (no overlays)
- Many specialized templates from day one

**Consequences**: v1 remains focused and practical; less maintenance overhead. New overlay types can be added later when demand justifies the effort.

**Follow-up**: Define the precise boundary of each overlay during detailed architecture refinement.

---

## Decision D-006

**Date**: 2026-03-29  
**Status**: Accepted  
**Decision**: Prefer `uv` for environment and dependency management.

**Context**: The starter should optimize for speed, simplicity, and a modern Python workflow.

**Alternatives Considered**:
- pip-tools
- Poetry
- Hatch

**Consequences**: Simpler default workflow; faster local feedback; revisit only if downstream constraints emerge.

**Follow-up**: Ensure uv is well-documented in the contributor guide and bootstrap instructions.

---

## Decision D-005

**Date**: 2026-03-29  
**Status**: Accepted  
**Decision**: Prefer `pyright` as the default type checker.

**Context**: The starter should align with VS Code workflows and fast local feedback.

**Alternatives Considered**:
- mypy only
- Dual support (mypy + pyright)

**Consequences**: Strong editor integration and fast checks; revisit only if policy requirements demand mypy.

**Follow-up**: Define the strictness baseline in pyproject.toml configuration.

---

## Decision D-004

**Date**: 2026-03-29  
**Status**: Accepted  
**Decision**: Keep deployment abstract in v1.

**Context**: The deployment target is not yet selected and should not distort the starter design.

**Alternatives Considered**:
- Optimize for containers from the start
- Optimize for serverless from the start

**Consequences**: The starter remains reusable; deployment guidance can be added later as an optional layer.

**Follow-up**: Revisit once the first real downstream projects appear and reveal deployment constraints.

---

## Decision D-003

**Date**: 2026-03-29  
**Status**: Accepted  
**Decision**: Agents may implement changes but must not merge.

**Context**: The workflow should benefit from autonomous code generation without removing human review.

**Alternatives Considered**:
- Plan-only agents
- Agents that auto-merge

**Consequences**: Strong guardrails with useful automation. Humans decide what makes it to main.

**Follow-up**: Define the PR review and validation rules that support this boundary.

---

## Decision D-002

**Date**: 2026-03-29  
**Status**: Accepted  
**Decision**: Use balanced security defaults.

**Context**: The starter should be secure by default without imposing heavy compliance friction on every project.

**Alternatives Considered**:
- Lightweight defaults
- High-assurance defaults

**Consequences**: Strong automated checks in local and CI workflows, with room to tighten later if needed.

**Follow-up**: Define the exact scanning and gating stack in CI workflows.

---

## Decision D-001

**Date**: 2026-03-29  
**Status**: Accepted  
**Decision**: Use one core starter plus overlays rather than many separate base templates.

**Context**: The starter must support multiple Python app types while preserving consistency and reuse.

**Alternatives Considered**:
- One generic template only
- Separate independent templates for each app type

**Consequences**: Shared engineering foundation with limited specialization overhead. Easier to maintain and evolve.

**Follow-up**: Define the responsibilities of the core and the initial overlays.

---
