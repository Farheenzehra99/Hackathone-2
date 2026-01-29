---
id: 001
title: constitution-amendment
stage: constitution
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: [system]
command: /sp.constitution
labels: [constitution,initial,governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - [N/A]
---

## Prompt

# Todo App – Phase I
## Spec-Driven Development Constitution

---

## 1. Scope & Purpose

This Constitution governs the **design, specification, and implementation**
of the **Todo App – Phase I**.

Phase I is strictly limited to:
- A **Python-based command-line (CLI) application**
- **In-memory task storage only**
- **Basic Todo functionality**
- **Spec-Driven Development using Claude Code**

This document is the **highest authority** for Phase I.
Any artifact (spec, plan, code, prompt) that violates this Constitution is invalid.

---

## 2. Core Principles

### 2.1 Spec-First Development
- Every feature MUST be fully specified **before** any code is generated.
- Specifications must be written in Markdown.
- Code generation is allowed **only after** specification approval.

### 2.2 No Manual Coding
- Human-written implementation code is strictly forbidden.
- All source code MUST be generated using **Claude Code**.
- Humans may only:
  - Write specs
  - Refine prompts
  - Validate outputs

### 2.3 Determinism Over Creativity
- The system must behave predictably.
- No probabilistic or creative behavior is allowed in Phase I.
- Given the same input, the system must produce the same output.

### 2.4 Simplicity by Design
- Phase I prioritizes clarity over extensibility.
- No abstractions for future phases.
- No premature optimization.

---

## 3. Functional Scope (Allowed)

The application MUST support **only** the following features:

1. Add Task
2. Update Task
3. Delete Task
4. View Task List
5. Mark Task as Complete / Incomplete

Each feature must be explicitly specified with:
- Inputs
- Expected behavior
- Error conditions
- Acceptance criteria

---

## 4. Explicitly Forbidden (Phase I)

The following are **NOT allowed** in Phase I:

- Databases or persistent storage
- APIs or web servers
- GUI or web interfaces
- Authentication or authorization
- Cloud services or containers
- Kubernetes, Docker, or DevOps tooling
- Event-driven or distributed systems
- Background jobs or schedulers
- AI autonomy or self-planning systems

Any reference to later phases invalidates the spec.

---

## 5. Data Model Constraints

### 5.1 Task Entity
Each task MUST contain:
- `id` (unique, immutable identifier)
- `title` (non-empty string)
- `description` (optional string)
- `completed` (boolean)

Optional fields may exist **only if explicitly specified**.

### 5.2 Storage Rules
- All tasks must exist **only in memory**
- No file I/O for persistence
- Data resets on application restart

---

## 6. Architectural Boundaries

### 6.1 Separation of Concerns
- State management must be isolated from user interaction logic.
- Input parsing must not mutate state.
- Output formatting must not contain business logic.

### 6.2 Agents vs Skills
- **Agents** orchestrate flow and enforce rules.
- **Skills** execute deterministic, reusable logic.
- Skills must not control application flow.

---

## 7. Error Handling Rules

- All errors must be:
  - Explicit
  - User-readable
  - Non-fatal
- The application must never crash due to invalid user input.
- Invalid operations must not mutate state.

---

## 8. Quality Standards

Generated code MUST:
- Follow clean Python structure
- Use clear, readable naming
- Avoid dead code and unused logic
- Be minimal and Phase I–appropriate

Generated specs MUST:
- Be unambiguous
- Be implementation-ready
- Avoid vague language

---

## 9. Validation & Acceptance

Phase I is considered **complete** only when:
- All 5 core features work as specified
- Behavior matches acceptance criteria exactly
- No forbidden features are present
- Code is fully generated via Claude Code
- Specs, plans, and code are consistent

---

## 10. Authority & Enforcement

- This Constitution overrides all other documents.
- In case of conflict:
  **Constitution → Spec → Plan → Code**
- Any violation requires rewriting the offending artifact.

---

## Final Statement

> **In Phase I, correctness beats cleverness.
> Simplicity beats scalability.
> Specification beats implementation.**

## Response snapshot

Constitution successfully created with version 1.0.0. All placeholders from the template were filled with the Todo App – Phase I governance content. Templates reviewed and confirmed compatible with the new constitution.

## Outcome

- ✅ Impact: Initial constitution established, defining Phase I scope, principles, and governance
- 🧪 Tests: N/A (constitution level)
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Ready for feature specification (/sp.specify)
- 🧠 Reflection: Constitution clearly delineates Phase I boundaries and enforces spec-first, no-manual-coding workflow

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification following constitutional principles
