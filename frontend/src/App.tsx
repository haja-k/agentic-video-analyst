import React, { useState } from 'react';
import { VideoUpload } from './components/VideoUpload';
import { ChatInterface } from './components/ChatInterface';
import { VideoInfo } from './components/VideoInfo';
import { useVideoQuery } from './hooks/useVideoQuery';
import { useChatHistory } from './hooks/useChatHistory';
import { apiClient, VideoMetadata, ChatMessage } from './services/api';
import { Brain } from 'lucide-react';

function App() {
  const [videoMetadata, setVideoMetadata] = useState<VideoMetadata | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [generatingReport, setGeneratingReport] = useState(false);

  const { queryVideo, loading, streamingUpdate } = useVideoQuery();
  const { messages, addMessage, clearHistory } = useChatHistory(sessionId);

  const handleVideoUploaded = (metadata: VideoMetadata) => {
    setVideoMetadata(metadata);
    // Generate new session ID
    const newSessionId = `session_${Date.now()}`;
    setSessionId(newSessionId);
    clearHistory();

    // Add system message
    addMessage({
      role: 'assistant',
      content: `Video uploaded successfully! Ask me anything about "${metadata.filename}".`,
      timestamp: Date.now(),
    });
  };

  const handleSendMessage = async (message: string) => {
    if (!videoMetadata || !sessionId) return;

    // Add user message
    addMessage({
      role: 'user',
      content: message,
      timestamp: Date.now(),
    });

    // Query backend
    const response = await queryVideo(
      {
        videoId: videoMetadata.videoId,
        query: message,
        sessionId,
      },
      true // Use streaming
    );

    if (response) {
      // Add assistant response
      addMessage({
        role: 'assistant',
        content: response.response,
        timestamp: Date.now(),
        artifacts: response.artifacts,
      });
    }
  };

  const handleGenerateReport = async (format: 'pdf' | 'pptx') => {
    if (!sessionId) return;

    setGeneratingReport(true);

    try {
      const result = await apiClient.generateReport({ sessionId, format });
      
      if (result.success) {
        addMessage({
          role: 'assistant',
          content: `${format.toUpperCase()} report generated successfully!\n\nFile: ${result.filePath}`,
          timestamp: Date.now(),
          artifacts: [
            {
              type: format === 'pdf' ? 'PDF Report' : 'PowerPoint Presentation',
              content: result.filePath,
            },
          ],
        });
      } else {
        addMessage({
          role: 'assistant',
          content: `Failed to generate report: ${result.message}`,
          timestamp: Date.now(),
        });
      }
    } catch (error) {
      addMessage({
        role: 'assistant',
        content: `Error generating report: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: Date.now(),
      });
    } finally {
      setGeneratingReport(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Video Analysis AI
              </h1>
              <p className="text-sm text-gray-600">
                Local AI-powered video understanding
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Upload & Info */}
          <div className="space-y-6">
            <VideoUpload onVideoUploaded={handleVideoUploaded} />
            <VideoInfo
              metadata={videoMetadata}
              onGenerateReport={handleGenerateReport}
              generating={generatingReport}
            />
          </div>

          {/* Right Column - Chat */}
          <div className="lg:col-span-2 h-[calc(100vh-200px)]">
            <ChatInterface
              messages={messages}
              onSendMessage={handleSendMessage}
              loading={loading}
              streamingUpdate={streamingUpdate}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-2">
        <div className="max-w-7xl mx-auto px-4">
          <p className="text-xs text-center text-gray-500">
            Powered by Llama 3.1 8B • Whisper • BLIP-2 • YOLOv8 • Running 100% locally
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
