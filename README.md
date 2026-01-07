# Agentic Video Analyst

> **Local AI-powered video analysis with multi-agent orchestration**

**Status:** Environment Setup Complete | Model Download Required  
**Platform:** MacBook Air M2, 16GB RAM | **Updated:** Jan 7, 2026  
**Purpose:** Intel Senior GenAI Software Solutions Engineer Application

---

## 🎯 Overview

**Agentic Video Analyst** is a fully local AI desktop application that uses multi-agent orchestration to analyze short videos (~1 min) through natural language queries. All AI inference runs offline with no cloud dependencies.

**Key Capabilities:**
- **Agentic Architecture:** Specialized AI agents coordinated via MCP protocol
- **Speech-to-text:** Whisper-powered transcription with timestamps
- **Visual Intelligence:** Object detection, scene description, OCR, graph analysis
- **Natural Language Interface:** Chat-based video querying
- **Report Generation:** Automated PDF/PPT creation from analysis
- **Fully Local:** No internet required, all inference on-device

---

## 🏗️ Architecture

```
┌─────────────┐         gRPC          ┌──────────────┐
│   React +   │ ◄──────────────────► │   Python     │
│   Tauri     │   Streaming RPC      │   Backend    │
│  (Desktop)  │                       │   + Agents   │
└─────────────┘                       └──────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │   AI Models     │
                                    │  (Local/Metal)  │
                                    │                 │
                                    │ • Llama 3.1 8B  │
                                    │ • Whisper       │
                                    │ • BLIP-2        │
                                    └─────────────────┘
```

### Components
- **Frontend:** React + Tauri (desktop app)
- **Backend:** Python FastAPI + gRPC
- **Agents:** Transcription, Vision, Generation (MCP protocol)
- **AI Runtime:** llama.cpp with Metal acceleration
- **Models:** Llama 3.1 8B, Whisper Medium, BLIP-2

---

## 🎬 Testing Agents

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
│   ├── models/            # AI models (download needed) ⚠️
│   ├── agents/            # AI agents (transcription, vision, generation)
│   ├── mcp_servers/       # MCP protocol implementations
│   ├── tests/             # Agent test scripts ✅
│   └── main.py            # Backend entry point
├── frontend/              # React + Tauri app (TODO)
├── proto/                 # gRPC definitions ✅
├── docs/                  # Documentation
└── README.md              # This file
```

---

## ✅ What's Already Setup

- [x] Python 3.9 virtual environment with 50+ packages
- [x] llama-cpp-python with Metal acceleration (M2 GPU)
- [x] openai-whisper for speech-to-text
- [x] PyTorch 2.1.2 with MPS (Metal) support
- [x] Transformers, OpenCV, moviepy, ReportLab, python-pptx
- [x] System dependencies (ffmpeg 8.0.1, pkg-config)
- [x] Agent framework (transcription, vision, generation)
- [x] MCP server implementations (custom, Python 3.9 compatible)
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
- [ ] MCP server implementations (next)
- [ ] Main orchestrator with Llama 3.1 8B

### Phase 3: Integration 🔄 IN PROGRESS
- Environment with all dependencies
- Metal-accelerated AI libraries
- Agent & MCP framework

### Phase 2: Core Features 🔄 IN PROGRESS
- [ ] Download AI models
- [ ] Implement TranscriptionAgent with Whisper
- [ ] Implement VisionAgent with BLIP-2
- [ ] Basic chat UI
- [ ] Backend orchestration

### Phase 3: Polish 📅 PLANNED
- [ ] GenerationAgent (PDF/PPT)
- [ ] Frontend React + Tauri
- [ ] End-to-end testing
- [ ] Demo scenarios

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
- Model Context Protocol (MCP) for tool discovery
- Each agent registers capabilities
- Main orchestrator routes queries

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

---

## 📝 License & Credits

**For:** Intel Senior GenAI Software Solutions Engineer Application  
**Date:** January 2026  
**Tech Stack:** Python, React, Tauri, llama.cpp, Whisper, PyTorch  
**Platform:** macOS (M2 optimized)

---

**Current Status:** Ready to start core implementation after model download ��
