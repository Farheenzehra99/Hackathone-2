# AI Chatbot MVP Testing Checklist

**Date**: 2026-02-06
**Feature**: 001-ai-chatbot
**Phase**: MVP (Phase 1-3 Complete)

## Pre-Testing Setup

### 1. Environment Configuration

- [ ] Copy `.env.example` to `.env`
- [ ] Add your Cohere API key:
  ```bash
  COHERE_API_KEY=your-actual-cohere-api-key-here
  ```
- [ ] Verify `DATABASE_URL` is set
- [ ] Verify `BETTER_AUTH_SECRET` is set

### 2. Backend Setup

```bash
cd backend

# Install dependencies (includes cohere>=5.0.0)
pip install -r requirements.txt

# Run database migration
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --port 8000
```

**Expected Output**: Server running on http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies (if needed)
npm install

# Start development server
npm run dev
```

**Expected Output**: Frontend running on http://localhost:3000

## Manual Testing Scenarios

### Test 1: Chatbot Trigger Button

**Steps**:
1. Navigate to http://localhost:3000/dashboard
2. Log in with test credentials
3. Look for floating button (bottom-right, emerald color)

**Expected**:
- ✅ Button visible at bottom-right
- ✅ Emerald green color
- ✅ Pulse animation when closed
- ✅ Chat icon visible

**Status**: ⬜ Pass / ⬜ Fail
**Notes**: _________________________

---

### Test 2: Open Chat Panel

**Steps**:
1. Click the chatbot trigger button

**Expected**:
- ✅ Chat panel slides in from bottom-right
- ✅ Glassmorphic design with backdrop blur
- ✅ "AI Assistant" header visible
- ✅ Close button (X) visible
- ✅ Empty state message: "Start a conversation!"
- ✅ Suggestion text: "Try: 'Add a task to buy groceries'"
- ✅ Input field at bottom with send button (paper plane icon)

**Status**: ⬜ Pass / ⬜ Fail
**Notes**: _________________________

---

### Test 3: Send Simple Message

**Steps**:
1. Type "Hello" in input field
2. Click send button OR press Enter

**Expected**:
- ✅ User message appears on right side (indigo bubble)
- ✅ Timestamp displayed below message
- ✅ Input field clears
- ✅ Typing indicator appears (three animated dots)
- ✅ Assistant response appears on left side (slate bubble)
- ✅ Message auto-scrolls to bottom

**Status**: ⬜ Pass / ⬜ Fail
**Notes**: _________________________

---

### Test 4: Create Task via Natural Language (PRIMARY MVP TEST)

**Steps**:
1. Type: "Add a task to buy groceries"
2. Send message

**Expected**:
- ✅ User message appears (right, indigo)
- ✅ Typing indicator shows
- ✅ Backend parses Cohere response for tool call
- ✅ `add_task` tool executes with title="buy groceries"
- ✅ Assistant responds: "✓ Task created: 'buy groceries' (ID: ...)"
- ✅ Response appears on left (slate bubble)

**Status**: ⬜ Pass / ⬜ Fail
**Notes**: _________________________

---

### Test 5: Create Task with Description

**Steps**:
1. Type: "Create a task called 'Meeting' with description 'Discuss Q1 goals'"
2. Send message

**Expected**:
- ✅ Cohere extracts both title and description
- ✅ Tool executes with both parameters
- ✅ Confirmation message includes task details

**Status**: ⬜ Pass / ⬜ Fail
**Notes**: _________________________

---

### Test 6: Create Task with Priority

**Steps**:
1. Type: "Add high priority task to review PR"
2. Send message

**Expected**:
- ✅ Cohere extracts priority="high"
- ✅ Tool validates priority value
- ✅ Confirmation includes priority

**Status**: ⬜ Pass / ⬜ Fail
**Notes**: _________________________

---

### Test 7: Ambiguous Request Handling

**Steps**:
1. Type: "Add task"
2. Send message

**Expected**:
- ✅ Cohere recognizes insufficient information
- ✅ Assistant responds: "I need more details. What task would you like to add?"
- ✅ No tool call executed

**Status**: ⬜ Pass / ⬜ Fail
**Notes**: _________________________

---

### Test 8: Close and Reopen Chat

**Steps**:
1. Click X button to close chat panel
2. Click chatbot trigger button again

**Expected**:
- ✅ Chat panel closes with animation
- ✅ Trigger button icon changes back to chat icon
- ✅ Pulse animation resumes
- ✅ Reopening shows previous conversation history
- ✅ Messages persist

**Status**: ⬜ Pass / ⬜ Fail
**Notes**: _________________________

---

### Test 9: Responsive Design (Mobile)

**Steps**:
1. Open browser DevTools
2. Switch to mobile view (320px width)
3. Open chatbot

**Expected**:
- ✅ Chat panel full-width on mobile
- ✅ Trigger button still visible
- ✅ Messages readable
- ✅ Input field usable
- ✅ Send button accessible

**Status**: ⬜ Pass / ⬜ Fail
**Notes**: _________________________

---

### Test 10: Theme Adaptation (Dark/Light)

**Steps**:
1. Toggle theme in application
2. Observe chatbot colors

**Expected**:
- ✅ Chat panel background adapts to theme
- ✅ Text colors remain readable
- ✅ Border colors adjust
- ✅ Message bubbles maintain contrast

**Status**: ⬜ Pass / ⬜ Fail
**Notes**: _________________________

---

## Known Limitations (TODOs in Code)

### Backend:
1. **Database Integration**:
   - Placeholder user_id ("placeholder-user-id")
   - Conversation/Message persistence not connected
   - Task model integration needed

2. **JWT Validation**:
   - `get_current_user_id()` is placeholder
   - Real Better Auth integration needed

3. **Only 1 Tool**:
   - Only `add_task` implemented
   - `list_tasks`, `complete_task`, etc. not yet added

### Frontend:
1. **Auth Token**:
   - Uses localStorage fallback
   - Better Auth integration needed

2. **Conversation History**:
   - Returns empty array (backend endpoint not implemented)

## Error Scenarios to Test

### E1: Network Error
**Steps**: Disconnect internet, send message
**Expected**: "⚠ Network error - please check your connection"
**Status**: ⬜ Pass / ⬜ Fail

### E2: Invalid Priority
**Steps**: (Once validated) Send "Add super urgent task"
**Expected**: "Priority must be low, medium, or high"
**Status**: ⬜ Pass / ⬜ Fail

### E3: Cohere API Failure
**Steps**: Use invalid COHERE_API_KEY
**Expected**: "⚠ I'm having trouble connecting right now"
**Status**: ⬜ Pass / ⬜ Fail

---

## Test Results Summary

**Total Tests**: 13 (10 functional + 3 error scenarios)
**Passed**: ___
**Failed**: ___
**Blocked**: ___

### Critical Issues Found:
1. _________________________
2. _________________________
3. _________________________

### Non-Critical Issues:
1. _________________________
2. _________________________

### Recommendations:
- [ ] Fix critical issues before continuing
- [ ] Integrate actual database persistence
- [ ] Connect Better Auth JWT validation
- [ ] Add remaining P1 tools (list_tasks, complete_task)
- [ ] Continue to Phase 4-6 (P1 features)

---

**Tester**: _________________________
**Date Tested**: _________________________
**Sign-off**: _________________________
