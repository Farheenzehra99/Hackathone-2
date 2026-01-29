'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '../components/ui/button';
import { motion } from 'framer-motion';

export function Navbar() {
  const pathname = usePathname();

  return (
    <motion.header
      className="sticky top-0 z-50 backdrop-blur-xl bg-white/10 dark:bg-black/30 border border-white/20 dark:border-gray-700/50 p-4 shadow-xl"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="container mx-auto flex items-center justify-between">
        <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
          Todo App
        </Link>

        <nav className="flex items-center gap-4">
          {pathname !== '/' && (
            <Button
              asChild
              variant="ghost"
              className="text-white hover:bg-white/10 transition-all duration-300"
            >
              <Link href="/">Home</Link>
            </Button>
          )}

          {pathname !== '/dashboard' && (
            <Button
              asChild
              variant="ghost"
              className="text-white hover:bg-white/10 transition-all duration-300"
            >
              <Link href="/dashboard">Dashboard</Link>
            </Button>
          )}

          <Button
            onClick={() => window.location.href = '/dashboard/tasks'}
            className="bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white px-4 py-2 rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            Add Task
          </Button>
        </nav>
      </div>
    </motion.header>
  );
}