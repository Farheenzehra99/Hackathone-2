<!-- SYNC IMPACT REPORT
Version change: 2.0.0 → 3.0.0
Modified principles: Added VII. AI-First Natural Language Interface, Extended III. Agentic Development to include MCP tools
Added sections: Chatbot Functionality & Natural Language Handling, Database Extensions for Conversations, MCP Tools Specification, Cohere API Adaptation, ChatKit Frontend Integration
Removed sections: None (Phase II foundation preserved)
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# AI Todo Chatbot Integration for The Evolution of Todo - Phase III Constitution

## Project Overview

The Evolution of Todo - Phase III represents the culmination of a three-phase evolution: from Phase I's single-user console application to Phase II's secure multi-user web application, and now to Phase III's intelligent AI-powered chatbot interface. This phase integrates natural language processing capabilities through Cohere API, enabling users to manage tasks conversationally while maintaining all security, isolation, and architectural principles established in prior phases.

**Evolution Summary:**
- **Phase I**: Single-user in-memory console application with basic CRUD operations
- **Phase II**: Multi-user full-stack web app with JWT authentication, PostgreSQL persistence, and RESTful APIs
- **Phase III**: AI chatbot integration using Cohere API, MCP tools, and stateless conversation architecture

**Target Audience:**
- Hackathon judges evaluating cutting-edge agentic AI integrations
- Developers building intelligent productivity tools
- AI agents (Claude Code) implementing via Spec-Kit Plus

**Objective:** Deliver a production-ready, intelligent chatbot that handles complex natural language queries (e.g., "Add weekly meeting and list pending tasks") by chaining MCP tools, providing confirmations, handling errors gracefully, and maintaining multi-user security.

## Core Principles

### I. Spec-First Development
All development begins with comprehensive specifications before any implementation work. Features must be fully defined in spec documents with clear acceptance criteria, edge cases, and error handling requirements before implementation begins. This ensures predictable outcomes and enables agentic development workflows.

### II. Security by Design
Security considerations are integrated from the ground floor up. All user data must be properly isolated with mandatory user_id validation against JWT claims. Authentication and authorization are non-negotiable requirements for all endpoints. No data access occurs without proper security validation. This extends to chatbot conversations - all messages and tool invocations must enforce user isolation.

### III. Agentic Development Compliance
Implementation strictly follows agentic development principles using Claude Code agents and Spec-Kit Plus tools only. No manual coding is permitted. All changes must flow through constitution → specs → plan → tasks → implementation workflow with proper documentation at each stage. MCP (Model Context Protocol) tools are the primary mechanism for AI-driven task execution.

### IV. Multi-User Isolation
Every operation must enforce strict user isolation. Users can only access, modify, or delete their own data. Cross-user data access is prohibited. All API endpoints and MCP tools must validate user identity against data ownership using JWT claims and database constraints. Conversations are isolated per user.

### V. RESTful API Design
All backend endpoints follow RESTful principles with proper HTTP methods, status codes, and consistent error handling. APIs are designed to be predictable, discoverable, and maintainable with clear contracts between frontend and backend services. The chat endpoint follows stateless design patterns.

### VI. Full-Stack Integration
Frontend and backend components are developed as integrated parts of a cohesive system. API contracts are established early and maintained throughout development. Both client and server sides share consistent data models and error handling patterns. The chatbot frontend (ChatKit) integrates seamlessly with existing UI components.

### VII. AI-First Natural Language Interface
The chatbot provides an intelligent, conversational interface for all task management operations. Natural language queries are interpreted through Cohere API reasoning, mapped to appropriate MCP tools, and executed with proper validation. The system handles multi-step queries, provides confirmations, and gracefully manages errors. User experience feels intuitive, helpful, and production-ready.

## Core Requirements

The Phase III chatbot extends all six Phase II task management features with conversational natural language interface:

### Conversational Task Management Features
1. **Add Task via Natural Language**: "Add a task to buy groceries" → creates task with extracted details
2. **View Tasks Conversationally**: "Show me all my pending tasks" → lists tasks with formatting
3. **Update Task via NL**: "Change the priority of task 5 to high" → updates task
4. **Delete Task Conversationally**: "Delete the meeting task" → removes task after confirmation
5. **Mark Complete/Incomplete via NL**: "Mark task 3 as done" → toggles completion status
6. **User Identity Queries**: "Who am I?" → "Logged in as user@example.com"

### REST API Endpoint - Chat Interface

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| POST | `/api/{user_id}/chat` | Stateless chatbot endpoint - accepts user message, returns AI response with tool results | Yes (JWT) |

**Request Schema:**
```json
{
  "message": "string",
  "conversation_id": "string (optional, auto-created if null)"
}
```

**Response Schema:**
```json
{
  "response": "string (AI-generated response)",
  "conversation_id": "string",
  "tool_calls": ["array of tool names invoked"],
  "timestamp": "ISO 8601"
}
```

## Chatbot Functionality & Natural Language Handling

### Conversation Flow Architecture

1. **User Input → Intent Detection**
   - User sends natural language message via ChatKit frontend
   - Backend receives message at `/api/{user_id}/chat`
   - JWT middleware extracts and validates `user_id`

2. **AI Reasoning with Cohere API**
   - Message + conversation history sent to Cohere chat endpoint
   - Prompt instructs Cohere to reason step-by-step and output tool invocation JSON
   - Cohere returns reasoning + structured tool calls

3. **MCP Tool Execution**
   - Parse Cohere output to extract tool name and parameters
   - Invoke appropriate MCP tool (e.g., `add_task`, `list_tasks`)
   - Tools interact with database using validated `user_id`
   - Collect tool results

4. **Response Generation**
   - Send tool results back to Cohere for natural language response generation
   - Cohere generates friendly confirmation or error message
   - Persist user message + AI response in database

5. **Return to User**
   - Frontend displays AI response in chat interface
   - User can continue conversation or issue new commands

### Natural Language Examples

**Example 1: Simple Task Creation**
- User: "Add a task to buy groceries"
- Cohere reasoning: "User wants to create a task. Extract title: 'buy groceries'. Use add_task tool."
- Tool call: `add_task(title="buy groceries", user_id=<validated>)`
- Response: "✓ Task created: 'buy groceries' (ID: 42)"

**Example 2: Complex Multi-Step Query**
- User: "Add weekly meeting and list pending tasks"
- Cohere reasoning: "Two operations: 1) create task, 2) list tasks with status filter."
- Tool calls:
  1. `add_task(title="weekly meeting", user_id=<validated>)`
  2. `list_tasks(status="pending", user_id=<validated>)`
- Response: "✓ Task created: 'weekly meeting'. Here are your pending tasks: [list]"

**Example 3: User Identity Query**
- User: "Who am I?"
- Cohere reasoning: "User asking for identity. Use get_user_info tool."
- Tool call: `get_user_info(user_id=<validated>)`
- Response: "Logged in as user@example.com"

**Example 4: Error Handling**
- User: "Delete task 999"
- Tool call: `delete_task(task_id=999, user_id=<validated>)`
- Tool result: `{"error": "Task not found"}`
- Response: "⚠ I couldn't find task 999. Please check the task ID and try again."

### Confirmation & Error Handling Patterns

- **Success confirmations**: Use checkmarks (✓) and restate action
- **Errors**: Use warning symbols (⚠) and provide actionable guidance
- **Ambiguity**: Ask clarifying questions ("Did you mean task 5 or 15?")
- **Invalid operations**: Explain constraints ("You can only delete your own tasks")

## Authentication & Security

### JWT-Based User Isolation

1. **Frontend Authentication**:
   - Better Auth handles login/registration
   - JWT token issued with claims: `user_id`, `email`, `exp`
   - Token stored in httpOnly cookie or localStorage

2. **Chat Endpoint Security**:
   - JWT middleware validates token signature using `BETTER_AUTH_SECRET`
   - Extracts `user_id` from claims
   - Injects validated `user_id` into request context

3. **MCP Tool Security**:
   - All tools require `user_id` parameter
   - Tools validate ownership before any data access/modification
   - Database queries include `WHERE user_id = :user_id` filters

4. **Conversation Isolation**:
   - Each conversation belongs to exactly one user
   - Conversation messages filtered by `user_id` before sending to Cohere
   - No cross-user conversation access possible

### Security Constraints
- **Mandatory JWT**: All chat requests must include valid JWT
- **User ID Validation**: `user_id` in URL path must match JWT claim
- **Tool-Level Isolation**: Every MCP tool enforces user ownership checks
- **No Shared State**: Server maintains no session state; all context from database
- **API Key Protection**: `COHERE_API_KEY` stored in environment variables, never exposed

## Non-Functional Requirements

- **Code Quality**: TypeScript (frontend), Python PEP 8 (backend), comprehensive type hints
- **Async Operations**: All I/O operations (database, Cohere API) must be async/await
- **Response Latency**: Chat responses under 3 seconds for single-tool queries
- **Scalability**: Stateless design enables horizontal scaling
- **Error Resilience**: Graceful degradation if Cohere API unavailable (fallback messages)
- **Conversation Limits**: Archive conversations older than 30 days (future enhancement)
- **Rate Limiting**: Protect against abuse (e.g., 10 messages/minute per user)
- **Logging**: Comprehensive structured logging for debugging and auditing

## Technology Stack and Tools

### Phase III Extensions to Phase II Stack

**AI & Reasoning:**
- **Cohere API**: Multi-turn conversations with tool-calling via prompt engineering
- **API Key**: `COHERE_API_KEY=your_api_key_here`

**MCP (Model Context Protocol):**
- **Official MCP SDK**: Tool definition, registration, and invocation framework
- **Custom Tools**: Five task management tools (see MCP Tools Specification section)

**Frontend Additions:**
- **ChatKit**: Conversational UI component library (or custom React chat interface)
- **Real-time Updates**: Optional WebSocket for live message streaming (future)

**Backend Additions:**
- **MCP Server**: Exposes tools for AI agent consumption
- **Chat Endpoint**: `/api/{user_id}/chat` for stateless conversation handling
- **Cohere Client**: Python SDK for API interactions

**Existing Stack (Preserved):**
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS, Better Auth, Shadcn/ui
- **Backend**: FastAPI, Python 3.11+, SQLModel, Neon PostgreSQL
- **Auth**: JWT verification middleware with `BETTER_AUTH_SECRET`
- **Environment**: Docker Compose, dotenv

## Development Workflow

Phase III follows the established agentic development workflow with MCP tool integration:

1. **Constitution** (this document) → Defines Phase III governance and AI principles
2. **Specifications** → Detailed chatbot feature requirements and acceptance criteria
3. **Planning** → MCP tool architecture, Cohere API integration design, database schema updates
4. **Tasks** → Actionable implementation steps (backend MCP server, frontend ChatKit, database migrations)
5. **Agents/Skills** → Claude Code implementation using Spec-Kit Plus tools
6. **Implementation** → Automated code generation for tools, endpoints, UI components
7. **Testing** → Validate tool execution, conversation flow, security isolation
8. **Iteration** → Refine prompts, error handling, user experience

**Agentic Constraints:**
- No manual coding permitted
- All implementation via Claude Code agents and Spec-Kit Plus skills
- MCP tools must be defined in spec before implementation
- Cohere API interactions must follow documented patterns

**Environment Configuration:**
```bash
# Existing variables
BETTER_AUTH_SECRET=<shared-secret>
DATABASE_URL=postgresql://...

# Phase III additions
COHERE_API_KEY=your_api_key_here
```

## Monorepo Updates

### Extended Directory Structure

```
project-root/
├── .specify/                    # Spec-Kit Plus configuration
│   ├── memory/
│   │   └── constitution.md      # This file (v3.0)
│   ├── templates/
│   └── commands/
├── specs/
│   ├── features/
│   │   ├── authentication/
│   │   └── chatbot/             # NEW: Phase III chatbot specs
│   │       ├── spec.md
│   │       ├── plan.md
│   │       └── tasks.md
│   ├── api/
│   │   └── chat-endpoint.md     # NEW: Chat API specification
│   ├── database/
│   │   └── conversations-schema.md  # NEW: Conversation models
│   └── mcp/
│       └── tools-spec.md        # NEW: MCP tool definitions
├── frontend/
│   ├── app/
│   │   └── chat/                # NEW: Chat interface pages
│   │       └── page.tsx
│   ├── components/
│   │   └── chatkit/             # NEW: Chat UI components
│   │       ├── ChatContainer.tsx
│   │       ├── MessageList.tsx
│   │       └── ChatInput.tsx
│   └── lib/
│       └── chat-api.ts          # NEW: Chat API client
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── chat.py          # NEW: Chat endpoint
│   │   └── mcp/
│   │       ├── server.py        # NEW: MCP server initialization
│   │       └── tools/           # NEW: MCP tool implementations
│   │           ├── add_task.py
│   │           ├── list_tasks.py
│   │           ├── update_task.py
│   │           ├── delete_task.py
│   │           └── get_user_info.py
│   ├── models/
│   │   ├── conversation.py      # NEW: Conversation model
│   │   └── message.py           # NEW: Message model
│   ├── services/
│   │   └── cohere_client.py     # NEW: Cohere API wrapper
│   └── requirements.txt         # Add cohere, mcp packages
└── docker-compose.yml           # Update with Cohere env vars
```

## Database Extensions

### New Models for Conversations

**Conversation Model:**
```python
class Conversation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
```

**Message Model:**
```python
class Message(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: str = Field(...)  # "user" or "assistant"
    content: str = Field(...)
    tool_calls: Optional[str] = Field(default=None)  # JSON array of tool names
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

**Database Constraints:**
- `user_id` indexed for fast conversation lookups
- `conversation_id` indexed for message retrieval
- Foreign key cascades: deleting conversation deletes messages
- `role` enum constraint: only "user" or "assistant" allowed

**Migration Strategy:**
- Create tables via Alembic migration
- No data migration needed (net-new feature)
- Add indexes after table creation for performance

## MCP Tools Specification

### Tool 1: add_task

**Purpose:** Create a new task for the authenticated user

**Parameters:**
- `title` (string, required): Task title
- `description` (string, optional): Task description
- `priority` (string, optional): "low" | "medium" | "high"
- `user_id` (string, required): Validated from JWT

**Returns:**
```json
{
  "success": true,
  "task": {
    "id": "string",
    "title": "string",
    "description": "string",
    "priority": "string",
    "completed": false,
    "created_at": "ISO 8601"
  }
}
```

**Error Cases:**
- Invalid priority value → 400 Bad Request
- Missing title → 400 Bad Request
- Database error → 500 Internal Server Error

---

### Tool 2: list_tasks

**Purpose:** Retrieve tasks for the authenticated user with optional filters

**Parameters:**
- `user_id` (string, required): Validated from JWT
- `status` (string, optional): "pending" | "completed" | "all"
- `priority` (string, optional): "low" | "medium" | "high"
- `limit` (integer, optional): Max results (default 50)

**Returns:**
```json
{
  "success": true,
  "tasks": [
    {
      "id": "string",
      "title": "string",
      "priority": "string",
      "completed": boolean
    }
  ],
  "count": integer
}
```

**Error Cases:**
- Invalid filter values → 400 Bad Request
- Database error → 500 Internal Server Error

---

### Tool 3: update_task

**Purpose:** Update task properties for authenticated user's task

**Parameters:**
- `task_id` (string, required): Task to update
- `user_id` (string, required): Validated from JWT
- `title` (string, optional): New title
- `description` (string, optional): New description
- `priority` (string, optional): New priority
- `completed` (boolean, optional): New completion status

**Returns:**
```json
{
  "success": true,
  "task": {
    "id": "string",
    "title": "string",
    "description": "string",
    "priority": "string",
    "completed": boolean
  }
}
```

**Error Cases:**
- Task not found → 404 Not Found
- Task belongs to different user → 403 Forbidden
- Invalid parameters → 400 Bad Request

---

### Tool 4: delete_task

**Purpose:** Delete a task owned by authenticated user

**Parameters:**
- `task_id` (string, required): Task to delete
- `user_id` (string, required): Validated from JWT

**Returns:**
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Error Cases:**
- Task not found → 404 Not Found
- Task belongs to different user → 403 Forbidden
- Database error → 500 Internal Server Error

---

### Tool 5: get_user_info

**Purpose:** Retrieve authenticated user's information (email, name)

**Parameters:**
- `user_id` (string, required): Validated from JWT

**Returns:**
```json
{
  "success": true,
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  }
}
```

**Error Cases:**
- User not found → 404 Not Found (should never happen with valid JWT)
- Database error → 500 Internal Server Error

---

### Tool Implementation Contract

All tools MUST:
1. Accept `user_id` as required parameter
2. Validate user ownership before data access/modification
3. Return consistent JSON schema with `success` field
4. Use async database operations (SQLModel async session)
5. Log all invocations with user_id and parameters
6. Handle database exceptions gracefully

## Cohere API Adaptation

### OpenAI-Style Agent Behavior → Cohere Implementation

**Challenge:** Cohere API does not natively support OpenAI's function-calling format. We adapt by using prompt engineering to simulate agent reasoning and tool invocation.

### Adaptation Strategy

**1. System Prompt Design:**
```
You are a helpful task management assistant. Users can ask you to manage their tasks in natural language.

You have access to the following tools:
- add_task(title, description?, priority?, user_id)
- list_tasks(user_id, status?, priority?, limit?)
- update_task(task_id, user_id, title?, description?, priority?, completed?)
- delete_task(task_id, user_id)
- get_user_info(user_id)

When a user makes a request, follow these steps:
1. Understand the user's intent
2. Determine which tool(s) to invoke
3. Output tool calls in JSON format: {"tool": "tool_name", "params": {...}}
4. After tool execution, generate a friendly response

Always validate that you have user_id before invoking tools.
```

**2. Conversation History Format:**
```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Add a task to buy groceries"},
    {"role": "assistant", "content": "Tool call: {\"tool\": \"add_task\", \"params\": {\"title\": \"buy groceries\", \"user_id\": \"123\"}}"},
    {"role": "user", "content": "Tool result: {\"success\": true, \"task\": {...}}"},
    {"role": "assistant", "content": "✓ Task created: 'buy groceries'"}
]
```

**3. Cohere API Call:**
```python
import cohere

co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

response = co.chat(
    message=user_message,
    chat_history=conversation_history,
    model="command-r-plus",
    temperature=0.3
)

assistant_message = response.text
```

**4. Parse Tool Calls from Response:**
```python
import json
import re

def extract_tool_calls(text: str) -> List[dict]:
    """Extract JSON tool calls from Cohere response"""
    pattern = r'\{\"tool\":\s*\".*?\",\s*\"params\":\s*\{.*?\}\}'
    matches = re.findall(pattern, text)
    return [json.loads(match) for match in matches]
```

**5. Execute Tools & Generate Final Response:**
```python
# Extract and execute tool calls
tool_calls = extract_tool_calls(assistant_message)
tool_results = []

for tool_call in tool_calls:
    tool_name = tool_call["tool"]
    params = tool_call["params"]
    result = await execute_mcp_tool(tool_name, params)
    tool_results.append(result)

# Send tool results back to Cohere for final response
final_response = co.chat(
    message=f"Tool results: {json.dumps(tool_results)}",
    chat_history=conversation_history + [
        {"role": "assistant", "content": assistant_message}
    ],
    model="command-r-plus",
    temperature=0.3
)

return final_response.text
```

### Best Practices for Cohere Adaptation

- **Low Temperature**: Use `temperature=0.3` for consistent tool invocation format
- **Explicit Instructions**: System prompt must clearly define tool schemas and output format
- **Validation Layer**: Always validate parsed tool calls before execution
- **Fallback Handling**: If tool call parsing fails, ask user to rephrase
- **Context Window**: Limit conversation history to last 10 messages to avoid token limits
- **Error Messages**: Include error context in tool results sent back to Cohere

## Guiding Principles

### AI-First Design
The chatbot is the primary interface for task management in Phase III. UI and API design prioritize conversational interactions over traditional form-based CRUD operations.

### Stateless Architecture
The chat endpoint maintains no server-side session state. All context is retrieved from database (conversation history) and JWT claims (user identity). This enables horizontal scaling and simplifies deployment.

### Security First
Every tool invocation, database query, and API response enforces user isolation. JWT validation is mandatory. No shortcuts or temporary bypasses permitted.

### No Manual Code
All implementation via Claude Code agents using Spec-Kit Plus tools. This ensures consistency, auditability, and alignment with agentic development principles.

### Hackathon Transparency
Full process documentation including constitution, specs, plans, tasks, and prompt history records. Judges can trace every decision and implementation step.

### Production-Ready Quality
The chatbot must feel polished, intelligent, and reliable. Handle edge cases gracefully, provide helpful error messages, and maintain consistent UX across all interactions.

## Deliverables and Success Criteria

### Primary Deliverables

1. **Working AI Chatbot Interface**
   - ChatKit frontend component integrated with existing UI
   - Natural language input/output with typing indicators
   - Message history display with user/assistant differentiation

2. **Backend Chat Endpoint**
   - `/api/{user_id}/chat` stateless endpoint
   - JWT authentication and user_id validation
   - Cohere API integration for reasoning
   - MCP tool execution framework

3. **Five MCP Tools**
   - `add_task`, `list_tasks`, `update_task`, `delete_task`, `get_user_info`
   - Stateless database interactions
   - Comprehensive error handling
   - User isolation enforcement

4. **Database Schema Updates**
   - Conversation and Message models
   - Alembic migrations
   - Indexes for performance

5. **Documentation & Specs**
   - Complete Phase III specs (feature, API, database, MCP tools)
   - Implementation plan and tasks
   - Prompt history records (PHRs) for all development steps

### Success Criteria

**Functional Requirements:**
- ✅ Chatbot handles all five task operations via natural language
- ✅ Multi-step queries work correctly (e.g., "Add task and list pending")
- ✅ User identity queries return correct email
- ✅ Confirmations and error messages are friendly and actionable
- ✅ Conversation history persists across sessions

**Security Requirements:**
- ✅ All chat requests require valid JWT
- ✅ user_id in URL matches JWT claim (enforced by middleware)
- ✅ MCP tools validate ownership before data access
- ✅ No cross-user conversation or task access possible
- ✅ API key stored securely in environment variables

**Quality Requirements:**
- ✅ Response latency under 3 seconds for simple queries
- ✅ Clean, type-safe code (TypeScript frontend, Python backend)
- ✅ Comprehensive error handling and logging
- ✅ No manual code - all via Claude Code agents
- ✅ Full audit trail in Spec-Kit Plus artifacts

**Demo Readiness:**
- ✅ Sample conversations demonstrating all features
- ✅ Error handling showcased (invalid task ID, ambiguous queries)
- ✅ Multi-user isolation demonstrated (login as different users)
- ✅ Performance acceptable for live demo

### Validation Requirements

**Functional Testing:**
- Test all five MCP tools independently
- Test natural language variations for each operation
- Test multi-step queries and tool chaining
- Test conversation persistence and history retrieval

**Security Testing:**
- Verify JWT validation on chat endpoint
- Attempt cross-user data access (should fail with 403)
- Test with expired/invalid tokens
- Verify tool-level ownership checks

**Integration Testing:**
- End-to-end conversation flows
- Frontend ↔ Backend ↔ Database ↔ Cohere API
- Error propagation through all layers
- Graceful degradation if Cohere API unavailable

**Performance Testing:**
- Measure chat response latency under load
- Database query performance with indexes
- Cohere API response times
- Frontend rendering with long conversation histories

## Governance

This constitution governs all aspects of Phase III development and supersedes any conflicting practices from Phase I or Phase II where explicitly defined. All development activities must comply with the principles and requirements outlined herein.

**Amendment Procedure:** Changes to this constitution require explicit approval and must be documented with version bumps, rationale, and migration plans. All dependent artifacts (specs, plans, tasks, templates) must be reviewed for alignment upon constitution updates.

**Compliance Review:** Regular audits ensure ongoing compliance with constitutional principles. All implementations must verify constitutional compliance as a quality gate. Claude Code agents enforce these principles automatically.

**Version History:**
- v1.0.0 (2025-12-30): Phase I - Console application foundation
- v2.0.0 (2025-12-30): Phase II - Full-stack web application with authentication
- v3.0.0 (2026-02-06): Phase III - AI chatbot integration with MCP tools and Cohere API

**Version:** 3.0.0 | **Ratified:** 2025-12-30 | **Last Amended:** 2026-02-06
