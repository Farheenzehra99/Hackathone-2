# Todo App with Glassmorphism UI

A modern todo application featuring a beautiful glassmorphism design with dark theme.

## Features

- **AI-Powered Chatbot**: Intelligent task management assistant using Cohere API
- **Natural Language Processing**: Create, list, update, and delete tasks using conversational language
- **Glassmorphism UI**: Beautiful frosted glass effect design with backdrop blur
- **Dark Theme**: Elegant dark interface with proper contrast ratios
- **Task Management**: Create, read, update, and delete tasks
- **Priority System**: Assign low, medium, or high priority to tasks
- **Status Tracking**: Mark tasks as pending or completed
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Conversation Persistence**: Chat history persists across sessions
- **Multi-Step Queries**: Handle complex requests requiring multiple operations

## Tech Stack

### Frontend
- Next.js 16 (App Router)
- React 18
- TypeScript 5.3+
- Tailwind CSS
- Shadcn/ui components
- React Hook Form (form handling)
- Zod (validation)

### Backend
- Python 3.11+
- FastAPI
- SQLModel (async SQLAlchemy)
- PostgreSQL (Neon)
- Cohere API (command-r-plus model)
- Better Auth (JWT authentication)

## Installation

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL database (or Neon account)
- Cohere API key ([Get one free at cohere.com](https://cohere.com))

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd phase_III
```

2. Navigate to the backend directory:
```bash
cd backend
```

3. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_db

# Cohere API
COHERE_API_KEY=your_cohere_api_key_here

# Auth
JWT_SECRET=your_jwt_secret_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

6. Run database migrations:
```bash
alembic upgrade head
```

7. Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at [http://localhost:8000](http://localhost:8000)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd ../frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
```

Edit `.env.local` and add:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## AI Magic Highlights

### Natural Language Task Management

Our AI chatbot powered by Cohere's command-r-plus model understands natural language and makes task management effortless:

#### What You Can Say

**Creating Tasks:**
- "Add a task to buy groceries"
- "Create a high priority task for the team meeting tomorrow"
- "Remind me to call mom"

**Listing Tasks:**
- "Show me my tasks"
- "List all pending tasks"
- "What high priority tasks do I have?"
- "Show completed tasks"

**Updating Tasks:**
- "Mark task 5 as done"
- "Change the priority of task 3 to high"
- "Update task 7 description to 'Buy milk and bread'"
- "Mark task 2 as incomplete"

**Deleting Tasks:**
- "Delete task 5"
- "Remove the groceries task"

**Getting Info:**
- "Who am I?"
- "Show my account information"

**Multi-Step Queries:**
- "Add task 'Weekly meeting' and list my pending tasks"
- "Mark task 5 done and show all completed tasks"
- "Create three tasks: buy milk, call john, review PR"

### Smart Features

- **Context Understanding**: The AI understands variations in how you phrase requests
- **Tool Chaining**: Handles complex multi-step operations in a single message
- **Conversation Memory**: Remembers context within the conversation
- **Friendly Responses**: Uses ✓ for success and ⚠ for warnings/errors
- **Rate Limiting**: Prevents abuse (10 messages per minute)
- **User Isolation**: Each user can only access their own tasks

### How to Use the Chatbot

1. **Open the Chat**: Click the floating green chat button in the bottom-right corner
2. **Type Your Message**: Use natural language to describe what you want
3. **See Results**: The AI will execute the appropriate tool(s) and respond
4. **Continue Conversation**: Your chat history is saved and persists across sessions

## Usage (Traditional UI)

- Click "Add Task" to create a new task
- Use the form to set task title, description, priority, and status
- Click the circle icon to toggle task completion status
- Use the pencil icon to edit a task
- Use the trash icon to delete a task
- Tasks are automatically saved to PostgreSQL database

## Design Highlights

- **Glassmorphism Effect**: Achieved using `backdrop-filter: blur()` and semi-transparent backgrounds
- **Smooth Animations**: Hover effects and transitions for enhanced user experience
- **Accessibility**: Proper ARIA labels and keyboard navigation support
- **Responsive Layout**: Adapts to different screen sizes

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/          # Reusable UI components
│   │   ├── ui/             # Base UI components
│   │   └── todo/           # Todo-specific components
│   ├── hooks/              # Custom React hooks
│   │   └── use-task-manager.ts
│   ├── lib/                # Utilities and constants
│   │   ├── constants.ts
│   │   └── utils.ts
│   └── styles/             # Global styles
│       └── glassmorphism.css
└── public/                 # Static assets
```

## Components

- **GlassNavbar**: Fixed top navigation bar with glass effect
- **TaskCard**: Displays individual tasks with glassmorphism styling
- **TaskForm**: Form for creating and editing tasks
- **TaskManager**: Main component managing task state
- **GlassModal**: Reusable modal component with glass effect
- **PriorityBadge**: Visual indicator for task priority

## Custom Hooks

- **useTaskManager**: Manages all task operations (CRUD) with localStorage persistence

## Styling

The application uses Tailwind CSS with custom glassmorphism utility classes:

- `glass-container`: Base glass effect container
- `glass-card`: Glass effect card component
- `glass-navbar`: Glass effect navigation bar
- `glass-button`: Glass effect button
- `glass-input`: Glass effect input field

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License.