'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { TaskList } from '@/components/tasks/task-list';
import { LoadingSpinner } from '@/components/loading-spinner';
import { Navbar } from '@/components/navbar';
import { Footer } from '@/components/footer';
import ChatbotTrigger from '@/components/chatbot/ChatbotTrigger';
import ChatPanel from '@/components/chatbot/ChatPanel';
import { useChat } from '@/hooks/useChat';

export default function DashboardPage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const { isOpen, messages, isLoading, sendMessage, togglePanel } = useChat(user?.id || '');

  // Debug logging
  console.log('🔍 Dashboard Debug:', { user, loading, userId: user?.id });

  useEffect(() => {
    // If user is not authenticated and not loading, redirect to sign-in
    if (!loading && !user) {
      router.push('/auth/sign-in');
    }
  }, [user, loading, router]);

  // Show loading spinner while checking auth status
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <LoadingSpinner />
      </div>
    );
  }

  // If user is not authenticated after loading, don't render the page
  // The useEffect hook will handle the redirect
  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow container mx-auto py-8 px-4">
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">My Tasks</h1>
          </div>
          <TaskList />
        </div>
      </main>
      <Footer />

      {/* AI Chatbot */}
      <ChatbotTrigger isOpen={isOpen} onClick={togglePanel} />
      <ChatPanel
        isOpen={isOpen}
        onClose={togglePanel}
        messages={messages}
        onSend={sendMessage}
        isLoading={isLoading}
      />
    </div>
  );
}