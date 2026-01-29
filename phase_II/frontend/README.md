# Todo App - Frontend

A beautiful, modern todo application with premium features and delightful user experience.

## Features

- 🎨 **Premium UI/UX**: Beautiful, modern interface with smooth animations and micro-interactions
- 🔐 **Secure Authentication**: JWT-based authentication with Better Auth integration
- 📱 **Responsive Design**: Fully responsive layout for desktop, tablet, and mobile devices
- ⌨️ **Keyboard Shortcuts**: Efficient keyboard navigation for power users
- 🔄 **Real-time Updates**: Optimistic UI updates for instant feedback
- ♻️ **Undo Functionality**: Ability to undo task deletions
- 🔍 **Search & Filter**: Powerful search and filtering capabilities
- ♿ **Accessibility**: WCAG AA compliant for inclusive user experience

## Tech Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript 5.3+
- **Styling**: Tailwind CSS with custom design system
- **UI Components**: Shadcn/ui
- **Animations**: Framer Motion
- **Forms**: React Hook Form with Zod validation
- **Authentication**: Better Auth with JWT handling

## Installation

1. Clone the repository
2. Navigate to the frontend directory: `cd frontend`
3. Install dependencies: `npm install` or `yarn install` or `pnpm install`
4. Copy the environment file: `cp .env.local.example .env.local`
5. Start the development server: `npm run dev` or `yarn dev` or `pnpm dev`

## Environment Variables

Create a `.env.local` file in the root of the frontend directory with the following variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Scripts

- `npm run dev`: Start the development server
- `npm run build`: Build the application for production
- `npm run start`: Start the production server
- `npm run lint`: Lint the codebase

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication pages
│   ├── (dashboard)/       # Dashboard pages
│   ├── layout.tsx         # Root layout with providers
│   └── page.tsx           # Home page
├── components/            # Reusable UI components
│   ├── providers/         # Context providers
│   ├── ui/               # Shadcn/ui components
│   └── tasks/            # Task-specific components
├── lib/                  # Shared utilities and types
│   ├── types.ts          # TypeScript type definitions
│   ├── api-client.ts     # API client with JWT handling
│   ├── validations.ts    # Zod validation schemas
│   └── utils.ts          # Utility functions
├── hooks/                # Custom React hooks
└── public/               # Static assets
```

## API Integration

The frontend communicates with the backend API using the API client located at `lib/api-client.ts`. All API calls include proper JWT authentication headers and error handling.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a pull request

## License

This project is licensed under the MIT License.