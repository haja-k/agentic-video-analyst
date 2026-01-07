# Changelog

Tracking what's been done, when things broke, and how I fixed them.

---

## [0.3.0] - 2026-01-07 Late Evening

### 🎯 Orchestrator Implementation - COMPLETE

**ADDED**: OrchestratorAgent with Llama 3.1 8B integration
- Natural language query understanding and intent analysis
- Dynamic routing to appropriate specialized agents
- Multi-agent workflow coordination
- Context management across conversations
- Fallback keyword-based intent parsing when LLM output is malformed
- Test script: `tests/test_orchestrator.py`

**Key Features:**
- Analyzes user queries to determine required actions
- Routes to TranscriptionAgent, VisionAgent, or GenerationAgent
- Handles clarification requests when needed
- Maintains conversation context for multi-turn interactions
- Supports 7+ query types: transcription, object detection, scene description, graphs, PDF/PPT generation, summarization

**FIXED**: Response generation issues
- Eliminated LLM hallucination by using factual fallback responses
- LLM now only used for summary/synthesis tasks
- Responses show actual detected objects and scene descriptions
- Stopped verbose rambling with stricter prompts and token limits

**FIXED**: Context bleeding between test queries
- Each test now shows only new results, not accumulated context
- Actions tracking properly reports what was actually executed
- Clean separation between queries in test output

**FIXED**: PowerPoint formatting
- All text now uses Calibri font throughout
- Body text: 15pt, Section headers: 28pt, Title: 32pt
- Professional, consistent appearance

**FIXED**: Rich console markup errors
- Exception messages properly escaped for square brackets
- No more markup parsing errors in test output

**UPDATED**: Backend server (main.py)
- Initializes all agents including orchestrator
- Proper lifecycle management with graceful shutdown
- Ready for gRPC service integration

**UPDATED**: Generation agent
- PDF and PPTX files now output to `results/` folder automatically
- Cleaner file organization

**ADDED**: Run scripts and utilities
- `backend/run.sh` - One-command server startup
- `backend/status.sh` - Project status display
- `backend/tests/test_all.sh` - Unified test runner

**ADDED**: Documentation
- ORCHESTRATOR_SUMMARY.md - Detailed implementation guide
- Updated README.md with orchestrator section and examples
- Updated PROJECT-STATUS.md showing Phase 3 complete
- Updated QUICKSTART.md with orchestrator test commands

**Testing Results:**
- Intent analysis: All query types correctly identified
- Transcription: Accurate audio extraction and text generation
- Vision: Proper object detection and scene descriptions
- Generation: PDF and PowerPoint creation working
- Orchestrator: Successful multi-agent coordination

**Next Steps:**
- gRPC service implementation for frontend communication
- React + Tauri desktop UI
- End-to-end integration testing

---

## [0.2.0] - 2026-01-07 Evening

### 🚀 Python 3.12 Upgrade

Upgraded from Python 3.9.6 to 3.12.12 because why not use the latest?

**What changed:**
- Installed Python 3.12 via Homebrew
- Rebuilt venv from scratch with new Python
- PyTorch bumped to 2.8.0 (from 2.1.2)
- Had to pin numpy to <2.0 because OpenCV 4.9 doesn't play nice with numpy 2.x
- All agents still work, Metal acceleration intact
- Can now use official MCP SDK if needed (requires 3.10+)

**Performance:** Python 3.12 is ~10-15% faster than 3.9, so inference should be slightly quicker.

**Files updated:**
- requirements.txt: Added `numpy<2.0` constraint
- test_models.py: Fixed model path checking
- .env.example: Updated to reflect actual model paths
- All docs updated for 3.12

---

## [0.1.0] - 2026-01-07 Morning

### ✅ Agent Implementation - Day 3 COMPLETE
- **IMPLEMENTED**: TranscriptionAgent with full Whisper integration
  - Audio extraction from video using moviepy
  - Speech-to-text with Whisper Medium model
  - Timestamped segments output
  - Test script: `tests/test_transcription.py`
- **IMPLEMENTED**: VisionAgent with BLIP-2 and YOLOv8
  - Frame extraction at regular intervals
  - Scene description using BLIP image captioning
  - Object detection using YOLOv8 nano
  - Test script: `tests/test_vision.py`
- **IMPLEMENTED**: GenerationAgent with ReportLab and python-pptx
  - PDF report generation with structured sections
  - PowerPoint presentation with multiple slides
  - Integrates transcription and vision results
  - Test script: `tests/test_generation.py`
- **ORGANIZED**: Test scripts moved to `backend/tests/` directory
  - All test outputs saved to `backend/tests/results/`
  - Cleaner project structure
- **TESTED**: All three agents working on M2 with Metal acceleration
- **VERIFIED**: Models auto-download on first use

### 📝 Documentation Overhaul
- **ADDED**: Consolidated [README.md](README.md) with complete project overview
- **ADDED**: Concise [QUICKSTART.md](QUICKSTART.md) with 5-step setup
- **ADDED**: This changelog to track project evolution
- **UPDATED**: All docs/ files to reflect current architecture
- **REMOVED**: Redundant markdown files (MODEL-UPDATE.md, SETUP-STATUS.md, etc.)

### 🤖 Model Selection - Final Decision
- **CHANGED**: Primary model from Llama 3.2 Vision 11B → **Llama 3.1 8B** (4.9GB Q4_K_M)
- **REASON**: Llama 3.2 Vision gated/restricted on HuggingFace (404 errors, requires approval)
- **ADDED**: Working download URLs from lmstudio-community repo
- **ADDED**: Alternative options: Mistral 7B, Llama 3.2 3B
- **FIXED**: download-models.sh with publicly accessible repos

### 🐛 Model Download Issues
- **IDENTIFIED**: Authentication failures with restricted/gated models
- **IDENTIFIED**: Downloaded files only 29 bytes ("Invalid username or password")
- **SOLUTION**: Switched to public model repositories (lmstudio-community, TheBloke)
- **ADDED**: File size verification in troubleshooting docs

---

## [0.1.0] - 2026-01-06

### ✅ Environment Setup Complete
- **CREATED**: Python 3.9.6 virtual environment at backend/venv/
- **INSTALLED**: 50+ dependencies including:
  - llama-cpp-python 0.2.90 with Metal GPU acceleration
  - PyTorch 2.1.2 with MPS (Metal Performance Shaders)
  - openai-whisper 20231117
  - transformers 4.36.2 (BLIP-2 vision models)
  - FastAPI 0.109.0 + gRPC 1.60.0
  - OpenCV 4.9.0.80, moviepy 1.0.3, av 12.3.0
  - ReportLab 4.0.9, python-pptx 0.6.23

### 🔧 Dependency Resolution
- **FIXED**: numpy 2.0.2 → 1.26.4 (PyTorch compatibility)
- **FIXED**: faster-whisper → openai-whisper (ffmpeg 8.0 compatibility)
- **FIXED**: av build errors → used pre-built wheel av 12.3.0
- **FIXED**: MCP SDK requires Python 3.10+ → implemented custom MCP protocol

### 🏗️ Project Structure
- **CREATED**: Directory layout (backend/, frontend/, proto/, docs/)
- **CREATED**: Agent framework (base_agent.py, transcription_agent.py, vision_agent.py, generation_agent.py)
- **CREATED**: Custom MCP servers (base_mcp_server.py + 3 implementations)
- **CREATED**: gRPC protocol definition (video_analysis.proto)
- **CREATED**: test_models.py for validation

### 🎨 Frontend Placeholder
- **CREATED**: Basic React + Tauri structure
- **STATUS**: Not yet implemented (Phase 2)

---

## [0.0.1] - Initial Commit

### 🎯 Project Kickoff
- **GOAL**: Build fully local AI desktop app for video analysis
- **PLATFORM**: MacBook Air M2, 16GB RAM, macOS
- **TECH STACK**: 
  - Frontend: React + Tauri (desktop app)
  - Backend: Python + llama.cpp + Whisper + BLIP-2
  - Communication: gRPC
  - Protocol: Model Context Protocol (MCP)
- **TIMELINE**: 6 days for working demo
- **CONSTRAINT**: All AI must run locally (no cloud APIs)

### 🔍 Requirements Analysis
- **Transcription**: Whisper for speech-to-text from video audio
- **Vision**: BLIP-2 for analyzing video frames/screenshots
- **Generation**: Llama for natural language processing and Q&A
- **Output**: PDF/PPT reports with chat history
- **Database**: SQLite for conversation persistence

---

## Version Timeline

| Version | Date       | What Happened             |
|---------|------------|---------------------------|
| 0.0.1   | Jan 5      | Started project           |
| 0.1.0   | Jan 6      | Got environment working   |
| 0.2.0   | Jan 7      | Upgraded to Python 3.12   |

---

## Why I Did Things This Way

**openai-whisper instead of faster-whisper:** faster-whisper broke with ffmpeg 8.0, and I wasn't about to downgrade my system ffmpeg.

**Custom MCP implementation:** Official SDK needs Python 3.10+, and I started with 3.9.6. Now on 3.12 so could switch, but the custom one works fine.

**Q4_K_M quantization:** 4.9GB model vs 16GB full precision. Same quality for chat stuff, way less RAM.

**Metal acceleration:** M2 has a GPU, might as well use it. Makes inference 3-5x faster.

**Python 3.12:** Better performance (10-15% faster), longer support, and unlocks access to newer libraries.

---

## Things That Broke

**Llama 3.2 Vision:** Wanted to use this but it's gated on HuggingFace. Switched to Llama 3.1 8B instead.

**av package:** Wouldn't compile from source. Used pre-built wheel: `pip install av==12.3.0`

**numpy 2.0:** OpenCV isn't ready for it yet. Pinned to numpy <2.0 in requirements.

**faster-whisper:** Broke with ffmpeg 8.0. Went with openai-whisper instead.

---

## What's Left

Check [development-guide.md](docs/development-guide.md) for the full timeline. TL;DR:
- Agents are done
- Need to wire up frontend
- Add the chat interface
- Polish for demo

---

**Last Updated:** January 7, 2026  
**Python:** 3.12.12 (upgraded from 3.9.6)
