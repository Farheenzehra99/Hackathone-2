# Implementation Plan: AI Todo Chatbot Integration

**Branch**: `001-ai-chatbot` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)

## Summary

Integrate intelligent AI chatbot using Cohere API with 6 MCP tools, stateless FastAPI endpoint, conversation persistence in PostgreSQL, and premium glassmorphic chat UI in Next.js. Enables natural language task management while maintaining JWT auth and user isolation.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript 5.3+, Next.js 16+
**Primary Dependencies**: FastAPI, SQLModel, Cohere SDK, React 18+, Tailwind
**Storage**: PostgreSQL (Neon) - add Conversation/Message tables
**Testing**: pytest, Jest/React Testing Library
**Performance Goals**: <3s response, 100 concurrent users, 60fps UI
**Constraints**: Stateless, JWT mandatory, user isolation, English-only

## Constitution Check

✅ All 7 constitutional principles satisfied - PASSED

## Key Architectural Decisions

**R1: Cohere Model** → command-r-plus (superior reasoning)
**R2: Tool Parsing** → Strict JSON blocks with validation
**R3: Multi-Step** → Loop execution (feed results back until done)
**R4: Conversations** → Optional ID (create if missing, resume if provided)
**R5: UI Layout** → Slide-in bottom-right glassmorphic card
**R6: Messages** → Plain text + minimal markdown (bold, links)

## Database Models

**Conversation**: id, user_id (FK, indexed), created_at, updated_at
**Message**: id, conversation_id (FK, indexed), role, content, tool_calls, created_at

## API Contract

**POST /api/{user_id}/chat**
Request: `{message: str, conversation_id?: str}`
Response: `{conversation_id: str, response: str, tool_calls: str[], timestamp: datetime}`

## MCP Tools (6)

1. add_task, 2. list_tasks, 3. update_task, 4. complete_task, 5. delete_task, 6. get_current_user
All validate user_id, return {success, data, error}

## Frontend Components

ChatbotTrigger → ChatPanel → MessageList → MessageBubble
ChatInput, TypingIndicator, useChat hook

## Timeline

**Phase 0** (Research): 2-4h
**Phase 1** (Design): 4-6h
**Phase 2** (Implementation): 18-24h via /sp.tasks

**Total**: 24-36 hours

## Parallel Execution

Agent 1: Database (models, migrations)
Agent 2: MCP Tools (6 tools)
Agent 3: Backend (Cohere, endpoint)
Agent 4: Frontend (UI components)

## Success Metrics

✅ Tools pass tests with 100% isolation
✅ <3s response time
✅ Multi-step queries work
✅ UI responsive 320px-1920px
✅ Conversation persists
✅ Friendly errors with ✓/⚠

**Next**: Run `/sp.tasks`
