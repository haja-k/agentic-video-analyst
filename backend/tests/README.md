# Test Scripts

This directory contains test scripts for all AI agents in the video analysis system.

## Quick Test

### Run gRPC Service (Full Integration) ✅
```bash
cd backend
source venv/bin/activate

# Start gRPC server
./run.sh

# In another terminal, run comprehensive test
cd backend
source venv/bin/activate
python tests/test_grpc_client.py uploads/CunkOnEarth.mp4
```

Tests all 6 scenarios: video upload, transcription, vision analysis, streaming, chat history, and PDF report generation.

### Run All Agent Tests
```bash
cd backend/tests
source ../venv/bin/activate
./test_all.sh ../uploads/your_video.mp4
```

Runs all individual agent test scripts in sequence with the provided video.

---

## gRPC Service Tests

### test_grpc_client.py ✅
Comprehensive test suite for the complete gRPC service with all 5 endpoints.

```bash
cd backend
source venv/bin/activate

# Ensure server is running
./run.sh

# Run full test suite
python tests/test_grpc_client.py uploads/your_video.mp4
```

**What it tests:**
1. **Video Upload** - File upload with OpenCV metadata extraction
2. **Transcription Query** - "Transcribe the video" through orchestrator
3. **Vision Query** - "What objects can you see?" with object detection
4. **Streaming Query** - Real-time response updates
5. **Chat History** - Session-based message persistence
6. **PDF Generation** - Context-aware report with session analysis

**Features:**
- Rich formatted output with tables and panels
- Session management with UUIDs
- Context preservation across queries
- Binary artifact handling (PDFs)
- Interactive mode: `--interactive` flag

**Test Results:**
- ✅ Video upload: 5.38 MB, 50s duration, 360x640 resolution
- ✅ Transcription: Full audio-to-text extraction
- ✅ Vision: Objects detected (chair, person, tie) + scene descriptions
- ✅ Streaming: Real-time progress updates
- ✅ Chat history: 6 messages preserved
- ✅ PDF generation: 3.9KB report with complete analysis

### test_connection.py ✅
Simple verification that the gRPC server is running and responding.

```bash
cd backend
source venv/bin/activate
python tests/test_connection.py
```

Expected output:
```
✓ Successfully connected to gRPC server on localhost:50051
✓ Chat history request successful: 0 messages
[SUCCESS] gRPC server is running and responding correctly!
```

### test_grpc.sh
Automated test runner that manages server lifecycle.

```bash
cd backend/tests
source ../venv/bin/activate
./test_grpc.sh
```

Starts server, runs tests, and stops server automatically.

---

## Individual Agent Tests

### test_orchestrator.py
Test the OrchestratorAgent with Llama 3.1 8B for query routing and multi-agent coordination through MCP servers.

```bash
cd backend/tests
source ../venv/bin/activate

# Quick intent analysis test (no video needed)
python test_orchestrator.py --intent-only

# Full workflow test with video
python test_orchestrator.py ../uploads/your_video.mp4
```

**What it tests:**
- Natural language query understanding
- Intent analysis and action routing through MCP servers
- MCP protocol communication between orchestrator and specialized agents
- Multi-agent coordination via standardized tool calls
- Context management across queries

**MCP Routing Implementation:**
The orchestrator no longer calls agents directly. Instead, it routes queries through MCP (Model Context Protocol) servers that wrap each specialized agent:
- `TranscriptionMCPServer` → `TranscriptionAgent` (Whisper)
- `VisionMCPServer` → `VisionAgent` (BLIP-2 + YOLOv8)
- `GenerationMCPServer` → `GenerationAgent` (ReportLab + python-pptx)

This ensures standardized communication and allows for future extensibility.

**Example queries:**
- "Transcribe the video"
- "What objects can you see in the video?"
- "Describe what's happening in the video"
- "Are there any graphs or charts shown?"
- "Create a PDF report with the key points discussed"
- "Summarize our discussion so far"

### test_transcription.py
Test the TranscriptionAgent with Whisper speech-to-text.

```bash
cd backend/tests
source ../venv/bin/activate
python test_transcription.py ../uploads/your_video.mp4
```

**Output:** `results/transcription_result.json`

### test_vision.py
Test the VisionAgent with BLIP-2 image captioning and YOLOv8 object detection.

```bash
cd backend/tests
source ../venv/bin/activate
python test_vision.py ../uploads/your_video.mp4
```

**Output:** `results/vision_result.json`

### test_generation.py
Test the GenerationAgent to create PDF and PowerPoint reports from previous results.

```bash
cd backend/tests
source ../venv/bin/activate
python test_generation.py
```

**Outputs:**
- `results/video_report.pdf`
- `results/video_presentation.pptx`

### test_models.py
Verify all AI models and dependencies are correctly installed.

```bash
cd backend/tests
source ../venv/bin/activate
python test_models.py
```

---

## Results Directory

All test outputs are saved in `results/`:
- `transcription_result.json` - Full transcription with timestamps
- `vision_result.json` - Frame analysis with objects and captions
- `report_*.pdf` - Generated PDF reports with session analysis (3-4KB, timestamped)
- `report_*.pptx` - Generated PowerPoint presentations (timestamped)
- `video_report.pdf` - Test generation output
- `server.log` - gRPC server logs (when using test_grpc.sh)

**Note:** PDF reports are now generated in `tests/results/` and include full transcription text and vision analysis from the session.

---

## Running Tests

Always activate the virtual environment first:

```bash
cd backend
source venv/bin/activate
cd tests
```

Then run the desired test script.

---

## Architecture

### gRPC Service Flow (Phase 5 Complete ✅)

```
Frontend (React+Tauri) ←─────gRPC────→ Backend (main.py)
                                            ↓
                                      gRPC Servicer
                                      - UploadVideo
                                      - QueryVideo
                                      - StreamQuery
                                      - GetChatHistory
                                      - GenerateReport
                                            ↓
                                      Session Management
                                      - video_id mapping
                                      - chat_history storage
                                      - session_results accumulation
                                            ↓
User Query → Orchestrator (Llama 3.1 8B)
                 ↓
         Intent Analysis
                 ↓
    ┌────────────┼────────────┐
    ↓            ↓            ↓
Transcription  Vision    Generation
  MCPServer    MCPServer   MCPServer
    ↓            ↓            ↓
Transcription  Vision    Generation
  Agent        Agent       Agent
    ↓            ↓            ↓
  Whisper    BLIP-2+YOLOv8  ReportLab+pptx
```

**gRPC Implementation:**
- 5 endpoints handling video upload, queries, streaming, history, and reports
- Session-based context management for multi-turn conversations
- Message size: 50MB limit for video uploads
- Server runs on port 50051 with graceful shutdown
- Binary artifact transfer (PDFs, images)

**MCP Protocol Layer:**
- Orchestrator communicates with MCP servers using standardized tool calls
- Each MCP server wraps a specialized agent and handles protocol translation
- Enables modular architecture and future agent additions

**Session Context:**
- Results stored per session in `session_results` dict
- Accumulates transcription and vision analysis across queries
- PDF reports include complete session context
- Chat history preserved for conversation continuity
