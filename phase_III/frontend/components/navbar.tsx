'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '../components/ui/button';
import { motion } from 'framer-motion';

export function Navbar() {
  const pathname = usePathname();

  return (
    <motion.header
      className="sticky top-0 z-50 backdrop-blur-xl bg-black/40 border-b border-white/10 dark:border-gray-700/50 shadow-xl"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link
          href="/"
          className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent hover:from-blue-300 hover:to-cyan-300 transition-all"
        >
          Todo App
        </Link>

        <nav className="flex items-center gap-4">
          {pathname !== '/' && (
            <Button
              asChild
              variant="ghost"
              className="text-white font-semibold hover:bg-white/10 hover:text-cyan-400 transition-all duration-300"
            >
              <Link href="/">Home</Link>
            </Button>
          )}

          {pathname !== '/dashboard' && (
            <Button
              asChild
              variant="ghost"
              className="text-white font-semibold hover:bg-white/10 hover:text-cyan-400 transition-all duration-300"
            >
              <Link href="/dashboard">Dashboard</Link>
            </Button>
          )}

          <Button
            onClick={() => window.location.href = '/dashboard/tasks'}
            className="bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-semibold px-5 py-2 rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            Add Task
          </Button>
        </nav>
      </div>
    </motion.header>
  );
}