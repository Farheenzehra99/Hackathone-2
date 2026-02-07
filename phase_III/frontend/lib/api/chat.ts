/**
 * Chat API Client - handles communication with chat endpoint
 *
 * Features:
 * - POST to /api/{user_id}/chat with JWT header
 * - Handle response/errors
 * - Load conversation history
 * - Type-safe API calls
 */

import { Message } from '@/hooks/useChat';

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_BASE ||
  '';

interface ChatResponse {
  reply: string;
  conversationId: string | null;
}

interface ConversationHistory {
  conversationId: string | null;
  messages: Message[];
}

/**
 * Get JWT token from localStorage (Better Auth)
 */
function getAuthToken(): string {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('accessToken') || '';
  }
  return '';
}

/**
 * Send chat message to backend
 */
export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId?: string | null
): Promise<ChatResponse> {
  try {
    const token = getAuthToken();

    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        user_id: userId,
        message,
        conversation_id: conversationId
      })
    });

    const rawBody = await response.text();
    console.log('Chat raw response:', rawBody);

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized - please log in again');
      }
      if (response.status === 403) {
        throw new Error('You can only access your own conversations');
      }
      if (response.status === 429) {
        throw new Error('Too many messages. Please wait a moment.');
      }

      let errorDetail = 'Failed to send message';
      try {
        const errorData = JSON.parse(rawBody);
        errorDetail = errorData.detail || errorDetail;
      } catch {
        // Keep default error detail for non-JSON responses
      }
      throw new Error(errorDetail);
    }

    let data: any;
    try {
      data = JSON.parse(rawBody);
    } catch {
      throw new Error('Invalid JSON response from server');
    }

    if (typeof data.reply !== 'string') {
      throw new Error('Invalid response contract: missing reply');
    }

    const headerConversationId = response.headers.get('x-conversation-id');
    return {
      reply: data.reply,
      conversationId: headerConversationId
    };

  } catch (error: any) {
    if (error.message) {
      throw error;
    }
    throw new Error('Unexpected error while handling response');
  }
}

/**
 * Load conversation history (last 50 messages)
 */
export async function loadConversationHistory(
  userId: string
): Promise<ConversationHistory> {
  try {
    const token = getAuthToken();

    // TODO: Implement actual history endpoint when backend supports it
    // For now, return empty history
    return {
      conversationId: null,
      messages: []
    };

    /* Future implementation:
    const response = await fetch(
      `${API_BASE_URL}/api/${userId}/conversations/history?limit=50`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );

    if (!response.ok) {
      throw new Error('Failed to load conversation history');
    }

    const data = await response.json();
    return {
      conversationId: data.conversation_id,
      messages: data.messages.map((msg: any) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        timestamp: new Date(msg.created_at)
      }))
    };
    */

  } catch (error) {
    console.error('Error loading conversation history:', error);
    return {
      conversationId: null,
      messages: []
    };
  }
}
