import { useState, useCallback } from 'react';
import { apiClient, QueryRequest, QueryResponse } from '../services/api';

export function useVideoQuery() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [streamingUpdate, setStreamingUpdate] = useState<string>('');

  const queryVideo = useCallback(async (
    request: QueryRequest,
    useStreaming: boolean = false
  ): Promise<QueryResponse | null> => {
    setLoading(true);
    setError(null);
    setStreamingUpdate('');

    try {
      if (useStreaming) {
        const response = await apiClient.streamQuery(request, (update) => {
          setStreamingUpdate(update);
        });
        return response;
      } else {
        const response = await apiClient.queryVideo(request);
        return response;
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
      return null;
    } finally {
      setLoading(false);
      setStreamingUpdate('');
    }
  }, []);

  return { queryVideo, loading, error, streamingUpdate };
}
