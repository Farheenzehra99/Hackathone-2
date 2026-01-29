# Skill: Todo Intent Parser

## 1. Purpose
Parse natural language todo commands into structured JSON operations for the Todo CLI application. This skill converts user intent into a machine-readable format that can be processed by downstream task management logic.

## 2. Owned By
Agent: **todo-intent-parser**

## 3. When to Use
Invoke this skill when:
- User provides any natural language input that appears to be a todo/task command
- Before executing any task manipulation operations (add, update, delete, complete, list, reschedule)
- When user input language needs to be detected (English or Urdu)
- When command intent is ambiguous and needs clarification

## 4. Input

**Required Input:**
```
user_input: string
```
The raw natural language message from the user.

**Constraints:**
- Input must be non-empty string
- Input may contain mixed English/Urdu text
- Input may contain temporal expressions, priority keywords, or task references
- Input may be malformed or ambiguous

## 5. Step-by-Step Process

### Step 1: Language Detection
Analyze the input text to determine the dominant language.
- Check script: Arabic script for Urdu, Latin for English
- Check vocabulary: Urdu keywords (kal, kar do, parso, etc.) vs English keywords
- Check grammar patterns
- Set `language` field to "en" or "ur"

### Step 2: Intent Classification
Determine the primary intent from the input.
- **add**: Keywords indicating creation (add, create, new, make, add karo, banao)
- **update**: Keywords indicating modification (change, update, modify, edit, badl do)
- **delete**: Keywords indicating removal (delete, remove, delete karo, hatao)
- **complete**: Keywords indicating completion (complete, finish, done, mark as done, complete kar do)
- **list**: Keywords indicating retrieval (show, list, display, all tasks, dikhao)
- **reschedule**: Keywords indicating date/time change (move, reschedule, change date, shift)
- **clarify**: When intent cannot be determined with confidence or multiple intents detected

### Step 3: Entity Extraction
Extract relevant entities based on the detected intent.

For **task_id**:
- Search for numeric patterns (task 5, #3, id: 7)
- Search for task references (that task, task id 5)
- Return null if no explicit ID is mentioned

For **title**:
- Extract for "add" intent: main task description
- Extract for "update" intent only if updating title
- Return null for non-add/update intents
- Remove intent keywords from extracted title

For **description**:
- Extract detailed information when explicitly provided
- Look for phrases like "with description", "details:"
- Return null if not explicitly provided

For **due_date**:
- Parse temporal expressions (tomorrow, next week, Friday, Jan 15)
- Convert to ISO 8601 format: YYYY-MM-DD
- Use current date as reference point
- Return null if no date mentioned or date is ambiguous

For **priority**:
- Extract priority keywords (high, medium, low, urgent, important, zaruri)
- Normalize to lowercase
- Return null if not mentioned

### Step 4: Temporal Expression Processing
Convert natural language dates to ISO 8601 format.

**Processing Rules:**
- "today" → current date
- "tomorrow" → current date + 1 day
- "next week" → current date + 7 days
- "Friday" / "shukravar" → next occurrence of that day
- "Jan 15" → current year January 15
- "kal" → tomorrow
- "parso" → day after tomorrow

**Ambiguity Handling:**
- If date cannot be resolved, set to null
- If relative date lacks reference point (e.g., "sometime"), set to null
- If multiple conflicting dates, set to null

### Step 5: Ambiguity Detection
Check if intent is ambiguous or missing critical information.

Return intent="clarify" when:
- Multiple distinct operations are requested in one command
- Command structure is malformed (e.g., "do something with that task" without context)
- Required information for detected intent is missing (e.g., "delete it" without task_id)
- Conflicting instructions are present
- Intent cannot be determined with confidence

**Do NOT guess or assume missing information.**

### Step 6: Validation
Validate all extracted entities before output.

**Validation Checklist:**
- Intent is one of: add, update, delete, complete, list, reschedule, clarify
- Language is exactly "en" or "ur"
- task_id is number or null
- title, description are string or null
- due_date follows YYYY-MM-DD format if present
- priority is one of: high, medium, low if present

### Step 7: Output Generation
Generate JSON response with all fields, setting missing/unextracted values to null.

**Never generate code or explanations. Output only JSON.**

## 6. Output

**Output Schema:**
```json
{
  "intent": "add|update|delete|complete|list|reschedule|clarify",
  "task_id": number|null,
  "title": string|null,
  "description": string|null,
  "due_date": "YYYY-MM-DD"|null,
  "priority": "high|medium|low|null",
  "language": "en|ur"
}
```

**Output Constraints:**
- Raw JSON only, no markdown code fences
- No explanatory text before or after JSON
- Explicit null values for unspecified fields (not empty strings)
- No trailing commas in JSON
- Proper double-quoting of strings

## 7. Failure Handling

### Invalid Input
- Empty string: Set intent="clarify", all other fields null
- Non-string input: Error - do not process

### Ambiguous Intent
- Multiple intents detected: Set intent="clarify", explain in error handling (not in output)
- Clear intent but missing required data: Set intent="clarify"

### Entity Extraction Failure
- Cannot parse date: Set due_date=null
- Cannot resolve priority: Set priority=null
- Cannot extract task_id: Set task_id=null

### Language Detection Failure
- Unable to determine language: Default to "en" (English)

### JSON Generation Failure
- Invalid JSON structure: Rebuild from scratch with proper schema
- Missing required fields: Fill with null values

**Non-Destructive Behavior:**
- Never modify user input
- Never make assumptions beyond explicit information
- Failures result in null values or clarify intent
- Never throw exceptions or crash

**Quality Assurance:**
- Always return valid JSON
- Preserve user intent accurately
- Maintain consistency across multiple invocations
- Ensure deterministic output for same input
