"use client";

/**
 * MessageBubble - Individual message display component
 *
 * Features:
 * - Role-based styling (user: right/indigo, assistant: left/slate)
 * - Timestamp display
 * - Markdown support for bold and links
 * - Responsive layout
 */

import React from 'react';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function MessageBubble({ role, content, timestamp }: MessageBubbleProps) {
  const isUser = role === 'user';

  // Format timestamp
  const formattedTime = timestamp.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  });

  // Simple markdown parsing for **bold** and [links](url)
  const parseMarkdown = (text: string) => {
    // Bold: **text**
    let parsed = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Links: [text](url)
    parsed = parsed.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="underline">$1</a>');

    return parsed;
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[75%] ${isUser ? 'order-2' : 'order-1'}`}>
        <div
          className={`
            rounded-lg px-4 py-2
            ${isUser
              ? 'bg-indigo-500 text-white'
              : 'bg-slate-200 dark:bg-slate-700 text-gray-900 dark:text-gray-100'
            }
          `}
        >
          <div
            className="text-sm break-words"
            dangerouslySetInnerHTML={{ __html: parseMarkdown(content) }}
          />
        </div>
        <div
          className={`
            text-xs text-gray-500 dark:text-gray-400 mt-1
            ${isUser ? 'text-right' : 'text-left'}
          `}
        >
          {formattedTime}
        </div>
      </div>
    </div>
  );
}
