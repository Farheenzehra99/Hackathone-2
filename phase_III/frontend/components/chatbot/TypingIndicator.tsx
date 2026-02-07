"use client";

/**
 * TypingIndicator - Animated dots while assistant is processing
 *
 * Features:
 * - Three animated dots
 * - Smooth animation
 * - Shows during isLoading state
 */

import React from 'react';

export default function TypingIndicator() {
  return (
    <div className="px-4 py-2">
      <div className="flex items-center gap-2 max-w-[75px] bg-slate-200 dark:bg-slate-700 rounded-lg px-4 py-3">
        <div className="flex gap-1">
          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
}
