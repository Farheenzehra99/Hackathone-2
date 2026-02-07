import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { ThemeProvider } from '@/components/providers/theme-provider';
import { AuthProvider } from '@/components/auth/auth-provider';
import ErrorBoundary from '@/components/error-boundary';
import { ErrorProvider } from '@/components/providers/error-provider';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: {
    default: 'Todo App - Productivity at Its Finest',
    template: '%s | Todo App',
  },
  description: 'A beautiful, modern todo application with premium features and delightful user experience.',
  keywords: ['todo', 'productivity', 'task management', 'organizer'],
  authors: [{ name: 'Todo App Team' }],
  creator: 'Todo App Team',
  publisher: 'Todo App Team',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://todo-app.example.com',
    title: 'Todo App - Productivity at Its Finest',
    description: 'A beautiful, modern todo application with premium features and delightful user experience.',
    siteName: 'Todo App',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Todo App - Productivity at Its Finest',
    description: 'A beautiful, modern todo application with premium features and delightful user experience.',
  },
  icons: {
    icon: '/favicon.svg',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-foreground min-h-screen`}>
        <AuthProvider>
          <ErrorBoundary>
            <ErrorProvider>
              <ThemeProvider
                attribute="class"
                defaultTheme="dark"
                enableSystem={false}
                disableTransitionOnChange
              >
                {children}
              </ThemeProvider>
            </ErrorProvider>
          </ErrorBoundary>
        </AuthProvider>
      </body>
    </html>
  );
}