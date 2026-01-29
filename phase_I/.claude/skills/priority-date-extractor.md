# Skill: Priority & Date Extractor

## 1. Purpose
Extract due dates, times, and priority levels from natural language input for todo task creation and modification. This skill handles temporal expression parsing in English and basic Urdu, providing structured scheduling data for the Todo CLI application.

## 2. Owned By
Agent: **priority-date-extractor**

## 3. When to Use
Invoke this skill when:
- User provides task input that may contain date/time information
- User mentions priority or urgency in task description
- Creating new tasks with scheduling details
- Modifying existing task deadlines or priorities
- Parsing natural language temporal expressions

## 4. Input

**Required Input:**
```
user_input: string
```
Natural language text containing possible date, time, or priority information.

**Constraints:**
- Input must be non-empty string
- Input may be in English or basic Urdu
- Input may contain multiple temporal expressions (use most specific)
- Input may be ambiguous or incomplete

## 5. Step-by-Step Process

### Step 1: Language Detection
Determine the primary language of the input text.
- Check for Urdu script (Arabic characters)
- Check for Urdu temporal keywords (kal, parso, agle hafte, baje)
- Check for Urdu priority keywords (zaruri, fauri)
- Set language flag for processing rules

### Step 2: Due Date Extraction
Parse temporal expressions to extract due dates.

**English Temporal Patterns:**
- "today" → current date
- "tomorrow" → current date + 1 day
- "next week" → current date + 7 days
- "next Monday/Tuesday/etc." → next occurrence of named day
- "in 2 days" → current date + 2 days
- "by [date]" → specified date
- "end of week" → upcoming Friday or Sunday
- "Jan 15" → January 15 of current year
- "January 15th, 2024" → 2024-01-15

**Urdu Temporal Patterns:**
- "kal" → tomorrow (current date + 1 day)
- "parso" → day after tomorrow (current date + 2 days)
- "agle hafte" → next week (current date + 7 days)
- "agle hafte somvar" → next Monday
- "is hafte" → this week

**Extraction Rules:**
- Identify all temporal expressions in input
- Select the most specific date mentioned
- Convert to ISO 8601 format: YYYY-MM-DD
- Use current date as reference point for relative expressions
- Return null if no date or ambiguous date detected

### Step 3: Time Extraction
Parse time expressions to extract specific times.

**English Time Patterns:**
- "3pm", "3 PM" → 15:00
- "3:30pm", "3:30 PM" → 15:30
- "15:00", "15:00" → 15:00
- "3 o'clock" → 15:00 (if PM implied) or 03:00
- "by 3pm" → 15:00

**Urdu Time Patterns:**
- "5 baje" → 5:00 (need AM/PM context for conversion)
- "dopahar 2 baje" → 14:00
- "sham 6 baje" → 18:00

**Conversion Rules:**
- Identify time patterns in input
- Convert 12-hour format to 24-hour format:
  - AM: 12:00 AM → 00:00, 1:00 AM → 01:00
  - PM: 12:00 PM → 12:00, 1:00 PM → 13:00
- Ensure output format is HH:MM
- Return null if no time mentioned or ambiguous

### Step 4: Priority Extraction
Extract priority level from input text.

**English Priority Keywords:**
- "urgent", "asap", "right now" → "urgent"
- "high", "important", "critical" → "high"
- "medium", "normal" → "medium"
- "low", "whenever" → "low"

**Urdu Priority Keywords:**
- "zaruri", "fauri", "turant" → "urgent"
- "muhim" → "high"
- "mamooli" → "medium"
- "kam" → "low"

**Extraction Rules:**
- Scan input for priority keywords
- Map detected keywords to standard levels
- If multiple priorities mentioned, use highest urgency
- Return null if no priority mentioned

### Step 5: Confidence Assessment
Evaluate confidence level based on input clarity.

**High Confidence:**
- Date/time/priority explicitly stated and unambiguous
- Clear temporal expressions with specific values
- Example: "finish report by tomorrow 3pm, high priority"

**Medium Confidence:**
- Information clearly implied but not explicit
- Relative dates with clear reference
- Example: "task for next Friday"

**Low Confidence:**
- Input unclear, ambiguous, or incomplete
- Vague temporal references
- Example: "meeting sometime next week"

**Confidence Assignment:**
- If all three fields are clear: confidence = "high"
- If some fields are inferred: confidence = "medium"
- If input is vague or ambiguous: confidence = "low"
- When confidence is low, set uncertain fields to null

### Step 6: Validation
Validate extracted values.

**Date Validation:**
- YYYY-MM-DD format
- Date is in future when context suggests future intent
- Valid calendar date (not February 30)

**Time Validation:**
- HH:MM format in 24-hour time
- Valid hour (00-23) and minute (00-59)

**Priority Validation:**
- One of: urgent, high, medium, low

**Confidence Validation:**
- One of: high, medium, low

### Step 7: Output Generation
Generate JSON response with extracted fields.

**Never generate code or explanations. Output only JSON.**

## 6. Output

**Output Schema:**
```json
{
  "due_date": "YYYY-MM-DD|null",
  "time": "HH:MM|null",
  "priority": "urgent|high|medium|low|null",
  "confidence": "high|medium|low"
}
```

**Output Constraints:**
- Raw JSON only, no markdown code fences
- No explanatory text before or after JSON
- Explicit null values for unspecified fields
- No trailing commas
- Proper double-quoting of strings

## 7. Failure Handling

### Invalid Input
- Empty string: Set all fields to null, confidence="low"
- Non-string input: Error - do not process

### Date Extraction Failure
- Cannot parse date: Set due_date=null
- Ambiguous date: Set due_date=null, lower confidence
- Multiple dates detected: Select most specific, or set to null if equally specific

### Time Extraction Failure
- Cannot parse time: Set time=null
- AM/PM ambiguity: Set time=null (do not guess)
- Invalid time format: Set time=null

### Priority Extraction Failure
- No priority keywords: Set priority=null
- Conflicting priorities: Select highest urgency
- Unrecognized keyword: Ignore, do not guess

### Low Confidence Handling
- When confidence="low", set uncertain fields to null
- Do not return extracted values if confidence is low
- Let caller handle missing information

**Non-Destructive Behavior:**
- Never modify user input
- Never infer or guess missing information
- Failures result in null values or low confidence
- Never throw exceptions or crash

**Quality Assurance:**
- Always return valid JSON
- Only extract what is explicitly stated
- Maintain consistency across multiple invocations
- Ensure deterministic output for same input
