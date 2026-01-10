# Video Analysis AI - Frontend

React + Tauri desktop application for local AI video analysis.

## Features

- 🎥 **Video Upload** - Drag & drop or click to upload video files
- 💬 **Chat Interface** - Natural language queries about your videos
- 🔍 **AI Analysis** - Transcription, object detection, scene description
- 📄 **Report Generation** - Create PDF and PowerPoint reports
- 💾 **Session Management** - Chat history persists across queries
- 🚀 **100% Local** - All processing happens on your device

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tauri** - Desktop app wrapper (Rust + WebView)
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## Prerequisites

- Node.js 18+ and npm
- Rust (for Tauri)
- Backend server running on port 50051

## Installation

```bash
# Install dependencies
npm install

# Install Tauri CLI (if not already installed)
cargo install tauri-cli
```

## Development

```bash
# Start development server (Vite only)
npm run dev

# Start Tauri development (full desktop app)
npm run tauri:dev
```

The development server runs on `http://localhost:1420`.

## Building

```bash
# Build for production
npm run build

# Build Tauri app
npm run tauri:build
```

The built application will be in `src-tauri/target/release/`.

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ChatInterface.tsx    # Chat UI
│   │   ├── VideoUpload.tsx      # Video upload component
│   │   └── VideoInfo.tsx        # Video metadata display
│   ├── hooks/               # Custom React hooks
│   │   ├── useChatHistory.ts    # Chat history management
│   │   ├── useVideoQuery.ts     # Query handling
│   │   └── useVideoUpload.ts    # Upload handling
│   ├── services/            # API services
│   │   └── api.ts               # Backend communication
│   ├── App.tsx              # Main application
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
├── src-tauri/               # Tauri (Rust) configuration
│   ├── src/
│   │   └── main.rs          # Tauri main
│   ├── Cargo.toml           # Rust dependencies
│   └── tauri.conf.json      # Tauri config
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## API Communication

The frontend communicates with the Python backend via HTTP/JSON on port 50051:

- `POST /upload` - Upload video file
- `POST /query` - Send query to backend
- `POST /stream` - Stream query with real-time updates
- `GET /history` - Get chat history for session
- `POST /report` - Generate PDF/PPTX report

## Usage

1. **Start Backend**: Ensure the Python backend is running (`cd backend && ./run.sh`)
2. **Start Frontend**: Run `npm run tauri:dev`
3. **Upload Video**: Click or drag video file to upload area
4. **Ask Questions**: Type queries in the chat interface
5. **Generate Reports**: Click PDF or PowerPoint buttons in the video info panel

## Example Queries

- "Transcribe the video"
- "What objects can you see?"
- "Describe what's happening in the video"
- "Are there any graphs or charts shown?"
- "Generate a PDF report"
- "Create a PowerPoint presentation"
- "Summarize our discussion so far"

## Troubleshooting

### Backend Connection Issues

If you see connection errors:
1. Verify backend is running: `cd backend && ./status.sh`
2. Check backend logs: `tail -f backend/logs/server.log`
3. Test connection: `curl http://localhost:50051/health`

### Tauri Build Errors

If Tauri fails to build:
1. Ensure Rust is installed: `rustc --version`
2. Update Rust: `rustup update`
3. Clean build: `cd src-tauri && cargo clean`

### Video Upload Issues

Supported formats: MP4, MOV, AVI, WebM
Max file size: 100MB (configurable in backend)

## License

Intel Assignment - 2026
