import { useState, useCallback, useEffect } from 'react';
import { apiClient, ChatMessage } from '../services/api';

export function useChatHistory(sessionId: string | null) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadHistory = useCallback(async () => {
    if (!sessionId) return;
    
    setLoading(true);
    setError(null);

    try {
      const history = await apiClient.getChatHistory(sessionId);
      setMessages(history);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load history';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  const addMessage = useCallback((message: ChatMessage) => {
    setMessages(prev => [...prev, message]);
  }, []);

  const clearHistory = useCallback(() => {
    setMessages([]);
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  return { messages, loading, error, addMessage, clearHistory, loadHistory };
}
