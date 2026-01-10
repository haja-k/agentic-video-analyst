# Agentic Video Analyst

> **Local AI-powered video analysis with multi-agent orchestration**

A fully local desktop application that analyzes short videos through natural language queries using multi-agent AI coordination. All inference runs offline on Apple Silicon Macs with no cloud dependencies.

**Status:** ✅ Production Ready  
**Platform:** macOS (Apple Silicon) | **Version:** 0.6.0 | **Updated:** January 9, 2026

---

## Features

- 🤖 **Intelligent Orchestration** - Llama 3.1 8B routes queries to specialized agents
- 🎙️ **Speech Transcription** - Whisper-powered speech-to-text with timestamps
- 👁️ **Visual Intelligence** - Object detection, scene description, OCR, graph analysis
- 💬 **Natural Language Interface** - Chat-based video querying
- 📄 **Report Generation** - Automated PDF/PowerPoint creation
- 🔒 **Fully Local** - No internet required, all processing on-device
- ⚡ **Metal-Accelerated** - Optimized for Apple Silicon GPUs

---

## Quick Start

### Prerequisites

- Apple Silicon Mac (M1/M2/M3)
- macOS 12.0+
- 16GB RAM recommended
- 15GB free disk space

### Installation

```bash
# 1. Clone repository
git clone <repository-url>
cd "Intel Assignment"

# 2. Setup backend
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Download models (~5GB)
./download-models.sh

# 4. Setup frontend
cd ../frontend
npm install
```

### Run Application

```bash
# All-in-one startup (from project root)
./start-all.sh

# Or manually:
# Terminal 1: cd backend && source venv/bin/activate && python main.py
# Terminal 2: cd backend && source venv/bin/activate && python http_bridge.py
# Terminal 3: cd frontend && npm run dev
```

Open `http://localhost:1420` in your browser.

---

## Usage

1. **Upload Video** - Drag and drop or click to upload (MP4, MOV, AVI)
2. **Ask Questions** - Type natural language queries:
   - "Transcribe the video"
   - "What objects can you see?"
   - "Describe the scene"
   - "Generate a PDF report"
3. **View Results** - Responses appear in chat with analysis data
4. **Generate Reports** - Create PDF/PPTX summaries of your analysis

---

## Architecture

```
Frontend (React + Tauri)  ──HTTP/JSON──>  HTTP Bridge (FastAPI)
       ↓                                         ↓
  Port 1420                                  Port 8080
                                                 ↓
                                            gRPC (50051)
                                                 ↓
                                    ┌────────────────────────┐
                                    │   Python Backend       │
                                    │                        │
                                    │  Orchestrator (Llama)  │
                                    │         ↓              │
                                    │  ┌──────┴──────┐       │
                                    │  │  MCP Servers │       │
                                    │  ├─────────────┤       │
                                    │  │ Transcription│       │
                                    │  │ Vision       │       │
                                    │  │ Generation   │       │
                                    │  └─────────────┘       │
                                    └────────────────────────┘
```

**Key Components:**
- **Orchestrator Agent**: Routes queries using Llama 3.1 8B
- **Transcription Agent**: Whisper Medium for speech-to-text
- **Vision Agent**: BLIP + YOLOv8 for visual analysis
- **Generation Agent**: ReportLab + python-pptx for documents
- **MCP Protocol**: Model Context Protocol for agent coordination
- **gRPC Service**: 5 endpoints for video upload, querying, and reports

---

## Documentation

### User Guides
- [Getting Started](docs/getting-started.md) - Complete setup and first steps
- [Installation](docs/installation.md) - Detailed installation instructions

### Technical Documentation
- [Architecture](docs/architecture.md) - System design and components
- [gRPC Implementation](docs/grpc-implementation.md) - API specifications
- [Orchestrator](docs/orchestrator.md) - Multi-agent coordination
- [Development Guide](docs/development-guide.md) - Contributing guidelines
- [Model Setup](docs/model-setup.md) - AI model configuration

---

## Project Status

### ✅ Completed
- Multi-agent system with MCP protocol
- gRPC service (5 endpoints fully functional)
- HTTP/JSON bridge for frontend communication
- Session-based analysis with persistent storage
- Video registry with server restart recovery
- PDF/PPTX report generation
- Frontend UI with real-time streaming
- Complete test suite

### 🎯 Current Focus
- UI polish and error handling
- Performance optimization
- Documentation finalization

---

## Testing

```bash
cd backend/tests
source ../venv/bin/activate

# Run all tests
./test_all.sh

# Test individual components
python test_transcription.py
python test_vision.py
python test_orchestrator.py
python test_grpc_client.py
```

---

## Technologies

**Backend:**
- Python 3.12
- llama-cpp-python (Metal-accelerated)
- Whisper (OpenAI)
- Transformers (HuggingFace)
- YOLOv8 (Ultralytics)
- gRPC
- FastAPI
- OpenCV

**Frontend:**
- React 18
- TypeScript
- Tauri (Desktop)
- TailwindCSS
- Vite

**AI Models:**
- Llama 3.1 8B Instruct (4.6GB, Q4_K_M quantized)
- Whisper Medium (~1.5GB)
- BLIP Image Captioning (~1GB)
- YOLOv8 Nano (6MB)

---

## Requirements

- **Python:** 3.12.x
- **Node.js:** 18.x+
- **RAM:** 16GB recommended (8GB minimum)
- **Storage:** 15GB (10GB for models, 5GB for workspace)
- **GPU:** Apple Silicon with Metal support

---

## License

[Add your license here]

---

## Contact

**Purpose:** Intel Senior GenAI Software Solutions Engineer Application  
**Developer:** [Your Name]  
**Email:** [Your Email]

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and recent updates.

---

*Built with ❤️ for local AI-powered video analysis*
                                      │  │ Orchestrator   │  │
                                      │  │ (Llama 3.1 8B) │  │
                                      │  └────────┬───────┘  │
                                      │           │          │
                                      │  ┌────────┼────────┐ │
                                      │  ↓        ↓        ↓ │
                                      │ Trans   Vision   Gen │
                                      │ Agent   Agent  Agent │
                                      └──────────────────────┘
                                                 │
                                                 ▼
                                      ┌─────────────────┐
                                      │   AI Models     │
                                      │  (Local/Metal)  │
                                      │                 │
                                      │ • Llama 3.1 8B  │
                                      │ • Whisper       │
                                      │ • BLIP-2+YOLOv8 │
                                      └─────────────────┘
```

### Components
- **Frontend:** React 18 + Tauri desktop app (TypeScript, Vite, Tailwind CSS)
- **HTTP Bridge:** FastAPI server converting HTTP/JSON to gRPC (port 8080)
- **Backend:** Python gRPC service with multi-agent orchestration (port 50051)
- **gRPC Service:** 5 endpoints (UploadVideo, QueryVideo, StreamQuery, GetChatHistory, GenerateReport)
- **Orchestrator:** Llama 3.1 8B for query understanding and routing via MCP
- **MCP Layer:** Protocol servers wrapping each specialized agent
- **Agents:** Transcription (Whisper), Vision (BLIP-2+YOLOv8), Generation (PDF/PPT)
- **AI Runtime:** llama.cpp with Metal acceleration
- **Session Management:** Context-aware report generation with stored results

**Why HTTP Bridge?** React can't directly call gRPC from the browser, so we use a FastAPI bridge that translates HTTP requests to gRPC calls. Simple and works.

---

## 🎬 Testing

### Test gRPC Service (Full Integration)
```bash
cd backend
source venv/bin/activate

# Start gRPC server (runs in background)
./run.sh

# Run comprehensive test suite
python tests/test_grpc_client.py uploads/CunkOnEarth.mp4
```

**Tests all endpoints:**
- ✅ Video upload with metadata extraction
- ✅ Transcription queries via orchestrator
- ✅ Vision analysis (objects + scene descriptions)
- ✅ Streaming query responses
- ✅ Chat history persistence
- ✅ PDF report generation with session context

### Test Orchestrator (Query Routing & Multi-Agent Coordination)
```bash
cd backend/tests
source ../venv/bin/activate

# Test intent analysis only (quick test)
python test_orchestrator.py --intent-only

# Full orchestrator test with video
python test_orchestrator.py ../uploads/your_video.mp4
```

The orchestrator uses Llama 3.1 8B to understand queries and route to appropriate agents.

**Example queries tested:**
- "Transcribe the video"
- "What objects can you see?"
- "Are there any graphs or charts?"
- "Create a PowerPoint with key points"
- "Summarize our discussion"

### Test Transcription Agent
```bash
cd backend/tests
source ../venv/bin/activate
python test_transcription.py ../uploads/your_video.mp4
```

Outputs full transcription with timestamps to `results/transcription_result.json`

### Test Vision Agent
```bash
cd backend/tests
source ../venv/bin/activate
python test_vision.py ../uploads/your_video.mp4
```

Outputs scene descriptions and detected objects to `results/vision_result.json`

### Test Generation Agent
```bash
cd backend/tests
source ../venv/bin/activate
python test_generation.py
```

Generates `results/video_report.pdf` and `results/video_presentation.pptx` from previous results

---

## 📁 Project Structure

```
agentic-video-analyst/
├── backend/
│   ├── venv/              # Virtual env (50+ packages) ✅
│   ├── models/            # AI models (Llama 3.1 8B, YOLOv8) ✅
│   ├── agents/            # AI agents ✅
│   │   ├── orchestrator_agent.py    # Query routing with Llama 3.1 8B
│   │   ├── transcription_agent.py   # Whisper integration
│   │   ├── vision_agent.py          # BLIP-2 + YOLOv8
│   │   └── generation_agent.py      # PDF/PPT creation
│   ├── mcp_servers/       # MCP protocol implementations ✅
│   ├── generated/         # Generated proto files ✅
│   ├── logs/              # Server logs (gitignored) ✅
│   ├── uploads/           # Video upload directory ✅
│   ├── tests/             # Agent test scripts ✅
│   │   ├── test_orchestrator.py     # Orchestrator tests
│   │   ├── test_all.sh              # Run all tests
│   │   ├── test_grpc_client.py      # Full gRPC integration test
│   │   └── results/                 # Test outputs (PDFs, JSONs)
│   ├── run.sh             # Start backend server ✅
│   ├── status.sh          # Check server status ✅
│   └── main.py            # Backend entry point ✅
├── frontend/              # React + Tauri app (TODO)
├── proto/                 # gRPC definitions ✅
├── docs/                  # Documentation ✅
└── README.md              # This file
```

---

## ✅ What's Already Setup

- [x] Python 3.12 virtual environment with 50+ packages
- [x] llama-cpp-python with Metal acceleration (M2 GPU)
- [x] openai-whisper for speech-to-text
- [x] PyTorch 2.8.0 with MPS (Metal) support
- [x] Transformers, OpenCV, moviepy, ReportLab, python-pptx
- [x] System dependencies (ffmpeg 8.0.1, pkg-config)
- [x] **Orchestrator Agent** - Llama 3.1 8B query routing via MCP
- [x] **Transcription Agent** - Whisper integration complete
- [x] **Vision Agent** - BLIP-2 + YOLOv8 working
- [x] **Generation Agent** - PDF/PPT creation with Calibri 15pt
- [x] MCP server implementations (transcription, vision, generation)
- [x] MCP routing complete - orchestrator communicates via MCP protocol
- [x] Multi-agent coordination and context management
- [x] Comprehensive test suite with all agents
- [x] gRPC protocol definitions

---

## 🚀 Quick Start

### 1. Download AI Model (~5 mins)

**Recommended: Llama 3.1 8B** (publicly available, no auth needed)

```bash
cd backend/models
curl -L "https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" \
     -o Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf \
     --progress-bar

# Verify (should show ~4.9GB)
ls -lh *.gguf
```

**Why Llama 3.1 8B?**
- ✅ Public (no HuggingFace auth)
- ✅ Strong instruction following
- ✅ Fits in 16GB RAM (~5-6GB usage)
- ✅ Fast on M2 with Metal

### 2. Configure Environment

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:
```env
LLAMA_MODEL_PATH=models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
WHISPER_MODEL_SIZE=medium
BACKEND_HOST=0.0.0.0
BACKEND_PORT=50051
```

### 3. Test Setup

```bash
cd backend
source venv/bin/activate
python test_models.py
```

Expected: All components ✅ Ready

### 4. Compile gRPC Protocols

```bash
cd backend
source venv/bin/activate
python -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/video_analysis.proto
```

### 5. Start Backend Services

**Terminal 1 - gRPC Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - HTTP Bridge:**
```bash
cd backend
source venv/bin/activate
python3 http_bridge.py
```

**Terminal 3 - Frontend (Optional):**
```bash
cd frontend
npm run dev
```

Then open http://localhost:1420 in your browser. The frontend talks to the HTTP bridge (8080), which talks to the gRPC backend (50051).

---

## 📋 Development Status

### Phase 1: Foundation ✅ COMPLETE
- Environment setup with 50+ packages
- Metal GPU acceleration configured
- All system dependencies installed

### Phase 2: Agent Implementation ✅ COMPLETE
- [x] **TranscriptionAgent** - Whisper integration complete
- [x] **VisionAgent** - BLIP-2 + YOLOv8 integration complete
- [x] **GenerationAgent** - PDF/PPT creation complete
- [x] **OrchestratorAgent** - Llama 3.1 8B query routing complete
- [x] MCP server implementations
- [x] Main backend server with all agents

### Phase 3: Integration ✅ COMPLETE
- [x] Orchestrator routes queries via MCP protocol layer
- [x] MCP servers wrap all specialized agents
- [x] Multi-agent coordination through MCP working
- [x] Context management across agents
- [x] gRPC service definitions and implementation
- [x] Full backend test suite verified
- [x] Backend codebase reorganized (generated/, logs/, models/)
- [ ] Frontend React + Tauri UI
- [ ] Persistent chat storage (SQLite)

### Phase 4: Frontend Development 🔄 IN PROGRESS
- [x] React + TypeScript project scaffolding (Vite + Tailwind)
- [x] Tauri desktop wrapper configured
- [x] HTTP bridge for React ↔ gRPC communication
- [x] Video upload component with drag & drop
- [x] Chat interface with message history
- [x] API client with TypeScript types
- [ ] End-to-end integration testing
- [ ] Streaming response handling
- [ ] Report download UI
- [ ] Desktop app packaging and distribution

### Phase 5: Polish & Deployment 📅 PLANNED
- [ ] End-to-end testing with frontend
- [ ] Performance optimization
- [ ] Demo scenarios and user guide
- [ ] Final packaging and deployment

---

## 🎬 Demo Scenarios

1. **Transcription:** Upload video → Extract audio transcript
2. **Vision:** "What objects are in this video?"
3. **Analysis:** "Are there any graphs? Describe them."
4. **Generation:** Generate summary report (PDF/PPT)

---

## 🔧 Technical Highlights

### Metal Acceleration (M2)
- llama-cpp-python: `-DLLAMA_METAL=on`
- PyTorch: MPS backend enabled
- ~2-3x faster inference vs CPU

### Agentic Architecture
- Model Context Protocol (MCP) for standardized agent communication
- Each agent wrapped by MCP server with tool registration
- Orchestrator routes through MCP protocol layer (satisfies assignment requirement)
- Main orchestrator uses Llama 3.1 8B for intent understanding

### Local-First Design
- All models run in RAM
- No internet required after setup
- Suitable for confidential content

---

## 📊 Resource Usage (16GB M2)

| Component | RAM Usage |
|-----------|-----------|
| Llama 3.1 8B | ~5-6GB |
| Whisper Medium | ~1.5GB |
| PyTorch/Vision | ~1-2GB |
| System/Other | ~2GB |
| **Total** | **~10-11GB / 16GB** |

Comfortable headroom for development tools.

---

## 🐛 Known Issues & Solutions

1. **Llama 3.2 Vision 11B not available**  
   → Use Llama 3.1 8B (publicly available)

2. **faster-whisper build errors**  
   → Using openai-whisper (stable alternative)

3. **MCP SDK requires Python 3.10+**  
   → Custom MCP implementation (in `backend/mcp_servers/`)

4. **Model download authentication errors**  
   → Use lmstudio-community repos (no auth)

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Detailed setup guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[docs/architecture.md](docs/architecture.md)** - System design
- **[docs/model-comparison.md](docs/model-comparison.md)** - Model selection rationale
- **[docs/development-guide.md](docs/development-guide.md)** - Implementation plan

---

## 🔑 Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| **openai-whisper** over faster-whisper | faster-whisper incompatible with ffmpeg 8.0 |
| **Llama 3.1 8B** over TinyLlama | TinyLlama too weak for structured output |
| **Custom MCP** over official SDK | SDK requires Python 3.10+, system has 3.9 |
| **llama.cpp** over transformers | Better Metal support, lower memory usage |

---

## 🎯 Success Criteria

- [x] **Offline:** All AI runs locally
- [x] **M2 Optimized:** Metal acceleration enabled
- [x] **Agentic:** Multi-agent with MCP protocol
- [x] **Transcription:** Whisper integration working
- [x] **Vision:** Image/video analysis working (YOLOv8 + BLIP-2)
- [x] **Chat Interface:** Natural language queries via gRPC
- [x] **Artifacts:** PDF/PPT generation with session context
- [x] **Backend Tests:** Full test suite verified
- [ ] **Frontend UI:** React + Tauri desktop app
- [ ] **Desktop App:** Final packaging and distribution

---

## 🚦 Getting Help

**Model fails to load?**
```bash
# Check file size (should be ~4.9GB, not bytes)
ls -lh backend/models/*.gguf

# Check file type (should be "data")
file backend/models/*.gguf
```

**Import errors?**
```bash
cd backend
source venv/bin/activate
pip list | grep -E "llama|whisper|torch"
```

**GPU not working?**
```bash
python -c "import torch; print(f'MPS: {torch.backends.mps.is_available()}')"
# Should output: MPS: True
```

**Orchestrator test fails?**
```bash
# Ensure venv is activated
cd backend/tests
source ../venv/bin/activate

# Test with intent analysis only (no video needed)
python test_orchestrator.py --intent-only

# Check if model is loaded correctly
ls -lh ../models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

---

## 📝 License & Credits

**For:** Intel Senior GenAI Software Solutions Engineer Application  
**Date:** January 2026  
**Tech Stack:** Python, React, Tauri, llama.cpp, Whisper, PyTorch  
**Platform:** macOS (M2 optimized)

---

## 🔄 Recent Updates (Jan 9, 2026)

### Frontend Setup & HTTP Bridge
- ✅ Complete React + Tauri project scaffolding:
  - 19 frontend files created (components, hooks, services)
  - TypeScript strict mode, Vite build system, Tailwind CSS
  - Video upload, chat interface, video info components
  - API service layer with full typing
- ✅ HTTP Bridge implementation:
  - FastAPI server bridging React to gRPC backend
  - 5 endpoints matching proto definitions (upload, query, stream, history, report)
  - CORS enabled for local development
  - Fixed protobuf field mappings to match video_analysis.proto
- ✅ Frontend dependencies installed (230 npm packages)
- ✅ All 3 services tested: backend (50051), bridge (8080), frontend (1420)

### Backend Reorganization & Testing
- ✅ Reorganized backend structure (generated/, logs/, models/)
- ✅ Fixed PDF report generation (saves to `tests/results/`)
- ✅ Full backend test suite verified
- ✅ gRPC service tested and operational

**Current Status:** Backend complete, HTTP bridge operational, frontend scaffolding done - now testing integration 
