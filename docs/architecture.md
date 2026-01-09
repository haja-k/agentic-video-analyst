# AI Video Analysis - Project Structure

```
Intel Assignment/
│
├── README.md                    # Project overview
├── QUICKSTART.md               # Quick start guide  
├── .gitignore                  # Git ignore rules
│
├── setup-backend.sh            # Backend setup script
├── download-models.sh          # Model download script
│
├── backend/                    # Python backend
│   ├── .env.example           # Environment template
│   ├── requirements.txt       # Python dependencies
│   ├── main.py               # Backend entry point
│   ├── test_models.py        # Model testing script
│   │
│   ├── agents/               # AI Agents
│   │   ├── __init__.py
│   │   ├── base_agent.py     # Base agent class
│   │   ├── transcription_agent.py   # Speech-to-text
│   │   ├── vision_agent.py          # Image analysis
│   │   └── generation_agent.py      # PDF/PPT generation
│   │
│   ├── mcp_servers/          # MCP Server implementations
│   │   ├── __init__.py
│   │   ├── base_mcp_server.py
│   │   ├── transcription_mcp.py
│   │   ├── vision_mcp.py
│   │   └── generation_mcp.py
│   │
│   ├── models/               # AI model files (gitignored)
│   │   └── .gitkeep
│   │
│   ├── data/                 # Database and persistent data
│   │   └── .gitkeep
│   │
│   ├── uploads/              # User uploaded videos
│   │   └── .gitkeep
│   │
│   └── venv/                 # Python virtual environment
│
├── frontend/                  # React + Tauri frontend
│   └── (to be created)
│
├── proto/                     # gRPC Protocol definitions
│   └── video_analysis.proto
│
└── docs/                      # Documentation
    ├── model-setup.md         # Model download guide
    └── development-guide.md   # Development workflow
```

## Component Descriptions

### Backend (`backend/`)
Python-based backend with orchestrator and specialized agents.

**Orchestrator:** Query routing and coordination via MCP
- `orchestrator_agent.py`: ✅ Llama 3.1 8B intent analysis, routes through MCP servers to agents, context management

**Specialized Agents:**
- `transcription_agent.py`: ✅ Whisper Medium for audio
- `vision_agent.py`: ✅ BLIP-2 scene descriptions + YOLOv8 object detection
- `generation_agent.py`: ✅ ReportLab PDF + python-pptx presentations
- `base_agent.py`: Abstract base class

**Test Scripts:**
- `tests/test_orchestrator.py`: Query routing and multi-agent coordination
- `tests/test_transcription.py`: Audio transcription
- `tests/test_vision.py`: Frame analysis and object detection
- `tests/test_generation.py`: PDF and PowerPoint creation
- `tests/test_all.sh`: Run everything
- `tests/results/`: Output files

**MCP Servers:**
- Custom implementation (Python 3.12 compatible)
- Standardized tool interface
- Each server wraps an agent
- ✅ Orchestrator routes through MCP protocol layer

**gRPC Service:**
- 5 endpoints fully implemented and tested
- Session management with context preservation
- 50MB message size limits for video uploads
- Server runs on port 50051

**Status:** ✅ Phase 5 Complete - gRPC service live with all endpoints functional. PDF generation working with session context. Ready for frontend integration.

### Frontend (`frontend/`)
Desktop application built with React and Tauri.

**Key Features:**
- Chat-style UI for natural language interaction
- Video upload component
- Real-time response streaming
- Persistent chat history
- Artifact display (images, PDFs, etc.)

### Protocol (`proto/`)
gRPC definitions for frontend-backend communication.

**Services (All Implemented ✅):**
- **UploadVideo:** Video file uploads with metadata extraction (OpenCV)
- **QueryVideo:** Natural language query processing through orchestrator
- **StreamQuery:** Real-time streaming responses for long operations
- **GetChatHistory:** Session-based conversation history retrieval
- **GenerateReport:** PDF/PPTX generation from accumulated session context

**Features:**
- Message size: 50MB for video uploads
- Session management with UUIDs
- Context preservation across queries
- Binary artifact transfer (PDFs, images)
- Chat history persistence
- StreamQuery: Real-time response streaming
- GenerateReport: Create PDF/PPT documents

### Models (`backend/models/`)
AI model files (not committed to git).

**Current Model Stack:**
- **LLM**: Llama 3.1 8B Instruct (Q4_K_M) - 4.9GB
- **Speech**: Whisper Medium - 1.5GB
- **Vision**: BLIP-2 (2.7B) + YOLOv8 Nano
- **OCR**: EasyOCR (if needed)

**Download:**
```bash
cd backend/models
curl -L "https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" \
     -o Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf --progress-bar
```

## Data Flow

```
User Query
    ↓
Frontend (React/Tauri) - TODO
    ↓ gRPC
Backend
    ↓
Orchestrator (Llama 3.1 8B)
    ↓
Intent Analysis
    ↓
┌───┴───┐
↓   ↓   ↓
T   V   G  (agents)
↓   ↓   ↓
Results
    ↓
Orchestrator → Backend → Frontend
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend UI | React | Interactive interface |
| Desktop Runtime | Tauri | Native desktop wrapper |
| Backend | Python 3.9+ | AI/ML processing |
| Communication | gRPC | Frontend-backend RPC |
| LLM Runtime | llama.cpp | Local LLM inference |
| Speech | Whisper | Audio transcription |
| Vision | PyTorch + Transformers | Image/video analysis |
| Document Gen | ReportLab, python-pptx | PDF/PPT creation |
| Agent Framework | Custom MCP | Agentic AI workflows |
| Database | SQLite (SQLAlchemy) | Chat history |

## Next Steps

See [QUICKSTART.md](QUICKSTART.md) for setup instructions.
