# UI Overlay Contract

This document defines the public contract for the UI overlay family.

The UI overlay is implemented as a two-level model:

- Shared UI Base Contract (applies to every UI project)
- Profile Contract (Web, Desktop, or Mobile)

This model is designed for professional, maintainable, and extendable development without forcing a single runtime stack for all UI types.

## Scope

This contract applies to any generated project that selects the UI overlay.

It defines:

- Shared baseline obligations for all UI methods
- Platform profile obligations for Web, Desktop, and Mobile
- Compatibility and release-policy expectations

## Contract Model

Every UI project is composed as:

- UI Shared Base + exactly one platform profile (Web, Desktop, or Mobile)

Rules:

- Shared Base requirements are mandatory for all profiles.
- A profile may add requirements but may not weaken Shared Base guarantees.
- Optional capabilities must be additive and documented as flags.

## Status And Stability Policy

Initial status targets:

- UI Shared Base: `Experimental`
- Web profile: `Experimental`
- Desktop profile: `Experimental`
- Mobile profile: `Experimental`

Change policy while `Experimental`:

- Breaking changes are allowed only when explicitly called out in `CHANGELOG.md`.
- Any breaking change must update the compatibility matrix in `docs/guide/index.md`.
- Any contract narrowing or expansion must include test updates.

Promotion guidance:

- Promote any component from `Experimental` to `Beta` only after one full release cycle with passing validation and no unresolved material contract gaps.
- Track Shared Base and each profile maturity independently.

## Shared UI Base Contract

The following requirements apply to every UI profile.

### 1. Project Structure

The overlay must provide:

- A dedicated UI application root under the repository.
- A clear app entry point.
- A styles/theme location (or equivalent token location) that is safe to extend.
- A UI-focused usage section in docs that explains local development and extension points.

The specific framework/toolchain is intentionally not fixed by this shared contract.

### 2. Local Command Contract

The overlay must define deterministic local commands for:

- Starting the UI in development mode.
- Running UI validation checks.

Once a profile reaches `Beta`, these commands are frozen for one release cycle unless a documented breaking change is approved.

### 3. Configuration Contract

The overlay must document:

- Which runtime values are environment-driven.
- Which defaults are safe for local development.
- Which values are required for non-local environments.

### 4. Integration Boundary Contract

The overlay must define a local integration boundary to backend services:

- How UI code targets backend endpoints locally.
- How unavailable backend dependencies are handled.
- Which fallback behavior is expected during local development.

### 5. Shared Smoke Contract

Every UI profile must satisfy a minimal smoke contract:

- The app starts with the documented local command.
- The app renders a deterministic startup marker.
- The marker is testable in automation.

The deterministic marker can be title text, route content, window label, or equivalent profile-specific signal.

### 6. Documentation And Release Contract

Any UI overlay change must keep these docs aligned:

- `docs/guide/index.md`
- `docs/plan/ROADMAP.md`
- `CHANGELOG.md`

## Platform Profile Contracts

Each profile inherits the Shared UI Base Contract and adds platform-specific obligations.

### Web Profile Contract

- Defines web runtime and local dev server behavior.
- Defines browser-render smoke behavior with deterministic marker validation.
- Defines browser-focused build/test workflow expectations.

### Desktop Profile Contract

- Defines desktop runtime packaging and local launch behavior.
- Defines application-window smoke behavior with deterministic marker validation.
- Defines desktop-specific build/test workflow expectations.

### Mobile Profile Contract

- Defines mobile runtime boot behavior for local development.
- Defines initial-screen smoke behavior with deterministic marker validation.
- Defines mobile-specific build/test workflow expectations.

## Optional Capability Flags

Optional capabilities (for example, routing shell, auth shell, telemetry bootstrap, offline cache) must follow these rules:

- Flags are additive and optional.
- Flags must declare supported profiles.
- Flags must include explicit test coverage and documentation.
- Flags may not change baseline behavior when not enabled.

## Non-Goals

This contract does not standardize:

- One mandatory framework across Web, Desktop, and Mobile.
- Deployment topology.
- Backend API framework choice.
- Full design-system implementation in the first profile release.

## Enforcement

Contract expectations are enforced by:

- Smoke tests for startup and deterministic marker behavior per profile.
- Validation checks documented by each profile.
- Release checklist requirements, including matrix and changelog updates.
- Human review for contract-level changes.

## Compatibility Matrix Expectations

The compatibility matrix in `docs/guide/index.md` must represent:

- UI Shared Base status
- Web profile status
- Desktop profile status
- Mobile profile status

Status values follow the project legend: Planned, Backlog, Experimental, Beta, Stable.

## Implementation Exit Criteria

UI overlay contract implementation is complete when:

1. Shared UI Base requirements are implemented and validated.
2. At least one profile is implemented with passing smoke and validation checks.
3. Compatibility matrix rows are updated for Shared Base and implemented profile(s).
4. Release notes capture any compatibility-impacting behavior changes.
