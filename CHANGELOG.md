# Changelog

All notable changes to the Agentic Video Analyst project.

---

## [0.6.0] - 2026-01-09

### 🎉 Phase 6 Complete - Full-Stack Integration

**MILESTONE**: End-to-end video analysis system operational with frontend, HTTP bridge, and backend fully integrated.

### ✅ Frontend-Backend Integration

**IMPLEMENTED**: HTTP Bridge with enhanced streaming
- FastAPI bridge converts HTTP/JSON requests to gRPC calls
- Bidirectional communication between React frontend and Python backend
- Server running on port 8080 with CORS enabled
- Connected to gRPC backend on localhost:50051

**FIXED**: Streaming response flow
- HTTP bridge now sends two message types: progress updates and final response
- Progress updates: `{update: "text", progress: 0, sessionId: "..."}`
- Final response: `{response: "text", actions: [...], artifacts: [...], sessionId: "..."}`
- Frontend correctly parses both message types
- Real-time progress updates now display in UI during long-running operations

**FIXED**: Session data persistence across streaming
- `StreamQuery` method now stores results in `session_results` dict
- Accumulates transcription, vision_results, and summary data per session
- Session data persists for report generation
- Fixed empty PDF/PPTX issue caused by missing session context
- Reports now contain actual analysis data from video queries

**FIXED**: Video registry persistence
- Added `video_registry.json` in uploads directory
- Videos persist across server restarts
- `_load_video_registry()` loads mappings on startup
- `_save_video_registry()` saves after each upload
- Created `create_registry.py` utility to rebuild registry from existing uploads
- Handles 15+ videos with proper UUID → file path mapping

**IMPROVED**: Comprehensive logging throughout stack
- HTTP bridge logs: `[STREAM]`, `[QUERY]`, `[REPORT]` prefixes for clarity
- gRPC server logs: Session updates and context information
- Frontend logs: Console output for request/response debugging
- Detailed error messages with stack traces for troubleshooting

### 🔧 Backend Fixes

**FIXED**: Report generation with session context
- GenerateReport now properly retrieves session_results
- Logs available sessions and context keys for debugging
- Reports include accumulated transcription and vision data
- PDF/PPTX files now 3-4KB (with content) vs 1.6KB (empty)

**IMPROVED**: Error handling in streaming
- Graceful error handling in HTTP bridge generator
- Error chunks sent to frontend with proper formatting
- Connection recovery for interrupted streams
- Better validation of required fields (videoId, query)

### 📚 Documentation Overhaul

**CREATED**: Comprehensive documentation structure
- `docs/getting-started.md` - Complete setup and first steps guide
- `docs/installation.md` - Detailed installation instructions with troubleshooting
- Moved all setup documentation from root to `/docs` directory
- Consistent formatting and writing style across all docs

**UPDATED**: README.md
- Simplified to essential information and quick start
- Added clear architecture diagram
- Links to comprehensive docs in `/docs`
- Professional presentation for portfolio/application

**REORGANIZED**: Project structure
- Consolidated scattered markdown files
- Removed redundant quickstart files
- Clean repository root with proper documentation hierarchy
- Easy navigation for new users and developers

### 🧪 Testing & Validation

**VERIFIED**: Full integration test flow
1. Video upload through frontend → HTTP bridge → gRPC → Storage
2. Query submission → HTTP bridge → gRPC → Orchestrator → Agents → Response
3. Streaming responses → HTTP bridge → Frontend → UI display
4. Report generation → Session context → PDF/PPTX creation
5. Video registry persistence across restarts

### 🐛 Bug Fixes

- Fixed port conflicts during server startup (8080 and 50051)
- Resolved duplicate server instances causing connection issues
- Fixed video ID not found errors after server restart
- Corrected empty report generation from missing session data
- Resolved streaming response not appearing in UI chat interface

---

## [0.5.0] - 2026-01-09

### 🎯 Phase 5 Complete - gRPC Service + Report Generation

**IMPLEMENTED**: Full gRPC service with 5 endpoints
- `UploadVideo`: Video upload with metadata extraction (OpenCV)
- `QueryVideo`: Natural language queries through orchestrator
- `StreamQuery`: Real-time streaming responses
- `GetChatHistory`: Session-based message history
- `GenerateReport`: PDF/PPTX generation from session context
- Message size limits: 50MB for video uploads
- Server runs on port 50051 with graceful shutdown
- Test suite: `backend/tests/test_grpc_client.py` ✅

**FIXED**: Empty PDF generation issue
- Root cause: Session results not stored/passed to generation agent
- Added `session_results` dict in main.py to preserve orchestrator outputs
- Store transcription and vision_results after each QueryVideo call
- GenerateReport now uses stored session_results instead of parsing chat messages
- Fixed content extraction: generation_agent.py now extracts nested "content" dict
- PDFs now contain full transcription text and vision analysis
- File size increased from 1.6KB (empty) to 3.9KB (with content)

**FIXED**: PDF output directory
- Changed from `backend/results/` to `tests/results/`
- Updated orchestrator_agent.py output paths for both PDF and PPTX
- All generated reports now in proper test results folder
- Consistent with other test outputs

**FIXED**: Report generation intent detection
- LLM was misinterpreting "Generate a PDF report" as "analyze_graphs"
- Added early keyword check in analyze_intent() before LLM processing
- "pdf", "report", "pptx", "powerpoint" now bypass LLM analysis
- Prevents routing errors and ensures reliable report generation
- Reports generate consistently on first attempt

**FIXED**: Directory creation in generation agent
- Agent now creates parent directory even when output_path is explicit
- Extracts directory from output_path and creates with parents=True
- Handles both None (auto-generate) and explicit path scenarios
- Adds timestamps to prevent filename conflicts
- No more "FileNotFoundError" when generating reports

**IMPROVED**: Session context management
- Store actual agent results (not just response text)
- Accumulate transcription, vision_results, and summary per session
- Pass complete context to orchestrator for report generation
- Reports include all analysis from multi-turn conversations
- Proper data structures match what PDF generator expects

**Testing Results:**
```
✅ Video Upload: 5.38 MB, 50s duration, 360x640, 25fps
✅ Transcription: Full audio extraction with timestamps
✅ Object Detection: chair, person, tie + scene descriptions
✅ Streaming Query: Real-time progress updates
✅ Chat History: 6 messages preserved
✅ PDF Report: 3.9KB with transcription + vision analysis
```

**Current Status:**
- Backend: 100% complete ✅
- gRPC Service: All endpoints functional ✅
- Report Generation: Working with full context ✅
- Phase 5: COMPLETE ✅
- Next: Frontend development (Phase 6)

---

## [0.4.0] - 2026-01-08

### 🐛 MCP Routing Bug Fixes - Phase 4 COMPLETE

**FIXED**: Critical keyword matching order issue
- Graph/chart queries now prioritized BEFORE generic "see" matching
- "Are there any graphs?" now correctly routes to vision_analysis instead of transcription
- Moved graph detection to line 216 (before object detection at line 222)
- File: `backend/agents/orchestrator_agent.py`

**FIXED**: Vision results parsing with wrong data structure
- Objects are list of dicts with "class" key, not dict with classes as keys
- Changed from `frame["objects"].keys()` to iterating `frame["objects"]` list
- Now properly extracts object classes: chair, person, tie, etc.
- File: `backend/agents/orchestrator_agent.py` line 455-460

**FIXED**: MCP task mapping returning incomplete results
- Changed `detect_objects` task from "detect_objects" → "analyze"
- Changed `caption_video` task from "caption" → "analyze"
- Both now return BOTH objects AND captions (was returning nothing or only objects)
- File: `backend/mcp_servers/vision_mcp.py` line 90-93

**FIXED**: Response generation showing incomplete data
- Object detection queries now show detected objects list
- Scene description queries now show captions ("a woman sitting in a chair...")
- Graph queries show explicit "No graphs or charts detected" message
- Report generation shows complete file paths with .pdf/.pptx extensions
- Files: `backend/agents/orchestrator_agent.py` lines 445-500

**IMPROVED**: Response quality across all query types
- Test 1 (Transcribe): Shows full transcript ✅
- Test 2 (Objects): Lists detected objects + scene descriptions ✅
- Test 3 (Scene description): Shows detailed captions ✅
- Test 4 (Graph detection): Analyzes frames + explicit "no graphs" message ✅
- Test 5 (PDF report): Shows complete path with extension ✅
- Test 6 (PowerPoint): Shows complete path with extension ✅
- Test 7 (Summarize): Synthesizes context properly ✅

**UPDATED**: Documentation
- backend/tests/README.md: Added MCP routing explanation and architecture diagram
- AI-CONTEXT.md: Updated with Phase 4 completion and all bug fixes
- All docs now reflect working MCP routing with proper response generation

**CODE QUALITY**:
- Removed debug logging after verification
- Added proper error handling for vision result parsing
- Consistent response formatting across all query types
- Vision agent task mapping matches orchestrator expectations

**Testing Results:**
- All 7 test queries producing correct outputs
- Objects detected: chair, person, tie (real data from video)
- Scene descriptions showing in responses
- Graph detection explicitly reporting results
- Report file paths complete with extensions

**Current Status:**
- Backend: 100% complete with MCP routing working correctly ✅
- All agents tested and verified via MCP protocol ✅
- Ready for gRPC service implementation
- Ready for frontend development

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

| Version | Date       | What Happened                      |
|---------|------------|------------------------------------|
| 0.0.1   | Jan 5      | Started project                    |
| 0.1.0   | Jan 6      | Got environment working            |
| 0.2.0   | Jan 7 AM   | Upgraded to Python 3.12            |
| 0.3.0   | Jan 7 PM   | Orchestrator implemented           |
| 0.4.0   | Jan 9      | MCP routing bugs fixed             |

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

**Graph query routing:** Keyword order mattered - "see" matched before "graph". Fixed by reordering priority.

**Vision results parsing:** Expected dict structure but got list of dicts. Fixed object extraction logic.

**MCP task mapping:** Was sending wrong task names ("caption" vs "describe_scene"). Changed both to "analyze".

**Incomplete responses:** Vision results not showing objects/captions. Fixed by correcting task mapping and parsing.

---

## What's Left

Check [development-guide.md](docs/development-guide.md) for the full timeline. TL;DR:
- ✅ Agents are done
- ✅ MCP routing working
- ⏳ Need to wire up gRPC service
- ⏳ Add the frontend UI
- ⏳ Polish for demo

---

**Last Updated:** January 9, 2026  
**Python:** 3.12.12 (upgraded from 3.9.6)  
**Phase:** 4/6 Complete (Backend + MCP Routing Fully Working)
