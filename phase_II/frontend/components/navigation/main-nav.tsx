'use client';

import Link from 'next/link';
import { Button } from '../ui/button';
import { useAuth } from '../../hooks/use-auth';

export function MainNav() {
  const { user, signOut } = useAuth();

  return (
    <nav className="border-b">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-10">
          <Link href="/" className="text-xl font-bold">
            Todo App
          </Link>
          <div className="hidden md:flex space-x-6">
            <Link href="/dashboard" className="text-sm font-medium">
              Dashboard
            </Link>
            <Link href="/dashboard/tasks" className="text-sm font-medium">
              Tasks
            </Link>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          {user ? (
            <>
              <span className="text-sm">Welcome, {user.name || user.email}</span>
              <Button onClick={() => signOut()} variant="outline" size="sm">
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