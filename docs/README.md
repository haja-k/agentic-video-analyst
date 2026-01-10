# Documentation Index

Complete documentation for the Agentic Video Analyst system.

---

## User Documentation

### Getting Started
- **[Installation Guide](installation.md)** - Complete setup instructions from scratch
- **[Getting Started](getting-started.md)** - First steps, running the application, and basic usage

### Usage Guides
- **[Getting Started](getting-started.md#first-steps)** - Upload videos and ask questions
- **[Getting Started](getting-started.md#testing-backend-components)** - Testing individual components
- **[Getting Started](getting-started.md#troubleshooting)** - Common issues and solutions

---

## Technical Documentation

### Architecture & Design
- **[Architecture Overview](architecture.md)** - System design, components, and data flow
- **[Orchestrator](orchestrator.md)** - Multi-agent coordination and intent classification
- **[gRPC Implementation](grpc-implementation.md)** - API specifications and protobuf definitions

### Development
- **[Development Guide](development-guide.md)** - Contributing guidelines and code standards
- **[Model Setup](model-setup.md)** - AI model configuration and optimization
- **[Model Comparison](model-comparison.md)** - Model selection rationale

---

## Quick Links

### Setup & Installation
1. [System Requirements](installation.md#system-requirements)
2. [Step-by-Step Installation](installation.md#step-by-step-installation)
3. [Download AI Models](installation.md#4-download-ai-models)
4. [Verify Installation](installation.md#verify-installation)

### Running the Application
1. [Quick Start Options](getting-started.md#running-the-application)
2. [First Steps](getting-started.md#first-steps)
3. [Testing Components](getting-started.md#testing-backend-components)

### Troubleshooting
1. [Backend Won't Start](getting-started.md#backend-wont-start)
2. [Port Conflicts](getting-started.md#port-already-in-use)
3. [Model Loading Issues](getting-started.md#models-not-loading)
4. [Installation Problems](installation.md#troubleshooting-installation)

---

## Architecture Overview

```
Frontend (React + Tauri)
    ↓ HTTP/JSON (port 8080)
HTTP Bridge (FastAPI)
    ↓ gRPC (port 50051)
Backend (Python)
    ├── Orchestrator Agent (Llama 3.1 8B)
    └── MCP Servers
        ├── Transcription (Whisper)
        ├── Vision (BLIP + YOLOv8)
        └── Generation (ReportLab + python-pptx)
```

**Key Technologies:**
- Multi-agent orchestration via Model Context Protocol (MCP)
- Metal-accelerated inference on Apple Silicon
- gRPC for backend communication
- FastAPI bridge for frontend integration
- Session-based context management

---

## Component Documentation

### Backend Components

| Component | Documentation | Purpose |
|-----------|---------------|---------|
| Orchestrator | [orchestrator.md](orchestrator.md) | Query routing and agent coordination |
| Transcription Agent | [architecture.md#agents](architecture.md) | Speech-to-text with Whisper |
| Vision Agent | [architecture.md#agents](architecture.md) | Object detection and scene analysis |
| Generation Agent | [architecture.md#agents](architecture.md) | PDF/PPTX report creation |
| gRPC Service | [grpc-implementation.md](grpc-implementation.md) | Backend API server |
| HTTP Bridge | [architecture.md#http-bridge](architecture.md) | Frontend communication |

### Frontend Components

| Component | Path | Purpose |
|-----------|------|---------|
| App.tsx | `frontend/src/App.tsx` | Main application container |
| ChatInterface | `frontend/src/components/ChatInterface.tsx` | Chat UI and message display |
| VideoUpload | `frontend/src/components/VideoUpload.tsx` | Video upload handling |
| VideoInfo | `frontend/src/components/VideoInfo.tsx` | Video metadata and controls |

---

## API Documentation

### gRPC Endpoints

1. **UploadVideo** - Upload video with metadata extraction
2. **QueryVideo** - Single query processing
3. **StreamQuery** - Streaming query responses
4. **GetChatHistory** - Retrieve session messages
5. **GenerateReport** - Create PDF/PPTX reports

See [gRPC Implementation](grpc-implementation.md) for full API specifications.

### HTTP Bridge Endpoints

- `GET /health` - Health check
- `POST /upload` - Video upload
- `POST /query` - Single query
- `POST /stream` - Streaming query
- `GET /history` - Chat history
- `POST /report` - Generate report

---

## Development Workflow

1. **Setup Development Environment**
   - Follow [Installation Guide](installation.md)
   - Read [Development Guide](development-guide.md)

2. **Make Changes**
   - Follow code standards in [Development Guide](development-guide.md)
   - Test changes with backend test suite

3. **Test Changes**
   ```bash
   cd backend/tests
   ./test_all.sh
   ```

4. **Submit Changes**
   - Create descriptive commit messages
   - Update [CHANGELOG.md](../CHANGELOG.md)
   - Update relevant documentation

---

## Testing Documentation

### Backend Tests

| Test | Command | Purpose |
|------|---------|---------|
| All Tests | `./test_all.sh` | Run complete test suite |
| Transcription | `python test_transcription.py` | Test audio transcription |
| Vision | `python test_vision.py` | Test visual analysis |
| Generation | `python test_generation.py` | Test report creation |
| Orchestrator | `python test_orchestrator.py` | Test query routing |
| gRPC | `python test_grpc_client.py` | Test full integration |

See [Getting Started - Testing](getting-started.md#testing-backend-components) for details.

---

## Model Documentation

### AI Models Used

| Model | Size | Purpose | Documentation |
|-------|------|---------|---------------|
| Llama 3.1 8B | 4.6GB | Orchestration and intent classification | [model-setup.md](model-setup.md) |
| Whisper Medium | ~1.5GB | Speech transcription | [model-setup.md](model-setup.md) |
| BLIP | ~1GB | Image captioning | [model-setup.md](model-setup.md) |
| YOLOv8 Nano | 6MB | Object detection | [model-setup.md](model-setup.md) |

See [Model Comparison](model-comparison.md) for selection rationale.

---

## Archived Documentation

Historical documentation and development notes are available in `docs/archive/`:
- Original quickstart guides
- Phase completion notes
- Development context files
- Setup summaries

---

## Contributing

See [Development Guide](development-guide.md) for:
- Code standards and style guide
- Testing requirements
- Commit message format
- Pull request process

---

## Support

### Common Issues
- [Troubleshooting Guide](getting-started.md#troubleshooting)
- [Installation Problems](installation.md#troubleshooting-installation)

### Resources
- [CHANGELOG](../CHANGELOG.md) - Version history
- [README](../README.md) - Project overview

---

*Last Updated: January 9, 2026*
