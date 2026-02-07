"use client";

/**
 * ChatbotTrigger - Floating button to open/close chat panel
 *
 * Features:
 * - Bottom-right positioning (fixed)
 * - Emerald accent color
 * - 56x56px size
 * - Subtle pulse animation
 * - Responsive on all screen sizes
 */

import React from 'react';

interface ChatbotTriggerProps {
  isOpen: boolean;
  onClick: () => void;
}

export default function ChatbotTrigger({ isOpen, onClick }: ChatbotTriggerProps) {
  console.log('✨ ChatbotTrigger rendering:', { isOpen });

  return (
    <button
      onClick={onClick}
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 9999,
        background: 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)',
      }}
      className={`
        w-16 h-16
        text-white
        rounded-full
        shadow-2xl hover:shadow-cyan-500/50
        transition-all duration-300
        flex items-center justify-center
        hover:scale-110
        ${!isOpen ? 'animate-pulse' : ''}
        ring-2 ring-white/20
      `}
      aria-label={isOpen ? 'Close chat' : 'Open chat'}
    >
      {isOpen ? (
        // Close icon (X)
        <svg
          className="w-7 h-7"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2.5}
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      ) : (
        // Chat icon (message bubble)
        <svg
          className="w-7 h-7"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2.5}
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
          />
        </svg>
      )}
    </button>
  );
}
