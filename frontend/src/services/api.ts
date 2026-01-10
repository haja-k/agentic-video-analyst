// gRPC service types matching proto definitions
export interface VideoMetadata {
  videoId: string;
  filename: string;
  duration: number;
  resolution: string;
  fps: number;
  fileSize: number;
}

export interface QueryRequest {
  videoId: string;
  query: string;
  sessionId?: string;
}

export interface QueryResponse {
  response: string;
  actions: string[];
  artifacts: Artifact[];
  sessionId: string;
}

export interface Artifact {
  type: string;
  content: string;
  metadata?: Record<string, any>;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
  artifacts?: Artifact[];
}

export interface ReportRequest {
  sessionId: string;
  format: 'pdf' | 'pptx';
}

export interface ReportResponse {
  filePath: string;
  success: boolean;
  message: string;
}

// API Client for backend communication
class VideoAnalysisClient {
  private baseUrl: string;
  
  constructor(baseUrl: string = 'http://localhost:8080') {
    this.baseUrl = baseUrl;
  }

  async uploadVideo(file: File): Promise<VideoMetadata> {
    const formData = new FormData();
    formData.append('video', file);

    const response = await fetch(`${this.baseUrl}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return response.json();
  }

  async queryVideo(request: QueryRequest): Promise<QueryResponse> {
    const response = await fetch(`${this.baseUrl}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Query failed: ${response.statusText}`);
    }

    return response.json();
  }

  async streamQuery(
    request: QueryRequest,
    onUpdate: (update: string) => void
  ): Promise<QueryResponse> {
    console.log('[API] Sending stream request:', request);
    const response = await fetch(`${this.baseUrl}/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Stream failed: ${response.statusText}`);
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let finalResponse: QueryResponse | null = null;

    if (reader) {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        console.log('[API] Received chunk:', chunk);
        const lines = chunk.split('\n').filter(l => l.trim());
        
        for (const line of lines) {
          try {
            const data = JSON.parse(line);
            console.log('[API] Parsed data:', data);
            if (data.update) {
              console.log('[API] Calling onUpdate with:', data.update);
              onUpdate(data.update);
            }
            if (data.response) {
              console.log('[API] Setting final response');
              finalResponse = data;
            }
          } catch (e) {
            console.error('[API] Failed to parse chunk:', e, 'Line:', line);
          }
        }
      }
    }

    console.log('[API] Stream complete, final response:', finalResponse);
    return finalResponse || {
      response: '',
      actions: [],
      artifacts: [],
      sessionId: request.sessionId || '',
    };
  }

  async getChatHistory(sessionId: string, limit: number = 50): Promise<ChatMessage[]> {
    const response = await fetch(
      `${this.baseUrl}/history?sessionId=${sessionId}&limit=${limit}`
    );

    if (!response.ok) {
      throw new Error(`History fetch failed: ${response.statusText}`);
    }

    return response.json();
  }

  async generateReport(request: ReportRequest): Promise<ReportResponse> {
    const response = await fetch(`${this.baseUrl}/report`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Report generation failed: ${response.statusText}`);
    }

    return response.json();
  }
}

export const apiClient = new VideoAnalysisClient();
