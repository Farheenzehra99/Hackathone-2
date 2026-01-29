<!--
Sync Impact Report:
- Version change: [NONE] → 1.0.0
- Modified principles: N/A (initial version)
- Added sections: All sections (initial version)
- Removed sections: N/A (initial version)
- Templates requiring updates:
  ✅ plan-template.md (reviewed - Constitution Check section present, aligned with new principles)
  ✅ spec-template.md (reviewed - functional scope, requirements, success criteria sections aligned)
  ✅ tasks-template.md (reviewed - task categorization compatible with principles)
  ℹ️ No updates needed to templates - they are generic and compatible with Phase I constraints
- Follow-up TODOs: None
-->

# Todo App – Phase I Constitution

## Core Principles

### I. Spec-First Development
Every feature MUST be fully specified before any code is generated. Specifications must be written in Markdown. Code generation is allowed only after specification approval.

**Rationale**: Prevents implementation drift, ensures business requirements drive design, and creates a clear contract between requirements and implementation.

### II. No Manual Coding
Human-written implementation code is strictly forbidden. All source code MUST be generated using Claude Code. Humans may only write specs, refine prompts, and validate outputs.

**Rationale**: Ensures consistency with specification, eliminates human error in implementation details, and enforces the spec-first workflow.

### III. Determinism Over Creativity
The system must behave predictably. No probabilistic or creative behavior is allowed in Phase I. Given same input, system must produce same output.

**Rationale**: Ensures reliability, testability, and predictable behavior that can be verified against specification.

### IV. Simplicity by Design
Phase I prioritizes clarity over extensibility. No abstractions for future phases. No premature optimization.

**Rationale**: Keeps implementation focused, maintainable, and aligned with Phase I scope. Prevents over-engineering and complexity that doesn't serve current requirements.

## Functional Scope

The application MUST support only the following features:

1. Add Task
2. Update Task
3. Delete Task
4. View Task List
5. Mark Task as Complete / Incomplete

Each feature must be explicitly specified with inputs, expected behavior, error conditions, and acceptance criteria.

## Explicitly Forbidden (Phase I)

The following are NOT allowed in Phase I:

- Databases (SQL, NoSQL, or external database systems)
- APIs or web servers
- GUI or web interfaces
- Authentication or authorization
- Cloud services or containers
- Kubernetes, Docker, or DevOps tooling
- Event-driven or distributed systems
- Background jobs or schedulers
- AI autonomy or self-planning systems

Any reference to later phases invalidates spec.

## Data Model Constraints

### Task Entity
Each task MUST contain:
- `id` (unique, immutable identifier)
- `title` (non-empty string)
- `description` (optional string)
- `completed` (boolean)

Optional fields may exist only if explicitly specified.

### Storage Rules
Tasks must be persisted to a local JSON file to maintain state across CLI command invocations. The application uses in-memory storage as the primary data structure, with automatic file synchronization on each operation. No external databases or network storage allowed.

## Architectural Boundaries

### Separation of Concerns
State management must be isolated from user interaction logic. Input parsing must not mutate state. Output formatting must not contain business logic.

### Agents vs Skills
Agents orchestrate flow and enforce rules. Skills execute deterministic, reusable logic. Skills must not control application flow.

## Error Handling Rules

All errors must be explicit, user-readable, and non-fatal. The application must never crash due to invalid user input. Invalid operations must not mutate state.

## Quality Standards

Generated code MUST follow clean Python structure, use clear and readable naming, avoid dead code and unused logic, and be minimal and Phase I–appropriate.

Generated specs MUST be unambiguous, be implementation-ready, and avoid vague language.

## Validation & Acceptance

Phase I is considered complete only when:
- All 5 core features work as specified
- Behavior matches acceptance criteria exactly
- No forbidden features are present
- Code is fully generated via Claude Code
- Specs, plans, and code are consistent

## Governance

This Constitution overrides all other documents. In case of conflict: Constitution → Spec → Plan → Code. Any violation requires rewriting the offending artifact.

**Version**: 1.1.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01

## Amendment History

### v1.1.0 (2026-01-01)
**Reason**: CLI process lifecycle limitation - each `uv run todo <command>` creates new process, requiring persistence across invocations for multi-command workflows to function.

**Changes**:
- Removed blanket ban on "persistent storage"
- Updated to allow minimal local file-based persistence (JSON)
- Clarified that external databases remain forbidden
- Updated Storage Rules to require JSON file synchronization
