# Getting Started

**Agentic Video Analyst** - Complete setup and usage guide for the local AI video analysis system.

---

## Prerequisites

- **Hardware:** Apple Silicon Mac (M1/M2/M3) with 16GB+ RAM recommended
- **OS:** macOS 12.0 or later
- **Python:** 3.12.x
- **Node.js:** 18.x or later (for frontend)
- **Storage:** ~10GB free space for models

---

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd "Intel Assignment"
```

### 2. Backend Setup

The backend uses Python with a virtual environment for dependency isolation.

```bash
cd backend

# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Download AI Models

Download the required models (~5GB total):

```bash
# Run the model download script
chmod +x download-models.sh
./download-models.sh
```

**Models Downloaded:**
- Llama 3.1 8B Instruct (Q4_K_M quantized) - 4.6GB - Orchestrator
- Whisper Medium - ~1.5GB - Speech transcription
- BLIP Image Captioning - ~1GB - Scene description
- YOLOv8 Nano - 6MB - Object detection

Models are saved to `backend/models/` directory.

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Build frontend (optional)
npm run build
```

---

## Running the Application

### Option 1: Quick Start (All-in-One)

Use the startup script to launch both backend and frontend:

```bash
./start-all.sh
```

This starts:
- gRPC server on port 50051
- HTTP bridge on port 8080
- Frontend dev server on port 1420

### Option 2: Manual Start

**Terminal 1 - Backend (gRPC Server):**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - HTTP Bridge:**
```bash
cd backend
source venv/bin/activate
python http_bridge.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option 3: Backend Only (Testing)

```bash
cd backend
source venv/bin/activate
python main.py
```

Then use test scripts in `backend/tests/` to interact with the gRPC service directly.

---

## First Steps

1. **Open the Application**
   - Navigate to `http://localhost:1420` in your browser
   - The desktop app window should open automatically

2. **Upload a Video**
   - Click "Upload Video" or drag-and-drop
   - Supported formats: MP4, MOV, AVI
   - Recommended: ~1 minute videos for faster processing

3. **Ask Questions**
   - "Transcribe the video"
   - "What objects can you see?"
   - "Describe the scene"
   - "Generate a PDF report"

4. **View Results**
   - Transcriptions appear in chat
   - Analysis results shown with confidence scores
   - Reports saved to `backend/tests/results/`

---

## Testing Backend Components

### Test Individual Agents

```bash
cd backend/tests
source ../venv/bin/activate

# Test transcription
python test_transcription.py

# Test vision analysis
python test_vision.py

# Test report generation
python test_generation.py
```

### Test Orchestrator

```bash
# Test query routing (no video needed)
python test_orchestrator.py --intent-only

# Test with actual video
python test_orchestrator.py /path/to/video.mp4
```

### Test gRPC Service

```bash
# Full integration test
python test_grpc_client.py
```

---

## Troubleshooting

### Backend Won't Start

**Check Python version:**
```bash
python --version  # Should be 3.12.x
```

**Activate virtual environment:**
```bash
cd backend
source venv/bin/activate
```

**Verify models downloaded:**
```bash
ls -lh backend/models/
# Should see: Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf (4.6GB)
# Should see: yolov8n.pt (6MB)
```

### Port Already in Use

**Kill existing processes:**
```bash
# Kill gRPC server
lsof -ti :50051 | xargs kill

# Kill HTTP bridge
lsof -ti :8080 | xargs kill

# Kill frontend dev server
lsof -ti :1420 | xargs kill
```

### Frontend Not Connecting

1. Verify backend is running:
   ```bash
   curl http://localhost:8080/health
   # Should return: {"status":"ok","service":"http-bridge"}
   ```

2. Check browser console for errors (F12 → Console)

3. Restart frontend dev server:
   ```bash
   cd frontend
   npm run dev
   ```

### Models Not Loading

**Check model paths in code:**
- Backend models: `backend/models/`
- Test models: `backend/tests/models/`

**Re-download if corrupted:**
```bash
cd backend
rm -rf models/*
./download-models.sh
```

### Video Upload Fails

**Verify uploads directory exists:**
```bash
mkdir -p backend/uploads
```

**Check video registry:**
```bash
cat backend/uploads/video_registry.json
```

**Supported formats:** MP4, MOV, AVI, WebM
**Max size:** 50MB (configurable in gRPC settings)

---

## Performance Tips

### For Faster Processing

1. **Use shorter videos** (~30-60 seconds)
2. **Lower resolution** (720p is sufficient)
3. **Close other apps** to free RAM
4. **Use SSD storage** for models and videos

### Memory Usage

- **Idle:** ~2GB
- **Processing video:** ~6-8GB
- **Peak (transcription):** ~10GB

If experiencing memory issues:
- Close browser tabs
- Use smaller video files
- Process one video at a time

---

## Next Steps

- Read [Architecture Documentation](architecture.md) to understand system design
- Review [Development Guide](development-guide.md) for contributing
- Check [gRPC Implementation](grpc-implementation.md) for API details
- See [Model Setup](model-setup.md) for advanced configuration

---

## Quick Reference

| Component | Port | Command |
|-----------|------|---------|
| gRPC Server | 50051 | `python main.py` |
| HTTP Bridge | 8080 | `python http_bridge.py` |
| Frontend | 1420 | `npm run dev` |

**Health Checks:**
- gRPC: Check terminal output for "Ready to process"
- HTTP: `curl http://localhost:8080/health`
- Frontend: Open browser to `http://localhost:1420`

---

*Last Updated: January 9, 2026*
