# Research: Todo CLI Core Functionality

**Purpose**: Document technical decisions and rationale for implementation
**Date**: 2026-01-01

## Decision: Task ID Generation Strategy

**Decision**: Use sequential integer IDs starting from 1, incrementing with each new task.

**Rationale**:
- Simple and predictable for users
- Easy to reference in CLI commands (e.g., "task 1")
- No complex UUID handling needed for Phase I scope
- Aligns with user expectation from specification

**Alternatives considered**:
- UUID: More robust but adds complexity for CLI references
- Timestamps: Unnecessary for in-memory, single-session use
- Random integers: Adds user confusion with gaps

## Decision: Data Structure for In-Memory Storage

**Decision**: Use Python dictionary with task ID as key for O(1) lookups.

**Rationale**:
- Fast access for update, delete, and get_by_id operations
- Simple iteration for list operations via .values()
- Built-in Python data structure, no dependencies
- Meets performance goal (<2 seconds for 1000 tasks)

**Alternatives considered**:
- List with linear search: O(n) lookups too slow for 1000+ tasks
- Custom class: Unnecessary complexity for Phase I
- Third-party data structures: Violates simplicity principle

## Decision: Error Handling Strategy

**Decision**: Use exceptions for error conditions with specific exception types for each error category.

**Rationale**:
- Pythonic error handling pattern
- Clear separation of error types (validation vs not found vs system errors)
- User-friendly error messages can be generated at exception handling layer
- Supports non-fatal error requirement

**Alternatives considered**:
- Return codes/None: Less Pythonic, harder to debug
- Silent failures: Violates user-friendly error requirement
- System exit: Violates non-fatal error requirement

## Decision: Command Parsing Library

**Decision**: Use Python's built-in argparse module.

**Rationale**:
- Standard library, no external dependencies
- Automatic help generation
- Built-in type validation for task IDs
- Familiar to Python developers

**Alternatives considered**:
- Manual sys.argv parsing: More complex, error-prone
- Click/third-party libraries: Unnecessary dependencies for Phase I
- Custom argument parser: Violates simplicity principle

## Decision: Task Display Format

**Decision**: Use plain text with visual indicators for completion status.

**Rationale**:
- Simple and readable in terminal
- Cross-platform compatible
- No color library dependencies
- Meets human-readable output requirement

**Format**:
- [✓] 1: Task title
- [ ] 2: Another task (description: optional)

**Alternatives considered**:
- Colored output: Requires dependencies (colorama)
- Table formatting: Unnecessary for Phase I complexity
- JSON output: Not human-readable for CLI users

## Summary of Decisions

All technical decisions align with Phase I constitution principles:
- ✅ Spec-first: Decisions directly address specification requirements
- ✅ No manual coding: Framework choices enable automated generation
- ✅ Determinism: No probabilistic behavior in decisions
- ✅ Simplicity: Only standard Python libraries and basic structures used
