"use client";

/**
 * ChatPanel - Main chat interface container
 *
 * Features:
 * - Slide-in animation from bottom-right
 * - Glassmorphic design with backdrop blur
 * - 400px × 600px on desktop, full-width on mobile
 * - Theme-aware (dark/light mode)
 * - Integrates MessageList and ChatInput
 * - Close button
 * - Error boundary for graceful error handling
 */

import React, { Component, ErrorInfo, ReactNode } from 'react';
import MessageList, { Message } from './MessageList';
import ChatInput from './ChatInput';
import TypingIndicator from './TypingIndicator';

interface ChatPanelProps {
  isOpen: boolean;
  onClose: () => void;
  messages: Message[];
  onSend: (message: string) => void;
  isLoading: boolean;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

class ChatErrorBoundary extends Component<
  { children: ReactNode },
  ErrorBoundaryState
> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Chat error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-4 text-center">
          <p className="text-red-500 dark:text-red-400 mb-4">
            ⚠ Something went wrong. Please try again.
          </p>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-colors"
          >
            Reset Chat
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default function ChatPanel({
  isOpen,
  onClose,
  messages,
  onSend,
  isLoading
}: ChatPanelProps) {
  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/20 backdrop-blur-sm md:hidden"
        style={{ zIndex: 9998 }}
        onClick={onClose}
      />

      {/* Chat Panel */}
      <div
        className={`
          fixed
          bottom-6 right-6
          w-full max-w-md
          h-[600px]
          bg-white/95 dark:bg-gray-900/95
          backdrop-blur-xl
          rounded-2xl
          shadow-2xl
          border border-gray-200/50 dark:border-gray-700/50
          flex flex-col
          animate-in slide-in-from-bottom-4 duration-300 ease-out
          md:w-[400px]
          max-md:bottom-0 max-md:right-0 max-md:left-0 max-md:max-w-full
          max-md:rounded-t-2xl max-md:rounded-b-none max-md:h-[70vh]
          max-sm:h-[80vh]
        `}
        style={{
          backdropFilter: 'blur(20px)',
          zIndex: 9999,
          WebkitBackdropFilter: 'blur(20px)'
        }}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
            <h3 className="font-semibold text-gray-900 dark:text-gray-100">
              AI Assistant
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            aria-label="Close chat"
          >
            <svg
              className="w-5 h-5 text-gray-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Messages with Error Boundary */}
        <ChatErrorBoundary>
          <MessageList messages={messages} />

          {/* Typing Indicator */}
          {isLoading && <TypingIndicator />}

          {/* Input */}
          <ChatInput
            onSend={onSend}
            disabled={isLoading}
            placeholder="Type your message..."
          />
        </ChatErrorBoundary>
      </div>
    </>
  );
}
