# Agentic Video Analyst

> **Local AI-powered video analysis with multi-agent orchestration**

**Status:** Phase 5 Complete - gRPC Service Live | Ready for Frontend Integration  
**Platform:** MacBook Air M2, 16GB RAM | **Updated:** Jan 9, 2026  
**Purpose:** Intel Senior GenAI Software Solutions Engineer Application

---

## 🎯 Overview

**Agentic Video Analyst** is a fully local AI desktop application that uses multi-agent orchestration to analyze short videos (~1 min) through natural language queries. All AI inference runs offline with no cloud dependencies.

**Key Capabilities:**
- **Intelligent Orchestration:** Llama 3.1 8B routes queries to specialized agents
- **Speech-to-text:** Whisper-powered transcription with timestamps
- **Visual Intelligence:** Object detection, scene description, OCR, graph analysis
- **Natural Language Interface:** Chat-based video querying
- **Report Generation:** Automated PDF/PPT creation from analysis
- **Fully Local:** No internet required, all inference on-device

**Current Status:**
- ✅ All agents implemented and tested
- ✅ Orchestrator routing queries via MCP protocol
- ✅ Multi-agent coordination through MCP servers
- ✅ gRPC service with 5 endpoints fully functional
- ✅ PDF/PPTX report generation with session context
- ⏳ Frontend UI in development (Phase 6)

---

## 🏗️ Architecture

```
┌─────────────┐         gRPC          ┌──────────────────────┐
│   React +   │ ◄──────────────────► │   Python Backend     │
│   Tauri     │   Streaming RPC      │                      │
│  (Desktop)  │                       │  ┌────────────────┐  │
└─────────────┘                       │  │ Orchestrator   │  │
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
- **Frontend:** React + Tauri (desktop app) - In Development
- **Backend:** Python with multi-agent orchestration
- **gRPC Service:** 5 endpoints (UploadVideo, QueryVideo, StreamQuery, GetChatHistory, GenerateReport)
- **Orchestrator:** Llama 3.1 8B for query understanding and routing via MCP
- **MCP Layer:** Protocol servers wrapping each specialized agent
- **Agents:** Transcription (Whisper), Vision (BLIP-2+YOLOv8), Generation (PDF/PPT)
- **MCP Protocol:** Standardized tool interface for agent coordination
- **AI Runtime:** llama.cpp with Metal acceleration
- **Session Management:** Context-aware report generation with stored results

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
│   ├── models/            # AI models (Llama 3.1 8B downloaded) ✅
│   ├── agents/            # AI agents ✅
│   │   ├── orchestrator_agent.py    # Query routing with Llama 3.1 8B
│   │   ├── transcription_agent.py   # Whisper integration
│   │   ├── vision_agent.py          # BLIP-2 + YOLOv8
│   │   └── generation_agent.py      # PDF/PPT creation
│   ├── mcp_servers/       # MCP protocol implementations ✅
│   ├── tests/             # Agent test scripts ✅
│   │   ├── test_orchestrator.py     # Orchestrator tests
│   │   ├── test_all.sh              # Run all tests
│   │   └── results/                 # Test outputs
│   ├── run.sh             # Start backend server ✅
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

### 5. Start Backend (Development)

```bash
cd backend
source venv/bin/activate
python main.py
```

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

### Phase 3: Integration 🔄 IN PROGRESS
- [x] Orchestrator routes queries via MCP protocol layer
- [x] MCP servers wrap all specialized agents
- [x] Multi-agent coordination through MCP working
- [x] Context management across agents
- [ ] gRPC service definitions
- [ ] Frontend React + Tauri UI
- [ ] Persistent chat storage

### Phase 4: Polish 📅 PLANNED
- [ ] Complete frontend UI implementation
- [ ] End-to-end gRPC testing
- [ ] Desktop app packaging (Tauri)
- [ ] Demo scenarios and documentation

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
- [ ] **Agentic:** Multi-agent with MCP (structure ready)
- [ ] **Transcription:** Whisper integration working
- [ ] **Vision:** Image/video analysis working
- [ ] **Chat Interface:** Natural language queries
- [ ] **Artifacts:** PDF/PPT generation
- [ ] **Desktop App:** Tauri packaging

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

**Current Status:** Ready to start core implementation after model download 
