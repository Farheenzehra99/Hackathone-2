"use client";

/**
 * useChat - Custom hook for chat state management
 *
 * Features:
 * - Manages messages, isOpen, isLoading, conversationId state
 * - sendMessage function with API call
 * - togglePanel function
 * - Error handling
 * - Auto-load conversation history on mount
 */

import { useState, useEffect } from 'react';
import { sendChatMessage, loadConversationHistory } from '@/lib/api/chat';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatState {
  isOpen: boolean;
  messages: Message[];
  conversationId: string | null;
  isLoading: boolean;
  error: string | null;
}

export function useChat(userId: string) {
  const [state, setState] = useState<ChatState>({
    isOpen: false,
    messages: [],
    conversationId: null,
    isLoading: false,
    error: null
  });

  // Load conversation history on mount
  useEffect(() => {
    if (state.isOpen && !state.messages.length) {
      loadHistory();
    }
  }, [state.isOpen]);

  const loadHistory = async () => {
    try {
      const history = await loadConversationHistory(userId);
      setState(prev => ({
        ...prev,
        messages: history.messages,
        conversationId: history.conversationId
      }));
    } catch (error) {
      console.error('Failed to load conversation history:', error);
    }
  };

  const sendMessage = async (content: string) => {
    if (!content.trim() || state.isLoading) return;

    // Add user message to state immediately
    const userMessage: Message = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: content.trim(),
      timestamp: new Date()
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null
    }));

    try {
      // Send to API
      const response = await sendChatMessage(
        userId,
        content.trim(),
        state.conversationId
      );

      // Add assistant response
      const assistantMessage: Message = {
        id: `msg-${Date.now()}`,
        role: 'assistant',
        content: response.reply,
        timestamp: new Date()
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        conversationId: response.conversationId || prev.conversationId,
        isLoading: false
      }));

    } catch (error: any) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error.message || 'Failed to send message'
      }));

      // Add error message to chat
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: `⚠ ${error.message || 'Something went wrong. Please try again.'}`,
        timestamp: new Date()
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, errorMessage]
      }));
    }
  };

  const togglePanel = () => {
    setState(prev => ({
      ...prev,
      isOpen: !prev.isOpen
    }));
  };

  const clearError = () => {
    setState(prev => ({
      ...prev,
      error: null
    }));
  };

  return {
    isOpen: state.isOpen,
    messages: state.messages,
    conversationId: state.conversationId,
    isLoading: state.isLoading,
    error: state.error,
    sendMessage,
    togglePanel,
    clearError
  };
}
