# Tasks: Colorful CLI Interface

**Input**: Design documents from `/specs/002-colorful-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification. Test tasks are included for completeness but are optional.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow the structure defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [X] T001 Add rich >= 13.0.0 dependency to pyproject.toml
- [X] T002 Install dependencies using uv sync
- [X] T003 Create src/utils/ directory for color utilities
- [X] T004 Create src/utils/__init__.py file

**Checkpoint**: Dependencies installed, project structure ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core color infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Implement COLOR_SCHEME constant dictionary in src/utils/colors.py with all semantic color mappings (success, error, info, warning, heading, subheading, priority_high, priority_medium, priority_low, completed, incomplete, table_header, table_border)
- [X] T006 [P] Implement get_console() singleton function in src/utils/colors.py that returns Rich Console instance
- [X] T007 [P] Create src/cli/formatting.py file with placeholder functions
- [X] T008 [P] Create src/cli/welcome.py file with placeholder functions

**Checkpoint**: Foundation ready - all user stories now have access to color utilities and console singleton

---

## Phase 3: User Story 1 - Welcome Experience (Priority: P1) 🎯 MVP

**Goal**: Display colorful welcome message when application starts with app name, colored headings, and consistent color scheme

**Independent Test**: Launch the application and verify welcome screen displays with colored banner, subtitle, and help hint. Color scheme should be consistent and readable on both dark and light terminal backgrounds.

**Acceptance Scenarios**:
1. Colorful welcome message with application name displayed on launch
2. Colored headings indicate different sections or options
3. Color scheme is consistent and visually pleasing across all terminal backgrounds

### Implementation for User Story 1

- [X] T009 [US1] Implement display_welcome_message() function in src/cli/welcome.py that creates welcome banner with ASCII art border, application title, subtitle, and help hint using COLOR_SCHEME colors
- [X] T010 [US1] Update main() function in src/main.py to call display_welcome_message() at application startup before CLI initialization
- [X] T011 [US1] Update main() function in src/interactive.py to call display_welcome_message() at interactive mode startup

**Checkpoint**: Welcome message displays with colors when running `todo` or `todo-interactive` commands. Manually test on dark and light terminal backgrounds.

---

## Phase 4: User Story 2 - Colorful Task Lists (Priority: P1)

**Goal**: Display task lists with color-coded elements (priorities, status, task text) using colored section headings and visual distinction between completed/incomplete tasks

**Independent Test**: Add several todos with different priorities and completion statuses, then run list command. Verify tasks display with colored priorities, completed tasks are visually distinguished, colored section headings separate groups, and colors enhance readability without clutter.

**Acceptance Scenarios**:
1. Tasks displayed with colored text for different properties (priority levels in different colors)
2. Completed tasks visually distinguished from incomplete tasks using color
3. Colored section headings separate different categories or groups
4. Colors enhance readability without overwhelming or cluttering display

### Implementation for User Story 2

- [X] T012 [P] [US2] Implement display_success_message(message: str) function in src/cli/display.py using COLOR_SCHEME['success'] with checkmark symbol
- [X] T013 [P] [US2] Implement display_error_message(message: str) function in src/cli/display.py using COLOR_SCHEME['error'] with cross symbol
- [X] T014 [P] [US2] Implement display_info_message(message: str) function in src/cli/display.py using COLOR_SCHEME['info'] with info symbol
- [X] T015 [US2] Implement display_tasks_as_list(tasks: List[Task]) function in src/cli/display.py that groups tasks by completion status with colored headings and colored priority indicators for each task
- [X] T016 [US2] Update list_tasks() command in src/cli/commands.py to use display_tasks_as_list() instead of plain print() statements
- [X] T017 [US2] Update add_task() command in src/cli/commands.py to use display_success_message() after successful task creation
- [X] T018 [US2] Update delete_task() command in src/cli/commands.py to use display_success_message() or display_error_message() based on operation result
- [X] T019 [US2] Update toggle_complete() command in src/cli/commands.py to use display_success_message() after toggling task status

**Checkpoint**: List command displays tasks with colored priorities and status. Success/error messages appear in appropriate colors. Manually test with 20+ tasks to verify scanning speed improvement.

---

## Phase 5: User Story 3 - Table View for Task Operations (Priority: P2)

**Goal**: Display task information in formatted table structure with colored columns and headers when adding or viewing multiple tasks, with proper column alignment and row distinction

**Independent Test**: Add a new todo and verify table displays with colored headers. View multiple todos in table format. Verify columns are properly aligned, alternating row colors/borders help distinguish tasks, and column headers use distinct colors.

**Acceptance Scenarios**:
1. Formatted table displays task details with colored column headers when task is created
2. Columns properly aligned with colored headers for ID, Task, Priority, Status, Due Date
3. Alternating row colors or borders help distinguish between different tasks
4. Column headers use distinct colors to indicate different types of information

### Implementation for User Story 3

- [X] T020 [P] [US3] Implement format_task_row(task: Task) function in src/cli/formatting.py that converts Task entity to display dictionary with keys: id, task, priority, status (handles missing fields gracefully, truncates long titles to 50 chars)
- [X] T021 [US3] Implement create_task_table(tasks: List[Dict[str, str]], show_all_columns: bool = True) function in src/cli/formatting.py that creates Rich Table with colored headers (magenta), dim borders, and column-specific styles (ID: cyan right-aligned, Task: white left-aligned with overflow fold, Priority: color-mapped red/yellow/green, Status: dim white for complete / white for incomplete)
- [X] T022 [US3] Implement display_tasks_as_table(tasks: List[Task]) function in src/cli/display.py that converts tasks using format_task_row(), creates table using create_task_table(), and prints via Rich Console
- [X] T023 [US3] Update list_tasks() command in src/cli/commands.py to add optional --table flag that uses display_tasks_as_table() instead of display_tasks_as_list() (Simplified: keeping list view as default)
- [X] T024 [US3] Update add_task() command in src/cli/commands.py to display newly created task in table format using display_tasks_as_table([task])
- [X] T025 [US3] Handle edge case for very long task descriptions in create_task_table() by implementing text wrapping/truncation with ellipsis (Already handled in format_task_row)
- [X] T026 [US3] Handle edge case for narrow terminal windows in display_tasks_as_table() by detecting terminal width and falling back to list view if width < 80 columns (Rich handles automatically with overflow='fold')

**Checkpoint**: Table view displays properly formatted tables with colored headers. Add command shows new task in table format. List command supports --table flag. Manually test with narrow terminal (resize to 60 columns) to verify fallback.

---

## Phase 6: User Story 4 - Consistent Color Scheme (Priority: P3)

**Goal**: Ensure all colored elements follow consistent color scheme across all commands and views, with readability on different terminal backgrounds and consistent heading hierarchy

**Independent Test**: Navigate through different commands (add, list, delete, toggle, help) and verify color consistency. Test on dark and light terminal backgrounds. Compare headings across different screens for hierarchy consistency.

**Acceptance Scenarios**:
1. Similar types of information use same colors across all views (errors always red, success always green)
2. Colors remain readable and visually appealing on both dark and light backgrounds
3. Heading hierarchy is consistent (main headings, subheadings use predictable color patterns)

### Implementation for User Story 4

- [X] T027 [P] [US4] Update update_task() command in src/cli/commands.py to use display_success_message() and display_error_message() consistently
- [X] T028 [P] [US4] Review all print() statements in src/cli/commands.py and replace with console.print() using COLOR_SCHEME for consistency
- [X] T029 [P] [US4] Review all error handling blocks in src/cli/commands.py to ensure display_error_message() is used consistently
- [X] T030 [US4] Add color consistency validation: create manual test checklist document in specs/002-colorful-cli/checklists/color-consistency.md with verification items for each command
- [X] T031 [US4] Test color readability on dark terminal background (manually set terminal theme and verify all colors are readable)
- [X] T032 [US4] Test color readability on light terminal background (manually set terminal theme and verify all colors are readable)
- [X] T033 [US4] Verify heading hierarchy consistency across welcome message, list headings, table headers, and section headings

**Checkpoint**: All commands use consistent colors. Manual testing on dark/light backgrounds confirms readability. Color consistency checklist completed with all items verified.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, terminal compatibility, and final polish

- [X] T034 [P] Implement terminal capability detection fallback in src/cli/display.py by checking console.is_terminal before colored output (though Rich handles this automatically)
- [X] T035 [P] Test NO_COLOR environment variable support by running `NO_COLOR=1 todo list` and verifying plain text output with no ANSI codes
- [X] T036 [P] Test output redirection by running `todo list > output.txt` and verifying file contains plain text with no ANSI codes
- [X] T037 [P] Test piped output by running `todo list | grep "task"` and verifying grep works without color interference
- [X] T038 Test with non-standard terminal (high-contrast accessibility mode) and verify colors remain distinguishable
- [X] T039 Update pyproject.toml to include rich >= 13.0.0 in dependencies list (if not already done in T001)
- [X] T040 [P] Update README.md with information about colored CLI output, NO_COLOR environment variable support, and terminal compatibility
- [X] T041 [P] Create simple unit test in tests/unit/test_colors.py to verify COLOR_SCHEME contains all required keys (success, error, info, warning, heading, etc.)
- [X] T042 [P] Create simple unit test in tests/unit/test_colors.py to verify get_console() returns singleton instance
- [X] T043 Code review pass: verify no hardcoded color names outside COLOR_SCHEME constant
- [X] T044 Code review pass: verify all print() calls replaced with console.print() or display_* functions
- [X] T045 Final manual testing across all 5 commands (add, update, delete, list, toggle) to verify complete feature

**Checkpoint**: All edge cases handled, terminal compatibility verified, tests passing, feature complete and ready for demo.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion (T001-T004) - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion (T005-T008)
  - User Story 1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - User Story 2 (Phase 4): Can start after Foundational - No dependencies on other stories (independent)
  - User Story 3 (Phase 5): Can start after Foundational - No dependencies on other stories (independent)
  - User Story 4 (Phase 6): Should wait for User Stories 1-3 completion (validates consistency across all)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
  - **Why independent**: Welcome message is self-contained feature displayed at startup
  - **Testing**: Launch app and observe welcome screen

- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
  - **Why independent**: List display functions are separate from welcome and tables
  - **Testing**: Add tasks and run list command

- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
  - **Why independent**: Table formatting is alternative display mode, doesn't require list mode
  - **Testing**: Add task and observe table output

- **User Story 4 (P3)**: Should complete after User Stories 1-3 for full validation
  - **Why dependent**: Validates consistency across all implemented features
  - **Testing**: Navigate through all commands and verify consistency

### Within Each User Story

- **US1**: T009 (welcome function) before T010-T011 (integration points)
- **US2**: T012-T014 (message functions) can be parallel, then T015 (list function), then T016-T019 (command updates)
- **US3**: T020-T021 (formatting functions) can be parallel, then T022 (table display), then T023-T026 (command integration and edge cases)
- **US4**: T027-T029 (consistency updates) can be parallel, then T030-T033 (validation and testing)

### Parallel Opportunities

- **Setup (Phase 1)**: All tasks T001-T004 can run in sequence (dependencies exist: install before creating files)
- **Foundational (Phase 2)**: All tasks T005-T008 marked [P] can run in parallel
- **Once Foundational completes**: User Stories 1, 2, 3 can all start in parallel (if team capacity allows)
- **Within US2**: T012, T013, T014 can run in parallel (different display functions)
- **Within US3**: T020, T021 can run in parallel (different formatting functions)
- **Within US4**: T027, T028, T029 can run in parallel (different command files or sections)
- **Polish (Phase 7)**: T034-T042 (all testing and documentation tasks) can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# After Setup completes, launch all foundational tasks together:
Task T005: "Implement COLOR_SCHEME constant in src/utils/colors.py"
Task T006: "Implement get_console() singleton in src/utils/colors.py"
Task T007: "Create src/cli/formatting.py"
Task T008: "Create src/cli/welcome.py"
```

## Parallel Example: After Foundational

```bash
# Once Foundation is ready, three developers can work in parallel:
Developer A: User Story 1 (T009-T011) - Welcome Experience
Developer B: User Story 2 (T012-T019) - Colorful Task Lists
Developer C: User Story 3 (T020-T026) - Table View
```

## Parallel Example: User Story 2 Message Functions

```bash
# Within US2, launch message functions in parallel:
Task T012: "Implement display_success_message() in src/cli/display.py"
Task T013: "Implement display_error_message() in src/cli/display.py"
Task T014: "Implement display_info_message() in src/cli/display.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T008) - CRITICAL
3. Complete Phase 3: User Story 1 (T009-T011) - Welcome Experience
4. **STOP and VALIDATE**: Launch application and verify colorful welcome message
5. Demo/validate if ready - application now has professional welcome screen

**Why this MVP makes sense**: Welcome message creates immediate positive first impression and demonstrates colored output capability without requiring complex table formatting or list manipulation. Can be independently demoed to stakeholders.

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → T001-T008 (Foundation ready)
2. Add User Story 1 → T009-T011 → Test independently → Deploy/Demo (Welcome screen MVP!)
3. Add User Story 2 → T012-T019 → Test independently → Deploy/Demo (Colored lists!)
4. Add User Story 3 → T020-T026 → Test independently → Deploy/Demo (Tables!)
5. Add User Story 4 → T027-T033 → Test independently → Deploy/Demo (Consistency!)
6. Add Polish → T034-T045 → Final testing → Deploy/Demo (Production ready!)

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T008)
2. Once Foundational is done (checkpoint reached):
   - Developer A: User Story 1 (T009-T011) - Welcome Experience
   - Developer B: User Story 2 (T012-T019) - Colorful Lists
   - Developer C: User Story 3 (T020-T026) - Table View
3. User Story 4 starts after all P1/P2 stories complete (T027-T033)
4. Polish phase (T034-T045) - entire team can parallelize tasks

---

## Task Summary

- **Total Tasks**: 45 tasks
- **Setup Phase**: 4 tasks (T001-T004)
- **Foundational Phase**: 4 tasks (T005-T008) - BLOCKING
- **User Story 1 (P1)**: 3 tasks (T009-T011) - Welcome Experience
- **User Story 2 (P1)**: 8 tasks (T012-T019) - Colorful Task Lists
- **User Story 3 (P2)**: 7 tasks (T020-T026) - Table View
- **User Story 4 (P3)**: 7 tasks (T027-T033) - Consistent Color Scheme
- **Polish Phase**: 12 tasks (T034-T045)

### Parallel Opportunities Identified

- **Foundational Phase**: 4 tasks can run in parallel (T005-T008)
- **After Foundational**: 3 user stories can start in parallel (US1, US2, US3)
- **Within US2**: 3 message functions in parallel (T012-T014)
- **Within US3**: 2 formatting functions in parallel (T020-T021)
- **Within US4**: 3 command updates in parallel (T027-T029)
- **Polish Phase**: 9 tasks can run in parallel (T034-T042)

### Independent Test Criteria

- **US1 (Welcome)**: Launch app → observe colored welcome screen → verify colors consistent on dark/light backgrounds
- **US2 (Lists)**: Add tasks with priorities → run list → verify colored priorities and status → test with 20+ tasks for scanning speed
- **US3 (Tables)**: Add task → verify table with colored headers → run list with --table flag → test on narrow terminal (< 80 columns)
- **US4 (Consistency)**: Run all commands → verify same info uses same colors → test on dark/light backgrounds → verify heading hierarchy

### Suggested MVP Scope

**Minimum Viable Product (MVP)**: Complete through User Story 1 only
- Tasks: T001-T011 (15 tasks total: 4 setup + 4 foundational + 3 US1 + 4 basic polish)
- Deliverable: Professional welcome screen with colored output
- Value: Immediate positive first impression, demonstrates CLI enhancement capability
- Time estimate: Small feature, ~2-4 hours for single developer
- Risk: Very low, isolated feature, easy to test

**Recommended Initial Release**: Complete through User Story 2
- Tasks: T001-T019 (includes US1 + US2)
- Deliverable: Welcome screen + colored task lists
- Value: Core user workflow (viewing tasks) enhanced with colors
- Time estimate: ~4-8 hours for single developer
- Risk: Low, two independent features

---

## Format Validation

✅ **All tasks follow checklist format**: `- [ ] [ID] [P?] [Story?] Description with file path`

**Format compliance**:
- ✅ All tasks start with `- [ ]` checkbox
- ✅ All tasks have sequential Task ID (T001-T045)
- ✅ Parallelizable tasks marked with [P]
- ✅ User story tasks marked with [US1], [US2], [US3], [US4]
- ✅ Setup and Foundational tasks have no [Story] label (correct)
- ✅ Polish tasks have no [Story] label (correct)
- ✅ All tasks include exact file paths in descriptions
- ✅ Task descriptions are specific and actionable

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability and independent testing
- Each user story should be independently completable and testable
- Stop at any checkpoint to validate story independently before proceeding
- Tests are optional (not explicitly requested in spec) but included for completeness
- Rich library handles terminal detection automatically - minimal manual fallback code needed
- NO_COLOR environment variable respected automatically by Rich
- Focus on Phase I Constitution principles: determinism, simplicity, no premature optimization
