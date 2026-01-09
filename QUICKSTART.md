# Quick Start

**Updated:** Jan 8, 2026 | M2 MacBook Air | Python 3.12

Everything's already set up - Python 3.12 venv, Metal-accelerated llama.cpp, Llama 3.1 8B (4.6GB in backend/models/), all deps installed. **MCP routing now complete** - orchestrator routes through MCP protocol layer to agents. Just run the tests.

---

## Quick Test

### Test Orchestrator (No Video)

```bash
cd backend/tests
source ../venv/bin/activate
python test_orchestrator.py --intent-only
```

Tests query routing without needing a video file.

### Test with Video

```bash
cd backend/tests
source ../venv/bin/activate

# Full orchestrator test
python test_orchestrator.py /path/to/video.mp4

# Or test individual agents
python test_transcription.py /path/to/video.mp4
python test_vision.py /path/to/video.mp4
python test_generation.py

# Run everything
./test_all.sh /path/to/video.mp4
```

---

## Start Backend

```bash
cd backend
./run.sh
```

Starts server on port 50051.

---

## Test gRPC Service

### Quick Connection Test

```bash
cd backend
source venv/bin/activate
python tests/test_connection.py
```

Verifies gRPC server is running and accepting connections.

### Full gRPC Test Suite

```bash
cd backend
source venv/bin/activate
python tests/test_grpc_client.py uploads/SolarPower.mp4
```

Tests video upload, queries, streaming, and report generation.

### Automated Test (starts/stops server)

```bash
cd backend
./tests/test_grpc.sh
```

---

## What Queries Work

- "Transcribe the video"
- "What objects are in the video?"
- "Describe what's happening"
- "Any graphs or charts shown?"
- "Create a PowerPoint with the key points"
- "Summarize our discussion"
- "Generate a PDF report"

---
  --python_out=. \
  --grpc_python_out=. \
  ../proto/video_analysis.proto
```

---

### Step 5: Start Backend

```bash
cd backend
source venv/bin/activate
python main.py
```

Backend will start on `localhost:50051`

---

## �� Alternative Models

If Llama 3.1 8B is too large, try:

**Llama 3.2 3B (smaller, faster):**
```bash
cd backend/models
curl -L "https://huggingface.co/lmstudio-community/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf" \
     -o llama-3.2-3b-instruct.Q4_K_M.gguf --progress-bar
```
Update `.env`: `LLAMA_MODEL_PATH=models/llama-3.2-3b-instruct.Q4_K_M.gguf`

**Mistral 7B (alternative):**
```bash
cd backend/models
curl -L "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf" \
     -o mistral-7b-instruct-v0.2.Q4_K_M.gguf --progress-bar
```
Update `.env`: `LLAMA_MODEL_PATH=models/mistral-7b-instruct-v0.2.Q4_K_M.gguf`

---

## 🐛 Troubleshooting

### Model download fails
```bash
# Check internet connection
ping huggingface.co

# Try alternative download with wget
brew install wget
wget "https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" -O Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

### Model file corrupted
```bash
# Check file type (should be "data", not "ASCII text")
file backend/models/*.gguf

# If corrupted, delete and redownload
rm backend/models/*.gguf
# Then download again
```

### Import errors
```bash
# Always activate virtual environment first
cd backend
source venv/bin/activate

# Verify packages
pip list | grep -E "llama|whisper|torch"
```

### GPU not working
```bash
# Check Metal support
python -c "import torch; print(torch.backends.mps.is_available())"
# Should print: True

# Check llama.cpp
python -c "import llama_cpp; print(llama_cpp.__version__)"
# Should print: 0.2.90
```

---

## 📚 Next Steps

1. **Implement TranscriptionAgent** - Use Whisper for speech-to-text
2. **Build Chat UI** - React interface for queries
3. **Implement VisionAgent** - BLIP-2 for image analysis
4. **Add Report Generation** - PDF/PPT output

See [docs/development-guide.md](docs/development-guide.md) for detailed plan.

---

## 🎯 Quick Commands

```bash
# Activate environment
cd backend && source venv/bin/activate

# Test setup
python test_models.py

# Start backend
python main.py

# Check logs (output appears in console)
# Backend logs directly to terminal output

# Deactivate environment
deactivate
```

---

**Status:** Environment ✅ | Download Model ⚠️ | Start Coding 🚀
