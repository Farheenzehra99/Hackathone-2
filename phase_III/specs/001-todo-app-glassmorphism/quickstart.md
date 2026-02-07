# Quickstart Guide: Todo App with Glassmorphism UI

## Prerequisites
- Node.js 18+
- npm or yarn
- Git

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install dependencies
```bash
cd frontend
npm install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:3000/api
```

### 4. Run the development server
```bash
npm run dev
```

The app will be available at http://localhost:3000

## Development Commands

### Start development server
```bash
npm run dev
```

### Build for production
```bash
npm run build
```

### Run tests
```bash
npm run test
```

### Run linting
```bash
npm run lint
```

### Run formatting
```bash
npm run format
```

## Project Structure
```
frontend/
├── src/
│   ├── app/                # Next.js App Router pages
│   ├── components/         # Reusable UI components
│   ├── lib/               # Utilities and constants
│   ├── hooks/             # Custom React hooks
│   └── styles/            # Global styles
├── public/                # Static assets
├── package.json           # Dependencies and scripts
└── tailwind.config.js     # Tailwind CSS configuration
```

## Glassmorphism Design System

### Base Classes
- `glass-container`: Basic glassmorphism container
- `glass-card`: Card with glass effect
- `glass-navbar`: Navigation bar with glass effect
- `glass-button`: Button with glass effect

### Color Variables
- `--glass-bg`: rgba(255, 255, 255, 0.1) for light themes
- `--glass-border`: rgba(255, 255, 255, 0.2) for light themes
- `--glass-bg-dark`: rgba(0, 0, 0, 0.4) for dark themes
- `--glass-border-dark`: rgba(255, 255, 255, 0.2) for dark themes

### Responsive Breakpoints
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px