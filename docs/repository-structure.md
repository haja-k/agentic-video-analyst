# Repository Structure

Clean, organized structure for the Agentic Video Analyst project.

---

## Root Directory

```
Intel Assignment/
├── README.md                    # Project overview and quick start
├── CHANGELOG.md                 # Version history and updates
├── .gitignore                   # Git ignore rules
│
├── backend/                     # Python backend application
│   ├── main.py                  # gRPC server entry point
│   ├── http_bridge.py           # FastAPI HTTP/JSON bridge
│   ├── requirements.txt         # Python dependencies
│   ├── agents/                  # AI agent implementations
│   ├── mcp_servers/             # MCP protocol servers
│   ├── generated/               # gRPC generated code
│   ├── models/                  # AI model files (gitignored)
│   ├── uploads/                 # Video upload storage
│   ├── logs/                    # Application logs
│   ├── tests/                   # Backend test suite
│   └── venv/                    # Python virtual environment
│
├── frontend/                    # React + Tauri frontend
│   ├── src/                     # React source code
│   ├── public/                  # Static assets
│   ├── package.json             # Node dependencies
│   └── src-tauri/               # Tauri desktop wrapper
│
├── docs/                        # Complete documentation
│   ├── README.md                # Documentation index
│   ├── getting-started.md       # Setup and usage guide
│   ├── installation.md          # Installation instructions
│   ├── architecture.md          # System design
│   ├── orchestrator.md          # Agent coordination
│   ├── grpc-implementation.md   # API specifications
│   ├── development-guide.md     # Contributing guidelines
│   ├── model-setup.md           # Model configuration
│   ├── model-comparison.md      # Model selection
│   └── archive/                 # Historical documentation
│
├── proto/                       # gRPC protocol definitions
│   └── video_analysis.proto     # Service definitions
│
├── download-models.sh           # Model download script
├── setup-backend.sh             # Backend setup automation
├── setup-complete.sh            # Complete system setup
└── start-all.sh                 # Launch all services
```

---

## Key Files

### Essential Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview, features, quick start |
| `CHANGELOG.md` | Version history and recent updates |
| `docs/README.md` | Documentation index and navigation |

### Backend Entry Points

| File | Port | Purpose |
|------|------|---------|
| `backend/main.py` | 50051 | gRPC server for video analysis |
| `backend/http_bridge.py` | 8080 | HTTP/JSON bridge for frontend |

### Frontend Entry Points

| File | Port | Purpose |
|------|------|---------|
| `frontend/src/main.tsx` | 1420 | React application entry |
| `frontend/src/App.tsx` | - | Main app component |

### Setup Scripts

| Script | Purpose |
|--------|---------|
| `download-models.sh` | Download AI models (~5GB) |
| `setup-backend.sh` | Setup Python environment |
| `setup-complete.sh` | Complete system setup |
| `start-all.sh` | Launch all services |

---

## Documentation Organization

### User Documentation (`docs/`)

**Getting Started:**
- `installation.md` - Detailed setup instructions
- `getting-started.md` - First steps and usage

**Technical:**
- `architecture.md` - System design and components
- `grpc-implementation.md` - API specifications
- `orchestrator.md` - Multi-agent coordination

**Development:**
- `development-guide.md` - Contributing guidelines
- `model-setup.md` - Model configuration
- `model-comparison.md` - Model selection rationale

### Archived Documentation (`docs/archive/`)

Historical files moved from root:
- `QUICKSTART.md` - Original quick start guide
- `FRONTEND-QUICKSTART.md` - Frontend setup notes
- `PHASE-6-COMPLETE.md` - Phase completion notes
- `PROJECT-STATUS.md` - Development status tracking
- `AI-CONTEXT.md` - Context and background
- Other development notes and checklists

---

## Backend Structure

```
backend/
├── main.py                      # gRPC server
├── http_bridge.py               # HTTP/JSON bridge
├── requirements.txt             # Dependencies
│
├── agents/                      # AI Agents
│   ├── base_agent.py            # Base agent class
│   ├── orchestrator_agent.py    # Query routing (Llama)
│   ├── transcription_agent.py   # Speech-to-text (Whisper)
│   ├── vision_agent.py          # Visual analysis (BLIP+YOLO)
│   └── generation_agent.py      # Report creation
│
├── mcp_servers/                 # MCP Protocol
│   ├── base_mcp_server.py       # Base MCP server
│   ├── transcription_mcp.py     # Transcription MCP
│   ├── vision_mcp.py            # Vision MCP
│   └── generation_mcp.py        # Generation MCP
│
├── generated/                   # gRPC Generated
│   ├── video_analysis_pb2.py    # Protocol buffers
│   └── video_analysis_pb2_grpc.py
│
├── models/                      # AI Models (gitignored)
│   ├── Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
│   └── yolov8n.pt
│
├── uploads/                     # Video Storage
│   └── video_registry.json      # Video ID mapping
│
├── logs/                        # Application Logs
│   ├── grpc_server.log
│   └── http_bridge.log
│
└── tests/                       # Test Suite
    ├── test_all.sh              # Run all tests
    ├── test_orchestrator.py     # Test orchestrator
    ├── test_transcription.py    # Test transcription
    ├── test_vision.py           # Test vision
    ├── test_generation.py       # Test generation
    ├── test_grpc_client.py      # Test gRPC
    └── results/                 # Test outputs
```

---

## Frontend Structure

```
frontend/
├── src/
│   ├── main.tsx                 # Entry point
│   ├── App.tsx                  # Main app
│   ├── index.css                # Global styles
│   │
│   ├── components/              # React Components
│   │   ├── ChatInterface.tsx    # Chat UI
│   │   ├── VideoUpload.tsx      # Upload UI
│   │   └── VideoInfo.tsx        # Video metadata
│   │
│   ├── hooks/                   # Custom Hooks
│   │   ├── useVideoQuery.ts     # Query hook
│   │   ├── useVideoUpload.ts    # Upload hook
│   │   └── useChatHistory.ts    # History hook
│   │
│   └── services/                # API Services
│       └── api.ts               # Backend communication
│
├── public/                      # Static Assets
├── package.json                 # Dependencies
└── src-tauri/                   # Desktop Wrapper
    └── src/main.rs              # Tauri entry
```

---

## Git Ignored Items

Key directories excluded from git:

```gitignore
# Dependencies
backend/venv/
frontend/node_modules/

# AI Models (~5GB)
backend/models/*.gguf
backend/models/*.pt

# User Data
backend/uploads/*.mp4
backend/uploads/*.mov

# Build Artifacts
frontend/dist/
frontend/src-tauri/target/

# Logs
backend/logs/*.log

# System Files
.DS_Store
__pycache__/
```

---

## File Counts

```
Total Files: ~150
├── Python Files: ~30
├── TypeScript/React Files: ~15
├── Documentation Files: ~12
├── Configuration Files: ~10
└── Test Files: ~10
```

---

## Navigation Guide

### For New Users
1. Start with [README.md](../README.md)
2. Follow [docs/installation.md](installation.md)
3. Read [docs/getting-started.md](getting-started.md)

### For Developers
1. Review [README.md](../README.md)
2. Study [docs/architecture.md](architecture.md)
3. Follow [docs/development-guide.md](development-guide.md)
4. Explore backend code in `backend/agents/`

### For API Integration
1. See [docs/grpc-implementation.md](grpc-implementation.md)
2. Check `backend/http_bridge.py` for HTTP endpoints
3. Review `proto/video_analysis.proto` for definitions

---

## Maintenance

### Regular Updates
- Update [CHANGELOG.md](../CHANGELOG.md) with each change
- Keep version numbers in sync across files
- Update documentation when features change

### Clean Up Commands

```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -r {} +

# Remove logs
rm backend/logs/*.log

# Remove uploaded videos
rm backend/uploads/*.mp4

# Remove test results
rm backend/tests/results/*
```

---

*Last Updated: January 9, 2026*
