'use client';

import Link from 'next/link';
import { Button } from '../ui/button';
import { useAuth } from '../../hooks/use-auth';

export function MainNav() {
  const { user, signOut } = useAuth();

  return (
    <nav className="border-b border-white/10 dark:border-gray-700/50 bg-black/30 backdrop-blur-xl">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-10">
          <Link
            href="/"
            className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent hover:from-blue-300 hover:to-cyan-300 transition-all"
          >
            Todo App
          </Link>
          <div className="hidden md:flex space-x-6">
            <Link
              href="/dashboard"
              className="text-base font-semibold text-white hover:text-cyan-400 transition-colors"
            >
              Dashboard
            </Link>
            <Link
              href="/dashboard/tasks"
              className="text-base font-semibold text-white hover:text-cyan-400 transition-colors"
            >
              Tasks
            </Link>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          {user ? (
            <>
              <span className="text-base font-semibold text-white">
                Welcome, <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">{user.name || user.email}</span>
              </span>
              <Button
                onClick={() => signOut()}
                variant="outline"
                size="sm"
                className="border-white/30 text-white hover:bg-white/10 hover:border-white/50 font-medium"
              >
                Sign Out
              </Button>
            </>
          ) : (
            <>
              <Button asChild variant="outline" size="sm">
                <Link href="/auth/sign-in">Sign In</Link>
              </Button>
              <Button asChild size="sm">
                <Link href="/auth/sign-up">Sign Up</Link>
              </Button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}