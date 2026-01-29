# Skill: Conversation Context (Light) Manager

## 1. Purpose
Maintain minimal, short-term conversational context to enable seamless follow-up interactions without adding complexity to the broader system. This skill stores and retrieves just enough context to resolve ambiguous references in multi-step workflows.

## 2. Owned By
Agent: **context-light-manager**

## 3. When to Use
Invoke this skill when:
- User completes an action that might have follow-up interactions
- Processing a command that references previous context (e.g., "add that", "update it")
- Need to resolve ambiguous references to recent tasks or entities
- Context should be preserved between messages in a workflow
- User explicitly signals completion and context should be cleared

## 4. Input

**Required Inputs:**
```
action: string (enum: "store" | "retrieve" | "clear")
```
The operation to perform on context.

**Optional Inputs (for "store" action):**
```
last_intent: string
```
Primary intent of the last completed action (e.g., 'task_creation', 'code_review')

```
last_task_id: string | number
```
Identifier of the most recent task or entity created/modified

```
pending_fields: string[]
```
Array of fields awaiting user input or clarification

```
last_user_message: string
```
Verbatim copy of the user's last message for reference

**Constraints:**
- action is required
- For "store", all context fields are required
- Context fields are specific and limited (no arbitrary data)
- Storage is session-scoped (in-memory or temporary file)

## 5. Step-by-Step Process

### Step 1: Context Storage (action: "store")
Store conversational context after a user interaction.

**Storage Process:**
1. **Store last_intent**: Capture the primary intent of the completed action
   - Examples: 'task_creation', 'task_update', 'task_completion', 'code_review'
   - Must be descriptive enough to understand what happened
   - Keep intent names consistent across the application

2. **Store last_task_id**: Capture identifier of most recent entity
   - Task ID if task-related action
   - Entity ID for other operations
   - Null if no entity was created/modified
   - Store as string for consistency

3. **Store pending_fields**: Capture fields awaiting input
   - Array of field names needing user input
   - Empty array if no pending fields
   - Enables context-aware follow-up prompts

4. **Store last_user_message**: Capture verbatim user message
   - Exact copy of user's last message
   - Enables reference resolution ("that", "it", "the task")
   - Useful for disambiguation

**Storage Requirements:**
- Use session-scoped storage (in-memory Map or temporary file)
- Storage must be accessible within 10ms
- No persistence beyond current session
- Thread-safe access if concurrent operations possible

**Storage Data Structure:**
```typescript
interface ConversationContext {
  last_intent: string | null
  last_task_id: string | null
  pending_fields: string[]
  last_user_message: string | null
}
```

### Step 2: Context Retrieval (action: "retrieve")
Retrieve stored conversational context to resolve follow-up commands.

**Retrieval Process:**
1. **Access stored context**: Read all four context fields
2. **Return complete context**: Return all stored values
3. **Handle empty context**: Return null or empty structure if nothing stored

**Retrieval Requirements:**
- Return all fields even if some are null/empty
- Do not filter or modify context on retrieval
- Return as-is for caller to interpret
- Gracefully handle missing context

**Retrieval Use Cases:**
- Resolve "add that" → use last_task_id
- Resolve "update it" → use last_intent and last_task_id
- Resolve "the task" → use last_task_id and last_user_message
- Understand workflow state → use last_intent and pending_fields

### Step 3: Context Clearing (action: "clear")
Clear stored context when no longer needed.

**Clearing Process:**
1. **Clear all fields**: Set all four fields to null/empty
2. **Preserve storage**: Keep storage object but clear contents
3. **Immediate effect**: Context is unavailable after clear

**Clearing Triggers:**
- User explicitly signals completion ("done", "thanks", "that's all")
- New, unrelated intent detected that breaks conversation flow
- Context has been successfully applied to resolve follow-up
- Session ends or timeout occurs

**Clearing Requirements:**
- Must clear all fields (no selective clearing)
- Operation must complete immediately
- No side effects beyond the four managed fields

### Step 4: Storage Implementation
Implement storage mechanism for context management.

**Storage Options:**

**Option 1: In-Memory Storage (Recommended)**
```typescript
class ContextManager {
  private context: ConversationContext = {
    last_intent: null,
    last_task_id: null,
    pending_fields: [],
    last_user_message: null
  }

  store(intent: string, taskId: string | null, fields: string[], message: string): void {
    this.context.last_intent = intent
    this.context.last_task_id = taskId
    this.context.pending_fields = fields
    this.context.last_user_message = message
  }

  retrieve(): ConversationContext | null {
    if (!this.context.last_intent) return null
    return { ...this.context }
  }

  clear(): void {
    this.context = {
      last_intent: null,
      last_task_id: null,
      pending_fields: [],
      last_user_message: null
    }
  }
}
```

**Option 2: Temporary File Storage**
- Use temporary file in system temp directory
- Write/read JSON on each operation
- Clean up on session end
- Slower but persists across restarts (if needed)

**Implementation Requirements:**
- Simple get/set/clear operations
- Minimal and focused implementation
- Session-scoped storage
- Fast access (<10ms)
- Thread-safe if needed
- No external dependencies

### Step 5: Operation Routing
Route to appropriate operation based on action parameter.

**Routing Logic:**
- If action === "store": Execute Step 1
- If action === "retrieve": Execute Step 2
- If action === "clear": Execute Step 3
- If action invalid: Return error

**Validation:**
- Validate action is one of allowed values
- For "store", validate all required context fields provided
- Return structured error for invalid input

### Step 6: Output Generation
Return operation result based on action.

**Store Output:**
```json
{
  "success": true,
  "stored_context": {
    "last_intent": "task_creation",
    "last_task_id": "123",
    "pending_fields": [],
    "last_user_message": "Create a new task for refactoring"
  }
}
```

**Retrieve Output:**
```json
{
  "success": true,
  "context": {
    "last_intent": "task_creation",
    "last_task_id": "123",
    "pending_fields": [],
    "last_user_message": "Create a new task for refactoring"
  }
}
```

**Clear Output:**
```json
{
  "success": true,
  "message": "Context cleared successfully"
}
```

**Error Output:**
```json
{
  "success": false,
  "error": "Invalid action: 'update'. Must be 'store', 'retrieve', or 'clear'"
}
```

## 6. Output

**Output Schema:**

**Success Response:**
```json
{
  "success": true,
  "context": {
    "last_intent": "string|null",
    "last_task_id": "string|null",
    "pending_fields": "string[]",
    "last_user_message": "string|null"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "string"
}
```

**Output Constraints:**
- Raw JSON only, no markdown code fences
- No explanatory text before or after JSON
- context field only present on successful retrieve
- error field only present on failure
- All context fields present even if null

## 7. Failure Handling

### Invalid Action
- If action is not "store", "retrieve", or "clear":
  - Return error response
  - Describe valid actions
  - Do not modify stored context

### Missing Input for Store
- If context fields missing for "store" action:
  - Return error response
  - List missing required fields
  - Do not store partial context

### Storage Failures
- If storage operation fails (file I/O, permission issues):
  - Return error response
  - Describe storage failure
  - Fail silently if possible (don't block main operation)

### Context Unavailable
- If retrieve called on empty storage:
  - Return success with null context
  - Do not treat as error
  - Allow caller to handle missing context

**Non-Destructive Behavior:**
- Never perform intent parsing or reasoning
- Never modify task state or execute commands
- Never interact with external systems beyond storage
- Never persist context beyond session
- Fail silently if storage unavailable (don't block main operations)

**Quality Assurance:**
- Context retrieved within 10ms
- Zero side effects beyond four managed fields
- No logging or debugging output in production
- Fail gracefully without blocking primary operations
- Safe to ignore if empty or unavailable
