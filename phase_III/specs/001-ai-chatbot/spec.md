# Feature Specification: AI Todo Chatbot Integration

**Feature Branch**: `001-ai-chatbot`
**Created**: 2026-02-06
**Status**: Draft
**Version**: 1.0
**Input**: User description: "AI Todo Chatbot Integration for The Evolution of Todo - Phase III: Full-Stack Web Application"

## Overview

This specification defines the integration of an intelligent, natural-language AI chatbot into the Evolution of Todo application. The chatbot enables users to manage their tasks conversationally using Cohere API for natural language understanding and tool execution. The implementation extends the existing Next.js frontend and FastAPI backend with a beautifully designed chat interface and stateless conversation architecture.

**Target Audience**: Hackathon judges, developers building intelligent productivity tools, and AI agents implementing via Claude Code.

**Core Value Proposition**: Transform task management from form-based interactions to natural, conversational exchanges while maintaining security, user isolation, and flagship-quality user experience.

## User Scenarios & Testing

### User Story 1 - Basic Task Creation via Chat (Priority: P1)

Users can create new tasks by typing natural language commands into the chatbot without navigating forms or filling fields.

**Why this priority**: This is the most fundamental interaction pattern that demonstrates the chatbot's core value. It must work flawlessly as the foundation for all other features.

**Independent Test**: Can be fully tested by opening the chatbot, typing "Add a task to buy groceries", and verifying the task appears in the task list. Delivers immediate value by simplifying task creation.

**Acceptance Scenarios**:

1. **Given** a logged-in user opens the chatbot, **When** they type "Add a task to buy groceries", **Then** the system creates a new task with title "buy groceries" and responds with "✓ Task created: 'buy groceries' (ID: 42)"
2. **Given** a logged-in user, **When** they type "Add task: Complete project report with high priority", **Then** the system creates a task with title "Complete project report", priority "high", and confirms creation
3. **Given** a logged-in user, **When** they type "Create a task called 'Meeting' with description 'Discuss Q1 goals'", **Then** the system creates a task with both title and description and confirms
4. **Given** a user sends a vague command like "Add task", **When** the system receives insufficient information, **Then** it responds "I need more details. What task would you like to add?"

---

### User Story 2 - Listing and Filtering Tasks Conversationally (Priority: P1)

Users can view their tasks using natural language queries with optional filters for status and priority.

**Why this priority**: Essential for users to understand their current workload. Works independently and complements task creation.

**Independent Test**: Can be tested by creating sample tasks, then asking "Show me my pending tasks" or "List all high-priority tasks" and verifying correct filtering.

**Acceptance Scenarios**:

1. **Given** a user has 5 tasks (3 pending, 2 completed), **When** they ask "Show me my tasks", **Then** the chatbot displays all 5 tasks with titles, IDs, and completion status
2. **Given** a user has multiple tasks, **When** they ask "List my pending tasks", **Then** only incomplete tasks are shown
3. **Given** a user has tasks with different priorities, **When** they ask "Show high priority tasks", **Then** only tasks marked as high priority are displayed
4. **Given** a user has no tasks, **When** they ask "Show my tasks", **Then** the chatbot responds "You don't have any tasks yet. Would you like to create one?"

---

### User Story 3 - Task Completion via Natural Language (Priority: P1)

Users can mark tasks as complete or incomplete using conversational commands.

**Why this priority**: Core task management functionality that delivers immediate satisfaction and closure. Essential for the full task lifecycle.

**Independent Test**: Create a test task, mark it complete via chat ("Mark task 5 as done"), and verify status changes in both chat response and task list.

**Acceptance Scenarios**:

1. **Given** a user has a pending task with ID 5, **When** they say "Mark task 5 as done", **Then** the system updates the task to completed and responds "✓ Task 5 marked as complete!"
2. **Given** a user has a completed task, **When** they say "Mark task 3 as incomplete", **Then** the task status changes to pending
3. **Given** a user says "Complete the groceries task", **When** the system finds a task with "groceries" in the title, **Then** it marks that task complete
4. **Given** a user refers to a non-existent task ID, **When** they say "Mark task 999 as done", **Then** the system responds "⚠ I couldn't find task 999. Please check the task ID."

---

### User Story 4 - Task Updates and Modifications (Priority: P2)

Users can update task properties (title, description, priority) using natural language.

**Why this priority**: Important for maintaining accurate task information but not critical for initial MVP. Can be implemented after basic CRUD operations.

**Independent Test**: Create a task, then update it via chat ("Change the priority of task 5 to high"), and verify the update persists.

**Acceptance Scenarios**:

1. **Given** a task exists with ID 5, **When** user says "Change the priority of task 5 to high", **Then** the task priority updates and system confirms
2. **Given** a task exists, **When** user says "Rename task 3 to 'Updated meeting notes'", **Then** the task title changes
3. **Given** a task exists, **When** user says "Update task 7 description to 'Call client by Friday'", **Then** the description field updates
4. **Given** a user provides an invalid priority like "super urgent", **When** system receives this, **Then** it responds "Priority must be low, medium, or high. Please try again."

---

### User Story 5 - Task Deletion with Confirmation (Priority: P2)

Users can delete tasks using natural language commands.

**Why this priority**: Necessary for complete task lifecycle management but less frequently used than creation/completion. Requires careful UX to prevent accidental deletions.

**Independent Test**: Create a test task, delete it via chat ("Delete task 5"), and verify it no longer appears in the task list.

**Acceptance Scenarios**:

1. **Given** a user has a task with ID 5, **When** they say "Delete task 5", **Then** the system removes the task and responds "✓ Task 5 deleted successfully"
2. **Given** a user says "Delete the meeting task", **When** a task with "meeting" in the title exists, **Then** the system deletes it after confirmation
3. **Given** a user tries to delete a non-existent task, **When** they say "Delete task 999", **Then** system responds "⚠ I couldn't find task 999"
4. **Given** a user owns multiple tasks, **When** they attempt to delete a task owned by another user (via incorrect ID), **Then** system responds "⚠ You can only delete your own tasks"

---

### User Story 6 - User Identity Query (Priority: P3)

Users can ask the chatbot for their current login information.

**Why this priority**: Nice-to-have feature that helps users confirm their session but not essential for core task management.

**Independent Test**: Log in as a specific user, ask "Who am I?", and verify the chatbot returns the correct email address.

**Acceptance Scenarios**:

1. **Given** a logged-in user with email "user@example.com", **When** they ask "Who am I?", **Then** the chatbot responds "You're logged in as user@example.com"
2. **Given** a logged-in user, **When** they ask "What's my email?", **Then** the system interprets this as identity query and returns their email
3. **Given** a logged-in user, **When** they ask variations like "My account info" or "Show my profile", **Then** the system provides user email and user ID

---

### User Story 7 - Multi-Step Complex Queries (Priority: P2)

Users can issue commands that require multiple tool executions in a single natural language request.

**Why this priority**: Demonstrates advanced AI capabilities and significantly improves user experience, but depends on basic operations working first.

**Independent Test**: Send a command like "Add task 'Weekly meeting' and list my pending tasks", verify both actions execute correctly.

**Acceptance Scenarios**:

1. **Given** a logged-in user, **When** they say "Add task 'Weekly meeting' and list my pending tasks", **Then** the system creates the task and displays the updated pending list
2. **Given** a user has tasks, **When** they say "Complete task 5 and show me what's left", **Then** the system marks task 5 complete and lists remaining pending tasks
3. **Given** a user, **When** they say "Create 'Review docs' task with high priority and tell me my high-priority tasks", **Then** both operations execute sequentially

---

### User Story 8 - Conversation Persistence and Context (Priority: P2)

Users can see their conversation history with the chatbot persisted across sessions.

**Why this priority**: Enhances UX by providing context and allowing users to reference previous interactions, but not critical for core functionality.

**Independent Test**: Have a conversation with the chatbot, log out and log back in, reopen the chatbot, and verify previous messages are still visible.

**Acceptance Scenarios**:

1. **Given** a user has an active conversation, **When** they refresh the page, **Then** previous messages remain visible in the chat panel
2. **Given** a user closes the chat panel mid-conversation, **When** they reopen it, **Then** the conversation history is preserved
3. **Given** a user logs out and logs back in, **When** they open the chatbot, **Then** they see their previous conversation history (up to last 50 messages)

---

### User Story 9 - Beautiful Chatbot UI Integration (Priority: P1)

Users experience a visually stunning, responsive chat interface that integrates seamlessly with the existing application design.

**Why this priority**: First impressions matter for hackathon judges. The UI must be production-ready and flagship-quality from day one.

**Independent Test**: Open the application on desktop and mobile, click the chatbot trigger button, and verify the chat panel opens smoothly with premium design elements.

**Acceptance Scenarios**:

1. **Given** a user visits the application, **When** they see the chatbot button (bottom-right, emerald accent, subtle pulse), **Then** the button is clearly visible and accessible
2. **Given** a user clicks the chatbot button, **When** the chat panel opens, **Then** it slides in smoothly with glassmorphic design, dark/light theme awareness
3. **Given** messages are exchanged, **When** displayed in the chat panel, **Then** user messages appear on the right (indigo bubbles) and assistant messages on the left (slate bubbles) with timestamps
4. **Given** a long conversation exists, **When** new messages arrive, **Then** the chat auto-scrolls to the bottom
5. **Given** the chatbot is processing a request, **When** waiting for response, **Then** a typing indicator with animated dots appears
6. **Given** a user on mobile, **When** they open the chat panel, **Then** it remains responsive and usable with proper touch interactions

---

### Edge Cases

- **What happens when user sends extremely long messages (>1000 characters)?**
  - System truncates message after 1000 characters and prompts user to be more concise

- **How does system handle rate limiting (e.g., 20 messages/minute)?**
  - After exceeding rate limit, system responds "You're sending messages too quickly. Please wait a moment." and temporarily disables input

- **What if Cohere API is unavailable or returns errors?**
  - System displays "⚠ I'm having trouble connecting right now. Please try again in a moment." and logs error for debugging

- **How does system handle ambiguous task references (e.g., "Delete the meeting task" when multiple tasks contain "meeting")?**
  - System lists matching tasks with IDs and asks "I found multiple tasks with 'meeting'. Which one? (Task 5, Task 8, Task 12)"

- **What if user tries to perform operations on tasks they don't own?**
  - System enforces user isolation and responds "⚠ You can only modify your own tasks"

- **How does system handle network interruptions mid-conversation?**
  - Frontend detects connection loss, shows "Connection lost. Retrying..." banner, and automatically reconnects when available

- **What if user sends messages in a different language?**
  - System responds in English (assumption: English-only for MVP) with "I currently only support English. Please try your request in English."

- **How does system handle concurrent conversations (multiple tabs)?**
  - Each tab maintains its own conversation context; messages persist to database and sync across tabs on next load

- **What if database operations fail during tool execution?**
  - System catches exceptions, rolls back partial changes, and responds "⚠ Something went wrong. Please try again." while logging detailed error

- **How does system validate malicious or injection attempts in user input?**
  - Backend sanitizes all inputs before processing, validates against expected patterns, and rejects suspicious payloads

## Requirements

### Functional Requirements

**Natural Language Processing & Intent Detection**

- **FR-001**: System MUST process user messages through Cohere API (command-r-plus model) to interpret intent and extract entities
- **FR-002**: System MUST support natural language variations for all core operations (add, list, update, delete, complete tasks, user identity queries)
- **FR-003**: System MUST parse Cohere responses to identify tool invocation requests in JSON format: `{"tool": "tool_name", "params": {...}}`
- **FR-004**: System MUST handle multi-step queries that require chaining multiple tool executions (e.g., "Add task and list pending")

**MCP-Style Tool Execution**

- **FR-005**: System MUST provide 6 MCP-style tools accessible to the AI agent:
  - `add_task(title, description?, priority?, user_id)` - Create new task
  - `delete_task(task_id, user_id)` - Remove task
  - `update_task(task_id, user_id, title?, description?, priority?, completed?)` - Modify task
  - `complete_task(task_id, user_id, completed)` - Toggle completion status
  - `list_tasks(user_id, status?, priority?, limit?)` - Retrieve tasks with filters
  - `get_current_user(user_id)` - Return user email and ID

- **FR-006**: Each tool MUST validate `user_id` parameter against JWT claims to enforce user isolation
- **FR-007**: Each tool MUST return consistent JSON response with `success` boolean and data or error message
- **FR-008**: System MUST execute tools asynchronously using Python async/await patterns

**Database Persistence**

- **FR-009**: System MUST persist conversations in database with fields: `id`, `user_id`, `created_at`, `updated_at`
- **FR-010**: System MUST persist messages in database with fields: `id`, `conversation_id`, `role` ("user"/"assistant"), `content`, `tool_calls` (optional JSON array), `created_at`
- **FR-011**: System MUST maintain foreign key relationship between conversations and messages with cascade delete
- **FR-012**: System MUST index `user_id` in conversations table and `conversation_id` in messages table for performance

**Backend Chat Endpoint**

- **FR-013**: System MUST expose stateless endpoint `POST /api/{user_id}/chat`
- **FR-014**: Endpoint MUST accept request body: `{"message": "string", "conversation_id": "string (optional)"}`
- **FR-015**: Endpoint MUST return response: `{"conversation_id": "string", "response": "string", "tool_calls": ["array"], "timestamp": "ISO 8601"}`
- **FR-016**: Endpoint MUST validate JWT token and extract `user_id` from claims via middleware
- **FR-017**: Endpoint MUST verify `user_id` in URL path matches `user_id` from JWT (403 Forbidden if mismatch)
- **FR-018**: If `conversation_id` not provided, endpoint MUST create new conversation and return its ID
- **FR-019**: Endpoint MUST retrieve conversation history (last 10 messages) from database before sending to Cohere API
- **FR-020**: Endpoint MUST persist both user message and assistant response to database after successful interaction

**Frontend Chat UI**

- **FR-021**: System MUST display floating chatbot trigger button (bottom-right, emerald accent, 56x56px, subtle pulse animation)
- **FR-022**: Clicking trigger button MUST open/close slide-in chat panel (400px width on desktop, full-width on mobile)
- **FR-023**: Chat panel MUST display glassmorphic design with backdrop blur, rounded corners, and shadow
- **FR-024**: Chat panel MUST adapt to current theme (dark/light mode) using existing application theme context
- **FR-025**: User messages MUST appear on right side with indigo background, assistant messages on left with slate background
- **FR-026**: Each message bubble MUST display timestamp in small text below content
- **FR-027**: Chat panel MUST include scrollable message history area that auto-scrolls to bottom on new messages
- **FR-028**: Chat panel MUST include input bar at bottom with text field and send button (SVG paper plane icon)
- **FR-029**: System MUST display typing indicator (animated dots) while waiting for assistant response
- **FR-030**: System MUST disable input field and send button while processing request
- **FR-031**: Chat panel MUST be responsive and usable on mobile devices (320px minimum width)

**Authentication & Security**

- **FR-032**: All chat requests MUST include valid JWT token in Authorization header or cookie
- **FR-033**: System MUST reject requests with expired or invalid JWT tokens (401 Unauthorized)
- **FR-034**: System MUST enforce user isolation: users can only access their own conversations and tasks
- **FR-035**: System MUST validate all user inputs against injection attacks (SQL, XSS, command injection)
- **FR-036**: System MUST store Cohere API key in environment variable `COHERE_API_KEY`, never in code
- **FR-037**: System MUST log all tool executions with user_id, tool name, and parameters for auditing

**Error Handling & User Experience**

- **FR-038**: System MUST provide friendly error messages for common failures:
  - Task not found: "⚠ I couldn't find task [ID]. Please check the task ID."
  - Insufficient information: "I need more details. [Specific question]"
  - Permission denied: "⚠ You can only modify your own tasks"
  - API failure: "⚠ I'm having trouble connecting right now. Please try again."

- **FR-039**: System MUST include confirmation symbols in responses: ✓ for success, ⚠ for errors/warnings
- **FR-040**: System MUST ask clarifying questions when user intent is ambiguous
- **FR-041**: System MUST handle graceful degradation if Cohere API is unavailable (show fallback message)
- **FR-042**: System MUST enforce rate limiting: 10 messages per minute per user (return 429 Too Many Requests)

**Cohere API Integration**

- **FR-043**: System MUST use Cohere's `co.chat()` method with model "command-r-plus" and temperature 0.3
- **FR-044**: System MUST construct system prompt instructing Cohere to:
  - Think step-by-step
  - Identify user intent
  - Output tool calls in JSON format: `{"tool": "tool_name", "params": {...}}`
  - Generate friendly natural language responses

- **FR-045**: System MUST include conversation history in Cohere API calls formatted as:
  ```
  [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
  ```

- **FR-046**: System MUST parse Cohere response text to extract JSON tool call blocks using regex pattern
- **FR-047**: If tool call found, system MUST execute tool, then send result back to Cohere for final response generation
- **FR-048**: System MUST handle Cohere API errors (timeouts, rate limits, invalid responses) with appropriate fallbacks

### Key Entities

- **Conversation**: Represents a chat session between user and chatbot
  - Unique identifier (UUID)
  - Owner (user_id foreign key)
  - Creation and update timestamps
  - One-to-many relationship with Messages

- **Message**: Represents a single message in a conversation
  - Unique identifier (UUID)
  - Parent conversation (conversation_id foreign key)
  - Role (user or assistant)
  - Content (text of the message)
  - Optional tool_calls metadata (JSON array of tool names invoked)
  - Creation timestamp
  - Belongs to exactly one Conversation

- **User**: Existing entity representing authenticated users (no changes needed)
  - Used for JWT authentication and user_id validation

- **Task**: Existing entity representing todo items (no schema changes needed)
  - All task operations accessed through MCP-style tools

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can complete all six core task operations (add, list, update, delete, complete, get user info) via natural language in under 30 seconds each
- **SC-002**: Chatbot responds to simple queries (single-tool operations) in under 3 seconds from message send to response display
- **SC-003**: Multi-step queries (requiring 2+ tool calls) complete in under 5 seconds
- **SC-004**: 95% of natural language variations for core operations are correctly interpreted on first attempt (measured by tool invocation accuracy)
- **SC-005**: System handles 100 concurrent users sending chat messages without performance degradation (response time stays under 3 seconds)
- **SC-006**: Conversation history persists correctly across browser sessions for 100% of users
- **SC-007**: Chat UI renders correctly and remains fully functional on devices from 320px to 1920px width
- **SC-008**: Zero cross-user data access occurs (100% user isolation maintained in tool execution and conversation retrieval)
- **SC-009**: Chatbot trigger button and chat panel maintain visual harmony with existing application design (validated through design review)
- **SC-010**: Error handling provides actionable guidance to users in 100% of failure scenarios (no generic "something went wrong" messages without context)
- **SC-011**: Users can discover and understand chatbot capabilities within first 3 interactions (measured by successful task completion without external help)
- **SC-012**: Chat interface achieves 90% positive feedback rating from hackathon judges and demo users for visual design and user experience

## Assumptions

1. **Language Support**: English-only for MVP; internationalization can be added in future phases
2. **Cohere Model**: Using `command-r-plus` model for optimal balance of speed and accuracy
3. **Conversation Limit**: Storing last 10 messages per conversation for Cohere context window management
4. **Authentication**: JWT authentication already implemented and working in Phase II; no changes needed
5. **Database**: PostgreSQL (Neon) already provisioned with SQLModel ORM; can add new tables without migration issues
6. **Theme Support**: Application already has dark/light theme implemented; chat UI will integrate with existing theme context
7. **Mobile Support**: Existing application is responsive; chat UI will follow same responsive patterns
8. **Rate Limiting**: 10 messages/minute per user is reasonable default to prevent abuse while allowing normal usage
9. **Error Recovery**: Users can retry failed operations by resending message; no automatic retry needed
10. **Real-time Streaming**: Not implementing message streaming in MVP (responses appear complete after Cohere returns)
11. **Message History**: Loading last 50 messages on chat open provides sufficient context without performance impact
12. **Tool Timeout**: Individual tool operations complete within 5 seconds; longer operations should be async with status updates

## Out of Scope

The following features are explicitly excluded from this specification:

- Voice input/output for chatbot interactions
- File attachments or image uploads in chat
- Real-time streaming of assistant responses (word-by-word display)
- Custom Cohere model fine-tuning
- Multi-language support beyond English
- Integration with external calendar/reminder systems
- Task sharing or collaboration features via chat
- Advanced analytics on chatbot usage patterns
- Custom user-defined tools or commands
- Chatbot personality customization
- Conversation export/download functionality
- Search within conversation history
- Pinning or starring important conversations
- Chatbot availability on mobile native apps (web only)

## Dependencies

- **Cohere API**: Requires valid API key and internet connectivity
- **Existing Authentication System**: JWT-based auth from Phase II must be operational
- **Database**: Neon PostgreSQL with SQLModel ORM
- **Frontend Framework**: Next.js 16+ (App Router), React 18+, TypeScript
- **Backend Framework**: FastAPI, Python 3.11+
- **UI Components**: Shadcn/ui or compatible component library for consistent design
- **Theme System**: Existing dark/light theme context and utilities

## Non-Functional Requirements

- **Performance**: Chat endpoint responds within 3 seconds for 95th percentile requests
- **Scalability**: Stateless architecture supports horizontal scaling to handle increased load
- **Reliability**: System maintains 99% uptime during demo/judging period
- **Security**: All inputs sanitized, JWT validation mandatory, no API keys exposed
- **Maintainability**: Code follows project standards (TypeScript/Python best practices, PEP 8, ESLint rules)
- **Accessibility**: Chat UI supports keyboard navigation and screen reader compatibility (WCAG 2.1 Level A minimum)
- **Browser Support**: Works on latest versions of Chrome, Firefox, Safari, Edge
- **Mobile Performance**: Chat UI loads and operates smoothly on 4G connections

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
| --- | --- | --- | --- |
| Cohere API quota exceeded | High | Medium | Implement rate limiting; monitor usage; have fallback message |
| Cohere API interprets intent incorrectly | Medium | Medium | Use temperature 0.3 for consistency; extensive prompt engineering; validate tool calls |
| Chat UI performance degrades with long conversations | Medium | Low | Limit displayed messages to last 50; implement pagination or infinite scroll |
| User confusion about chatbot capabilities | Medium | Medium | Add welcome message explaining capabilities; provide example commands |
| Security breach via prompt injection | High | Low | Sanitize inputs; validate tool parameters; enforce strict user isolation |
| Mobile UI breaks on small screens | Medium | Low | Test on multiple devices; use responsive design patterns; min-width 320px |

## Open Questions

None - all critical decisions have been made with reasonable defaults documented in Assumptions section.

## Wireframes & Interaction Flows

### Chat Trigger Button (Bottom-Right)

```
┌─────────────────────────────────────┐
│                                     │
│         Main Application            │
│              Content                │
│                                     │
│                                     │
│                            ┌────┐  │
│                            │ 💬 │  │ ← Floating button
│                            └────┘  │    (emerald, pulse)
└─────────────────────────────────────┘
```

### Chat Panel Open (Slide-in from Right)

```
┌──────────────────┬──────────────────┐
│                  │                  │
│   Main App       │  Chat Panel      │
│   Content        │  ┌────────────┐  │
│                  │  │  Chat Title│  │
│                  │  │    [X]     │  │
│                  │  ├────────────┤  │
│                  │  │ User: Hi   │  │ ← User bubble (right, indigo)
│                  │  │ 10:23      │  │
│                  │  │            │  │
│                  │  │Bot: Hello! │  │ ← Assistant bubble (left, slate)
│                  │  │  10:23     │  │
│                  │  │            │  │
│                  │  │ [Typing...] │  │ ← Typing indicator
│                  │  ├────────────┤  │
│                  │  │ [Input]  ✈️ │  │ ← Input + send button
│                  │  └────────────┘  │
└──────────────────┴──────────────────┘
```

### Conversation Flow - Add Task

```
User: "Add a task to buy groceries"
  ↓
[Backend receives message]
  ↓
[JWT validated, user_id extracted]
  ↓
[Message sent to Cohere API with system prompt]
  ↓
[Cohere returns: {"tool": "add_task", "params": {"title": "buy groceries", "user_id": "123"}}]
  ↓
[System parses tool call and executes add_task()]
  ↓
[Tool result: {"success": true, "task": {"id": "42", "title": "buy groceries"}}]
  ↓
[Result sent back to Cohere for response generation]
  ↓
[Cohere returns: "✓ Task created: 'buy groceries' (ID: 42)"]
  ↓
[Both messages persisted to database]
  ↓
Bot: "✓ Task created: 'buy groceries' (ID: 42)"
```

### Conversation Flow - Multi-Step Query

```
User: "Add task 'Weekly meeting' and list my pending tasks"
  ↓
[Backend processes with Cohere]
  ↓
[Cohere identifies two operations needed]
  ↓
[Tool call 1: add_task("Weekly meeting")]
  ↓
[Tool call 2: list_tasks(status="pending")]
  ↓
[Both tools execute sequentially]
  ↓
[Results combined and sent to Cohere]
  ↓
Bot: "✓ Task created: 'Weekly meeting'. Here are your pending tasks:
     1. Weekly meeting (ID: 42)
     2. Buy groceries (ID: 38)
     3. Review docs (ID: 35)"
```

### Mobile Responsive Layout

```
┌─────────────────────┐
│ ☰  App Header       │
├─────────────────────┤
│                     │
│                     │
│   Main Content      │
│                     │
│                     │
│                     │
│  ┌───────────────┐  │ ← Chat Panel (full-width)
│  │ Chat Title [X]│  │
│  ├───────────────┤  │
│  │ User: Hi      │  │
│  │ Bot: Hello!   │  │
│  ├───────────────┤  │
│  │ [Input]  ✈️   │  │
│  └───────────────┘  │
└─────────────────────┘
```

---

**Next Steps**:
1. Run `/sp.clarify` if any requirements need user input
2. Run `/sp.plan` to create technical architecture design
3. Run `/sp.tasks` to generate implementation tasks
