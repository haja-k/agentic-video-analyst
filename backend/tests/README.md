# Test Scripts

This directory contains test scripts for all AI agents in the video analysis system.

## Quick Test

### Run All Tests
```bash
cd backend/tests
source ../venv/bin/activate
./test_all.sh ../uploads/your_video.mp4
```

Runs all test scripts in sequence with the provided video.

---

## Individual Test Scripts

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
- `report_*.pdf` - Generated PDF reports (timestamped)
- `report_*.pptx` - Generated PowerPoint presentations (timestamped)

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

The orchestrator coordinates all agents through MCP servers:

```
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

**MCP Protocol Layer:**
- Orchestrator communicates with MCP servers using standardized tool calls
- Each MCP server wraps a specialized agent and handles protocol translation
- Enables modular architecture and future agent additions
