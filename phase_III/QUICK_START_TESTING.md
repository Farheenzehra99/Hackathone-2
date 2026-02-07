# Quick Start: AI Chatbot MVP Testing

## 🚀 5-Minute Setup

### Step 1: Environment Variables (30 seconds)

```bash
# Copy example to .env
cp .env.example .env

# Edit .env and add your Cohere API key:
COHERE_API_KEY=your-key-here
```

**Get Cohere API Key**: https://dashboard.cohere.com/api-keys

### Step 2: Backend Setup (2 minutes)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migration (creates conversation + message tables)
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

Server: http://localhost:8000

### Step 3: Frontend Setup (2 minutes)

```bash
cd frontend

# Install if needed
npm install

# Start dev server
npm run dev
```

Frontend: http://localhost:3000

---

## ✅ Quick Test (30 seconds)

1. **Open**: http://localhost:3000/dashboard
2. **Login**: Use existing test account
3. **Click**: Green floating button (bottom-right)
4. **Type**: "Add a task to buy groceries"
5. **Press**: Enter

**Expected Result**:
```
You: Add a task to buy groceries
AI: ✓ Task created: 'buy groceries' (ID: ...)
```

---

## 🎯 What Works Now (MVP Core)

✅ **UI**: Beautiful glassmorphic chat panel
✅ **AI**: Cohere command-r-plus integration
✅ **NLP**: Understands "Add task..." variations
✅ **Tool**: add_task executes correctly
✅ **UX**: Typing indicators, smooth animations
✅ **Responsive**: Works on mobile + desktop
✅ **Theme**: Dark/light mode support

---

## ⚠️ Known Limitations

❌ **Database**: Conversations not persisting (placeholder)
❌ **Auth**: JWT validation is placeholder
❌ **Tools**: Only add_task works (list/complete/delete not implemented)
❌ **History**: Conversation history doesn't load yet
❌ **Multi-step**: Complex queries not supported yet

These will be fixed in Phase 4-13 (30 remaining tasks).

---

## 🐛 Common Issues

### Issue: "COHERE_API_KEY not set"
**Fix**: Add key to `.env` file and restart backend

### Issue: "Module 'cohere' not found"
**Fix**: Run `pip install -r backend/requirements.txt`

### Issue: Frontend won't connect
**Fix**: Check backend is running on port 8000

### Issue: "Conversation not found"
**Fix**: Expected - database persistence coming in Phase 8

---

## 📊 Test Checklist

Use `TESTING_CHECKLIST.md` for comprehensive testing.

**Quick Smoke Test** (5 minutes):
- [ ] Chat button appears
- [ ] Panel opens/closes
- [ ] Can send messages
- [ ] AI responds
- [ ] "Add task" works
- [ ] Mobile responsive

---

## 🎉 Success Criteria

MVP is successful if:
1. ✅ Chatbot UI loads without errors
2. ✅ Can send/receive messages
3. ✅ "Add task to [title]" creates task
4. ✅ AI provides friendly confirmations
5. ✅ Works on mobile + desktop

**Demo Ready**: Yes! (with known limitations)

---

## 🚦 Next Steps

After testing:

1. **If MVP works**: Continue to Phase 4-6 (P1 features)
   - list_tasks tool
   - complete_task tool
   - UI polish (TypingIndicator improvements)

2. **If issues found**: Fix critical bugs first
   - Check TESTING_CHECKLIST.md results
   - Review error logs
   - Test edge cases

3. **Production Ready**: Complete remaining 30 tasks
   - Phases 4-13
   - Full feature set
   - Security + polish

---

**Status**: 🟢 MVP READY FOR TESTING
**Progress**: 22/52 tasks (42%)
**Estimated Test Time**: 15-30 minutes
