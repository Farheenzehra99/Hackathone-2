# Frontend Quickstart Guide

## Setup Instructions

### Prerequisites
- Node.js 18+
- npm or yarn package manager
- Access to backend API endpoints

### Installation

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment variables**
   Copy the `.env.example` file to `.env.local` and update with your configuration:
   ```bash
   cp .env.example .env.local
   ```

   Required variables:
   - `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
   - `NEXT_PUBLIC_BETTER_AUTH_URL`: URL for Better Auth server
   - `BETTER_AUTH_SECRET`: Secret for JWT signing (shared with backend)

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Visit [http://localhost:3000](http://localhost:3000) to see the application

## Key Scripts

- `npm run dev`: Start development server with hot reloading
- `npm run build`: Build the application for production
- `npm run start`: Start production server
- `npm run lint`: Run ESLint to check for code issues
- `npm run test`: Run unit tests
- `npm run test:e2e`: Run end-to-end tests

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
├── components/            # Reusable React components
├── lib/                  # Utility functions and API clients
├── hooks/               # Custom React hooks
├── styles/              # Global styles
├── public/              # Static assets
├── types/               # TypeScript type definitions
└── __tests__/           # Test files
```

## Key Technologies Used

- **Next.js 16+**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Better Auth**: Authentication library with JWT support
- **Shadcn/ui**: Accessible UI components
- **React Hook Form**: Form management
- **Zod**: Schema validation
- **Framer Motion**: Animations

## Development Guidelines

### Component Development
- Use Shadcn/ui components when possible for consistency
- Create new components in the `components/` directory
- Follow accessibility best practices
- Add TypeScript interfaces for props

### Styling
- Use Tailwind CSS utility classes
- Leverage the configured theme in `tailwind.config.ts`
- Use responsive prefixes for mobile-first design
- Maintain consistent spacing with the design system

### API Integration
- Place API calls in the `lib/api-client.ts` file
- Use TypeScript interfaces for request/response types
- Handle errors gracefully with proper user feedback
- Implement proper loading states

### Authentication
- Wrap protected routes with the AuthProvider
- Use the useAuth hook to access authentication state
- Redirect unauthenticated users appropriately
- Handle JWT expiration and refresh automatically

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: The base URL for the backend API (e.g., http://localhost:8000)
- `NEXT_PUBLIC_BETTER_AUTH_URL`: The URL for the Better Auth server
- `BETTER_AUTH_SECRET`: The secret used for JWT signing (must match backend)
- `NEXT_PUBLIC_APP_NAME`: Display name for the application

## Troubleshooting

### Common Issues
- **Module not found**: Ensure all dependencies are installed with `npm install`
- **API connection errors**: Verify backend is running and API URL is correct
- **Auth errors**: Confirm that BETTER_AUTH_SECRET matches between frontend and backend
- **Styles not loading**: Check that Tailwind CSS is properly configured

### Development Tips
- Use the Next.js development server for hot reloading
- Check browser console for client-side errors
- Use browser dev tools to inspect network requests
- Enable React DevTools for component debugging