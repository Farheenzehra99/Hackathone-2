# Tasks: Todo CLI Core Functionality

**Input**: Design documents from `/specs/001-todo-cli-core/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, cli-interface.md

**Tests**: No tests specified in feature requirements. Tests will be generated if user requests TDD approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow single project structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create Python project structure per implementation plan
- [x] T002 Initialize Python 3.11+ project with argparse dependency
- [x] T003 Create __init__.py files for src/ and src/cli/, src/models/, src/services/ packages

**Checkpoint**: Foundation ready - project structure established

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Task data model in src/models/task.py with id, title, description, completed fields
- [x] T005 Implement Task validation logic in src/models/task.py (title non-empty, id immutable)
- [x] T006 Create in-memory storage structure in src/services/task_manager.py (dictionary-based)
- [x] T007 Implement sequential ID generation in src/services/task_manager.py
- [x] T008 Add error types for validation and operation errors in src/services/task_manager.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks with title and optional description

**Independent Test**: User can run application, add task with title, see task in list

### Implementation for User Story 1

- [x] T009 [US1] Implement create_task operation in src/services/task_manager.py
- [x] T010 [US1] Implement command-line Add command parser in src/cli/commands.py
- [x] T011 [US1] Create Add command handler in src/cli/commands.py that calls create_task
- [x] T012 [US1] Create task creation success message formatter in src/cli/display.py
- [x] T013 [US1] Create error message formatter for title validation in src/cli/display.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P1) 🎯 MVP

**Goal**: Enable users to see all their tasks with IDs, titles, descriptions, and completion status

**Independent Test**: User creates multiple tasks and can view complete task list

### Implementation for User Story 2

- [x] T014 [US2] Implement list_tasks operation in src/services/task_manager.py
- [x] T015 [US2] Implement command-line List command parser in src/cli/commands.py
- [x] T016 [US2] Create List command handler in src/cli/commands.py that calls list_tasks
- [x] T017 [US2] Create task list display formatter in src/cli/display.py with completion indicators
- [x] T018 [US2] Create empty task list message formatter in src/cli/display.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both be functional and testable independently

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P1) 🎯 MVP

**Goal**: Enable users to toggle task completion status

**Independent Test**: User creates tasks, marks some as complete, sees updated status, can mark back incomplete

### Implementation for User Story 3

- [x] T019 [US3] Implement toggle_complete operation in src/services/task_manager.py
- [x] T020 [US3] Implement command-line Complete command parser in src/cli/commands.py
- [x] T021 [US3] Create Complete command handler in src/cli/commands.py that calls toggle_complete
- [x] T022 [US3] Create success message formatter for completion toggle in src/cli/display.py
- [x] T023 [US3] Create error message formatter for task not found in src/cli/display.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all be functional and testable independently

---

## Phase 6: User Story 4 - Update Task (Priority: P2)

**Goal**: Enable users to modify existing tasks by changing title or description

**Independent Test**: User creates task, updates title/description, sees changes reflected in task list

### Implementation for User Story 4

- [x] T024 [US4] Implement update_task operation in src/services/task_manager.py
- [x] T025 [US4] Implement command-line Update command parser in src/cli/commands.py
- [x] T026 [US4] Create Update command handler in src/cli/commands.py that calls update_task
- [x] T027 [US4] Create success message formatter for task update in src/cli/display.py
- [x] T028 [US4] Create error message formatter for update validation in src/cli/display.py

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all be functional

---

## Phase 7: User Story 5 - Delete Task (Priority: P2)

**Goal**: Enable users to remove tasks they no longer need

**Independent Test**: User creates multiple tasks, deletes one, sees task no longer in list while others remain

### Implementation for User Story 5

- [x] T029 [US5] Implement delete_task operation in src/services/task_manager.py
- [x] T030 [US5] Implement command-line Delete command parser in src/cli/commands.py
- [x] T031 [US5] Create Delete command handler in src/cli/commands.py that calls delete_task
- [x] T032 [US5] Create success message formatter for task deletion in src/cli/display.py
- [x] T033 [US5] Create error message formatter for delete operation in src/cli/display.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Help & CLI Integration

**Purpose**: Provide help information and integrate all commands into main entry point

- [x] T034 Create help command handler in src/cli/commands.py
- [x] T035 Create main entry point in src/main.py with argparse configuration
- [x] T036 Wire all command handlers to main.py
- [x] T037 Add command routing logic to main.py
- [x] T038 Test that invalid commands display help

**Checkpoint**: Complete CLI interface with all 5 core features

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories proceed sequentially (US1 → US2 → US3 → US4 → US5) as specified in plan
- **Help & CLI Integration (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Task creation, command parsing, and output formatting are sequential
- Each story can be implemented independently once Foundational phase is complete

### Parallel Opportunities

- No parallel execution possible for user stories due to sequential nature defined in plan
- Foundation tasks T004-T008 must complete before any user story tasks
- Help & CLI Integration tasks can begin after user stories are complete

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (View Task List)
5. Complete Phase 5: User Story 3 (Mark Complete/Incomplete)
6. **STOP and VALIDATE**: Test User Stories 1-3 independently
7. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deliver MVP increment
3. Add User Story 2 → Test independently → Deliver increment
4. Add User Story 3 → Test independently → Deliver increment
5. Add User Story 4 → Test independently → Deliver increment
6. Add User Story 5 → Test independently → Deliver increment
7. Complete Help & CLI Integration → Deliver increment

Each story adds value without breaking previous stories.

---

## Notes

- No [P] tasks - implementation is sequential for Phase I
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable after Foundational phase
- Task IDs follow sequential pattern: T001-T038
- File paths follow single project structure: src/models/, src/services/, src/cli/, tests/
- No tests generated (not requested in feature spec)
- Verify each task before marking complete
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, missing file paths, story-independent order violations
