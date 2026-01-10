import { useState, useCallback } from 'react';
import { apiClient, VideoMetadata } from '../services/api';

export function useVideoUpload() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const uploadVideo = useCallback(async (file: File): Promise<VideoMetadata | null> => {
    setUploading(true);
    setProgress(0);
    setError(null);

    try {
      // Simulate progress (real progress would need backend support)
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 10, 90));
      }, 200);

      const metadata = await apiClient.uploadVideo(file);
      
      clearInterval(progressInterval);
      setProgress(100);
      
      return metadata;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Upload failed';
      setError(message);
      return null;
    } finally {
      setUploading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  }, []);

  return { uploadVideo, uploading, progress, error };
}
