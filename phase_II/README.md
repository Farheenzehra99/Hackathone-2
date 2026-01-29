# Todo App with Glassmorphism UI

A modern todo application featuring a beautiful glassmorphism design with dark theme.

## Features

- **Glassmorphism UI**: Beautiful frosted glass effect design with backdrop blur
- **Dark Theme**: Elegant dark interface with proper contrast ratios
- **Task Management**: Create, read, update, and delete tasks
- **Priority System**: Assign low, medium, or high priority to tasks
- **Status Tracking**: Mark tasks as pending or completed
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Local Storage**: Tasks persist between sessions

## Tech Stack

- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Lucide React (icons)
- React Hook Form (form handling)
- Zod (validation)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd todo-app-glassmorphism
```

2. Navigate to the frontend directory:
```bash
cd frontend
```

3. Install dependencies:
```bash
npm install
```

4. Run the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Usage

- Click "Add Task" to create a new task
- Use the form to set task title, description, priority, and status
- Click the circle icon to toggle task completion status
- Use the pencil icon to edit a task
- Use the trash icon to delete a task
- Tasks are automatically saved to browser's localStorage

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