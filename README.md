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
- 💬 **Natural Language Interface** - Chat-based video querying with streaming responses
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

### Installation & Setup

```bash
# Clone and setup (all-in-one)
git clone <repository-url>
./setup-complete.sh  # Installs backend + frontend + models
```

### Run Application

```bash
# Start all services
./start-all.sh
```

Open `http://localhost:1420` in your browser.

---

## Usage

1. **Upload Video** - Drag and drop or click to upload (MP4, MOV, AVI)
2. **Ask Questions** - Type natural language queries:
   - "Transcribe the video"
   - "What objects can you see?"
   - "Generate a PDF report"
3. **View Results** - Real-time streaming responses with analysis data
4. **Download Reports** - Save PDF/PPTX summaries of your analysis

---

## Architecture

```
Frontend (React + Tauri)  ──HTTP/JSON──>  HTTP Bridge (FastAPI)  ──gRPC──>  Backend
   Port 1420                               Port 8080                Port 50051
                                                                         │
                                                            Orchestrator (Llama 3.1)
                                                                         │
                                                              ┌──────────┴──────────┐
                                                              │    MCP Servers      │
                                                              ├────────────────────┤
                                                              │ Transcription      │
                                                              │ Vision             │
                                                              │ Generation         │
                                                              └────────────────────┘
```

**Key Components:**
- **Orchestrator**: Routes queries using Llama 3.1 8B via MCP protocol
- **Transcription**: Whisper Medium for speech-to-text with timestamps
- **Vision**: BLIP + YOLOv8 for object detection and scene analysis
- **Generation**: ReportLab + python-pptx for PDF/PowerPoint creation
- **HTTP Bridge**: FastAPI gateway enabling frontend communication with gRPC backend
- **Video Registry**: Persistent storage with session recovery across restarts

---

## Documentation

- [Getting Started](docs/getting-started.md) - Complete setup and first steps
- [Installation](docs/installation.md) - Detailed installation with troubleshooting
- [Architecture](docs/architecture.md) - System design and components
- [gRPC Implementation](docs/grpc-implementation.md) - API specifications
- [Development Guide](docs/development-guide.md) - Contributing guidelines
- [Orchestrator](docs/orchestrator.md) - Multi-agent coordination details

---

## Current Status

**v0.6.0 - Full-Stack Integration Complete**

✅ End-to-end video analysis operational  
✅ Frontend-backend integration with streaming responses  
✅ Session persistence and video registry  
✅ Real-time progress updates in UI  
✅ PDF/PPTX generation with session context  
✅ Comprehensive test suite validated  

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## Testing

```bash
# Full integration test
cd backend/tests
source ../venv/bin/activate
./test_all.sh

# Test specific components
python test_grpc_client.py ../uploads/your_video.mp4  # All endpoints
python test_orchestrator.py ../uploads/your_video.mp4  # Query routing
python test_transcription.py ../uploads/your_video.mp4  # Speech-to-text
python test_vision.py ../uploads/your_video.mp4        # Visual analysis
python test_generation.py                               # Report creation
```

---

## Technologies

**Backend:** Python 3.12, llama-cpp-python (Metal), Whisper, Transformers, YOLOv8, gRPC, FastAPI, OpenCV  
**Frontend:** React 18, TypeScript, Tauri, TailwindCSS, Vite  
**AI Models:** Llama 3.1 8B (4.6GB, Q4_K_M), Whisper Medium (~1.5GB), BLIP (~1GB), YOLOv8 Nano (6MB)

**System Requirements:**
- Python 3.12.x | Node.js 18.x+
- 16GB RAM (8GB minimum) | 15GB storage (10GB models, 5GB workspace)
- Apple Silicon with Metal support

---

## Contact

**Purpose:** Intel Senior GenAI Software Solutions Engineer Application  
**Developer:** Nur Hajjariah  
**Email:** nurhajjariahk@gmail.com

---

## Project Structure

```
agentic-video-analyst/
├── backend/
│   ├── agents/            # AI agents (orchestrator, transcription, vision, generation)
│   ├── mcp_servers/       # MCP protocol implementations
│   ├── generated/         # gRPC protocol buffers
│   ├── models/            # AI models (Llama 3.1 8B, YOLOv8)
│   ├── tests/             # Test suite with results directory
│   ├── uploads/           # Video storage with registry
│   ├── main.py            # gRPC backend server
│   └── http_bridge.py     # FastAPI HTTP/JSON gateway
├── frontend/              # React + Tauri desktop app
│   └── src/               # Components, hooks, services
├── proto/                 # gRPC service definitions
└── docs/                  # Comprehensive documentation
```

---

## Advanced Setup (Manual)

For detailed manual installation steps, see [docs/installation.md](docs/installation.md).

### Model Download

```bash
cd backend/models
curl -L "https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" \
     -o Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

### Environment Configuration

```bash
cd backend
cp .env.example .env
# Edit .env with model paths and port settings
```

### Manual Startup

```bash
# Terminal 1 - gRPC Backend
cd backend && source venv/bin/activate && python main.py

# Terminal 2 - HTTP Bridge  
cd backend && source venv/bin/activate && python http_bridge.py

# Terminal 3 - Frontend
cd frontend && npm run dev
```

---

## Technical Highlights

- **Metal Acceleration**: 2-3x faster inference on M2 GPU via llama-cpp-python and PyTorch MPS
- **MCP Protocol**: Standardized agent communication satisfying assignment requirements
- **Streaming Responses**: Real-time progress updates during long-running operations
- **Session Persistence**: Video registry and analysis results survive server restarts
- **Local-First**: All models run in RAM, suitable for confidential content

### Hardware Acceleration Note

**Current Implementation (M2 Mac):**
This project uses **Apple Metal** for GPU acceleration due to development on M2 hardware. Metal provides optimal performance on Apple Silicon with 2-3x speedup over CPU-only inference.

**Intel Hardware Deployment:**
For production deployment on Intel hardware, this architecture is designed to swap Metal with **OpenVINO** optimization:
- Replace `llama-cpp-python` Metal build with OpenVINO-optimized version
- Use OpenVINO Runtime for Whisper and vision models
- Leverage Intel CPU/iGPU/discrete GPU acceleration
- Maintain same MCP protocol and agent architecture

The modular design allows acceleration backend changes without modifying core agent logic. For Intel deployments, OpenVINO would provide similar or better performance with Intel's AI acceleration technologies (AVX-512, Intel AMX, Intel GPU).

---

## Resource Usage (M2 Mac)
|-----------|-----------|
| Llama 3.1 8B | ~5-6GB |
| Whisper Medium | ~1.5GB |
| PyTorch/Vision | ~1-2GB |
| System/Other | ~2GB |
| **Total** | **~10-11GB / 16GB** |

Comfortable headroom for development tools.

---

## Troubleshooting

**Model fails to load?**
```bash
ls -lh backend/models/*.gguf  # Should show ~4.9GB
file backend/models/*.gguf    # Should show "data"
```

**Import errors?**
```bash
cd backend && source venv/bin/activate
pip list | grep -E "llama|whisper|torch"
```

**GPU not working?**
```bash
python -c "import torch; print(f'MPS: {torch.backends.mps.is_available()}')"
# Should output: MPS: True
```

For detailed troubleshooting, see [docs/installation.md](docs/installation.md). 
