# Implementation Tasks: AI Todo Chatbot Integration

**Feature**: 001-ai-chatbot | **Date**: 2026-02-06 | **Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)

## Summary

Implement intelligent AI chatbot with Cohere API, 6 MCP tools, stateless backend endpoint, conversation persistence, and premium glassmorphic chat UI. Tasks organized by user story for independent, incremental delivery.

**Total Tasks**: 52 tasks across 8 phases
**Parallel Opportunities**: 28 parallelizable tasks marked with [P]
**MVP Scope**: Phase 3 (User Story 1 - Basic Task Creation)

## Implementation Strategy

**Approach**: Incremental delivery by user story priority
- Each story phase is independently testable
- P1 stories (US1-US3, US9) deliver core MVP
- P2 stories (US4, US5, US7, US8) add advanced features
- P3 stories (US6) add nice-to-have features

**Parallel Execution**: 4 specialized agents
- Agent 1 (Database): T003-T007 simultaneously
- Agent 2 (Tools): T008-T019 simultaneously after T007
- Agent 3 (Backend): T020-T027 after T019
- Agent 4 (Frontend): T028-T045 after T027

## Phase 1: Setup & Infrastructure (6 tasks)

**Goal**: Prepare development environment and install dependencies

- [X] T001 Add Cohere SDK to backend requirements.txt (cohere>=5.0.0)
- [X] T002 Update .env.example with COHERE_API_KEY placeholder
- [X] T003 [P] Create backend/app/tools/ directory structure
- [X] T004 [P] Create backend/app/services/ directory for Cohere client
- [X] T005 [P] Create frontend/components/chatbot/ directory structure
- [X] T006 [P] Create frontend/lib/api/chat.ts API client file

## Phase 2: Database Foundation (2 tasks)

**Goal**: Create conversation persistence infrastructure

- [X] T007 Create Conversation model in backend/app/models/conversation.py with id, user_id (FK, indexed), created_at, updated_at
- [X] T008 Create Message model in backend/app/models/message.py with id, conversation_id (FK, indexed), role, content, tool_calls, created_at
- [X] T009 Create Alembic migration for Conversation and Message tables with indexes

## Phase 3: User Story 1 - Basic Task Creation via Chat (P1) (8 tasks)

**Story Goal**: Users create tasks via natural language without forms

**Independent Test**: Open chatbot → type "Add a task to buy groceries" → verify task created and confirmation displayed

### Backend Tasks

- [X] T010 [P] [US1] Implement add_task tool in backend/app/tools/add_task.py (validate user_id, create task, return {success, task, error})
- [X] T011 [P] [US1] Create Cohere client service in backend/app/services/cohere_client.py with chat() method, model=command-r-plus, temperature=0.3
- [X] T012 [US1] Create tool executor in backend/app/services/tool_executor.py with execute_tool() and parse_tool_call() methods
- [X] T013 [US1] Implement chat endpoint POST /api/{user_id}/chat in backend/app/api/chat.py with JWT validation, conversation creation/loading, Cohere integration, tool execution loop (max 5 iterations)

### Frontend Tasks

- [X] T014 [P] [US1] Create ChatbotTrigger component in frontend/components/chatbot/ChatbotTrigger.tsx (floating button, emerald accent, 56x56px, pulse animation)
- [X] T015 [P] [US1] Create ChatInput component in frontend/components/chatbot/ChatInput.tsx (text field, send button with paper plane SVG, disabled state)
- [X] T016 [P] [US1] Create MessageBubble component in frontend/components/chatbot/MessageBubble.tsx (role-based styling: user=right/indigo, assistant=left/slate, timestamp)
- [X] T017 [P] [US1] Create MessageList component in frontend/components/chatbot/MessageList.tsx (scrollable area, auto-scroll to bottom, render MessageBubble array)
- [X] T018 [US1] Create ChatPanel component in frontend/components/chatbot/ChatPanel.tsx (slide-in animation, glassmorphic design, 400px×600px desktop, theme-aware, integrate MessageList + ChatInput)
- [X] T019 [US1] Create useChat hook in frontend/hooks/useChat.ts (manage state: messages, isOpen, isLoading, conversationId; sendMessage function with API call)
- [X] T020 [US1] Create chat API client in frontend/lib/api/chat.ts (POST to /api/{user_id}/chat with JWT header, handle response/errors)
- [X] T021 [US1] Update frontend/app/(authenticated)/dashboard/page.tsx to import and render ChatbotTrigger

## Phase 4: User Story 2 - Listing and Filtering Tasks (P1) (2 tasks)

**Story Goal**: Users view tasks with natural language queries and filters

**Independent Test**: Create sample tasks → ask "Show me my pending tasks" → verify filtered list displayed

- [X] T022 [P] [US2] Implement list_tasks tool in backend/app/tools/list_tasks.py (validate user_id, query with filters: status, priority, limit=50, return {success, tasks, count, error})
- [X] T023 [US2] Update Cohere system prompt in backend/app/services/cohere_client.py to include list_tasks tool schema and examples

## Phase 5: User Story 3 - Task Completion (P1) (2 tasks)

**Story Goal**: Users mark tasks complete/incomplete via natural language

**Independent Test**: Create test task → say "Mark task 5 as done" → verify status changes and confirmation shown

- [X] T024 [P] [US3] Implement complete_task tool in backend/app/tools/complete_task.py (validate user_id, update task.completed, return {success, task, error})
- [X] T025 [US3] Update Cohere system prompt to include complete_task tool schema

## Phase 6: User Story 9 - Beautiful Chat UI (P1) (3 tasks)

**Story Goal**: Premium, responsive chat UI integrated with existing design

**Independent Test**: Open on desktop + mobile → verify glassmorphic design, smooth animations, theme adaptation, responsiveness 320px-1920px

- [X] T026 [P] [US9] Add TypingIndicator component in frontend/components/chatbot/TypingIndicator.tsx (animated dots, show while isLoading)
- [X] T027 [US9] Update ChatPanel component with responsive styles (full-width on mobile <768px, proper z-index, backdrop blur)
- [X] T028 [US9] Add spring animation to ChatPanel slide-in using Tailwind transitions (duration-300, ease-in-out)

## Phase 7: User Story 4 - Task Updates (P2) (2 tasks)

**Story Goal**: Users update task properties via natural language

**Independent Test**: Create task → say "Change priority of task 5 to high" → verify update persisted

- [X] T029 [P] [US4] Implement update_task tool in backend/app/tools/update_task.py (validate user_id + ownership, update title/description/priority/completed, return {success, task, error})
- [X] T030 [US4] Update Cohere system prompt to include update_task tool schema

## Phase 8: User Story 5 - Task Deletion (P2) (2 tasks)

**Story Goal**: Users delete tasks with confirmation

**Independent Test**: Create task → say "Delete task 5" → verify task removed and confirmation shown

- [X] T031 [P] [US5] Implement delete_task tool in backend/app/tools/delete_task.py (validate user_id + ownership, delete task, return {success, message, error})
- [X] T032 [US5] Update Cohere system prompt to include delete_task tool schema

## Phase 9: User Story 6 - User Identity Query (P3) (2 tasks)

**Story Goal**: Users query their login information

**Independent Test**: Ask "Who am I?" → verify email address returned

- [X] T033 [P] [US6] Implement get_current_user tool in backend/app/tools/get_current_user.py (query user by user_id, return {success, user: {id, email}, error})
- [X] T034 [US6] Update Cohere system prompt to include get_current_user tool schema

## Phase 10: User Story 7 - Multi-Step Queries (P2) (3 tasks)

**Story Goal**: Handle complex queries requiring multiple tool executions

**Independent Test**: Say "Add task 'Weekly meeting' and list my pending tasks" → verify both operations execute

- [X] T035 [US7] Update tool_executor.py to implement loop execution (parse tool call → execute → feed result back to Cohere → repeat until no tool call, max 5 iterations)
- [X] T036 [US7] Add multi-step handling in chat endpoint (accumulate tool results, send combined context back to Cohere)
- [X] T037 [US7] Update Cohere system prompt with multi-step instructions and examples

## Phase 11: User Story 8 - Conversation Persistence (P2) (4 tasks)

**Story Goal**: Conversation history persists across sessions

**Independent Test**: Have conversation → refresh page → verify messages still visible

- [X] T038 [US8] Update chat endpoint to load last 10 messages from conversation_id before sending to Cohere
- [X] T039 [US8] Update chat endpoint to persist user message and assistant response after each interaction
- [X] T040 [P] [US8] Update frontend useChat hook to load conversation history on mount (fetch last 50 messages)
- [X] T041 [US8] Update ChatPanel to display conversation history from state on open

## Phase 12: Error Handling & Security (6 tasks)

**Goal**: Friendly error messages and security enforcement

- [X] T042 [P] Add rate limiting in backend/app/middleware/rate_limit.py (10 msg/min per user, return 429 with Retry-After)
- [X] T043 [P] Add input validation in chat endpoint (max 1000 chars, sanitize for SQL/XSS)
- [X] T044 [P] Implement error response formatter in backend/app/services/error_formatter.py (convert exceptions to friendly messages with ✓/⚠ symbols)
- [X] T045 Update all 6 tools to use error_formatter for consistent error responses
- [X] T046 [P] Add error boundary in frontend ChatPanel component (catch errors, show "⚠ Something went wrong. Please try again.")
- [X] T047 Update frontend chat API client to handle 401/403/429 errors with appropriate user messages

## Phase 13: Polish & Documentation (5 tasks)

**Goal**: Production-ready polish and documentation

- [X] T048 [P] Update README.md with Cohere setup section (API key, environment variables, chatbot usage examples)
- [X] T049 [P] Add AI Magic Highlights section to README.md (natural language capabilities, tool chaining, intelligent responses)
- [X] T050 [P] Create IMPLEMENTATION_LOG.md documenting phase completions and key decisions
- [X] T051 [P] Add JSDoc comments to all frontend components and hooks
- [X] T052 [P] Add Python docstrings to all backend tools, services, and endpoints

## Dependencies & Execution Order

### Story Dependency Graph

```
Phase 1 (Setup) → Phase 2 (Database)
                    ↓
Phase 3 (US1: Task Creation) [MVP - P1]
    ↓
├─ Phase 4 (US2: List Tasks) [P1]
├─ Phase 5 (US3: Complete Tasks) [P1]
├─ Phase 6 (US9: Beautiful UI) [P1]
├─ Phase 7 (US4: Update Tasks) [P2]
├─ Phase 8 (US5: Delete Tasks) [P2]
├─ Phase 9 (US6: User Identity) [P3]
├─ Phase 10 (US7: Multi-Step) [P2] (requires US1-US5 tools)
└─ Phase 11 (US8: Persistence) [P2]
    ↓
Phase 12 (Error Handling & Security)
    ↓
Phase 13 (Polish & Documentation)
```

### Blocking Dependencies

- **T007-T009** (Database) must complete before any backend tool development
- **T010-T013** (US1 backend) must complete before frontend integration
- **T014-T021** (US1 frontend) must complete before other UI features
- **T035** (Loop execution) requires all P1 tools (T010, T022, T024) complete
- **T038-T041** (Persistence) requires database models and chat endpoint complete

### Parallel Opportunities (28 tasks marked [P])

**Fully Parallel** (can execute simultaneously):
- T003-T006 (Setup directories)
- T007-T008 (Database models)
- T010, T011, T014-T017 (US1 backend + frontend components)
- T022, T024, T026-T027 (P1 tools + UI polish)
- T029, T031, T033 (P2/P3 tools)
- T040 (Frontend persistence)
- T042-T044, T046, T048-T052 (Security + docs)

## Testing Checklist

**Manual Test Scenarios**:

1. **Basic Flow (US1)**:
   - Login → Click chatbot button → Type "Add task to buy groceries" → Verify task created and confirmation shown

2. **Filtering (US2)**:
   - Create 5 tasks (3 pending, 2 complete) → Ask "Show pending tasks" → Verify 3 shown

3. **Completion (US3)**:
   - Create task → Ask "Mark task X as done" → Verify status updated

4. **Multi-Step (US7)**:
   - Ask "Add task 'Meeting' and list my tasks" → Verify both execute

5. **Persistence (US8)**:
   - Have conversation → Refresh page → Verify history loads

6. **Error Handling**:
   - Ask to delete non-existent task → Verify friendly error message
   - Send 11 messages quickly → Verify rate limit triggers

7. **Responsive UI (US9)**:
   - Test on 320px, 768px, 1920px widths → Verify proper layout

8. **Security**:
   - Login as User A → Create task → Login as User B → Attempt to access User A's task → Verify 403 error

## Success Criteria

Implementation complete when:
- ✅ All 52 tasks checked off
- ✅ 6 MCP tools operational with user isolation
- ✅ Chat endpoint responds <3s (test with 50 requests)
- ✅ Multi-step query works end-to-end
- ✅ UI responsive 320px-1920px
- ✅ Conversation persists across refresh
- ✅ Rate limiting enforces 10 msg/min
- ✅ Friendly error messages with ✓/⚠
- ✅ JWT validation rejects invalid tokens
- ✅ Demo-ready for hackathon judges

## MVP Recommendation

**MVP = Phase 3 (User Story 1)**: Basic task creation via chat
- Delivers core chatbot value
- 21 tasks (T001-T021)
- Estimated: 12-15 hours
- Includes: Database, 1 tool, Cohere service, tool executor, chat endpoint, complete chat UI
- Independently testable and demo-ready

**Full Feature = All Phases**: Complete AI assistant
- All 6 tools, multi-step, persistence, error handling, polish
- 52 tasks
- Estimated: 24-36 hours
- Flagship-quality production-ready chatbot

---

**Next Steps**:
1. Review task breakdown and dependencies
2. Assign specialized agents to parallel phases
3. Execute MVP (Phase 3) first for early validation
4. Incrementally add P1, P2, P3 stories
5. Polish and document for demo
