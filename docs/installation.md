# Installation Guide

Complete installation instructions for the Agentic Video Analyst system.

---

## System Requirements

### Hardware Requirements

**Minimum:**
- Apple Silicon (M1/M2/M3) Mac
- 8GB RAM
- 15GB free disk space
- Metal-compatible GPU

**Recommended:**
- M2 or newer
- 16GB+ RAM
- 20GB free disk space (for models and videos)
- SSD storage

### Software Requirements

- **macOS:** 12.0 (Monterey) or later
- **Python:** 3.12.x
- **Node.js:** 18.x or later
- **npm:** 9.x or later
- **Git:** 2.x or later

---

## Step-by-Step Installation

### 1. Install System Dependencies

#### Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install Python 3.12

```bash
brew install python@3.12
```

Verify installation:
```bash
python3.12 --version
# Output: Python 3.12.x
```

#### Install Node.js

```bash
brew install node@18
```

Verify installation:
```bash
node --version  # Should show v18.x.x
npm --version   # Should show 9.x.x
```

### 2. Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd "Intel Assignment"
```

### 3. Backend Setup

#### Create Virtual Environment

```bash
cd backend

# Create venv
python3.12 -m venv venv

# Activate venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

#### Install Python Dependencies

```bash
# Install all requirements
pip install -r requirements.txt
```

**Key Dependencies Installed:**
- `llama-cpp-python` - Metal-accelerated LLM inference
- `whisper` - Speech-to-text transcription
- `transformers` - BLIP image captioning
- `ultralytics` - YOLOv8 object detection
- `grpcio` - gRPC server
- `fastapi` - HTTP bridge
- `opencv-python` - Video processing
- `reportlab` - PDF generation
- `python-pptx` - PowerPoint generation

#### Verify Installation

```bash
python -c "import llama_cpp; import whisper; import grpc; print('✓ All imports successful')"
```

### 4. Download AI Models

#### Automatic Download (Recommended)

```bash
# From backend directory
chmod +x download-models.sh
./download-models.sh
```

This downloads:
1. **Llama 3.1 8B Instruct** (Q4_K_M) - 4.6GB
2. **YOLOv8 Nano** - 6MB

#### Manual Download

If automatic download fails:

**Llama Model:**
```bash
cd backend/models
curl -L -o Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf \
  https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

**YOLOv8:**
```bash
cd backend/models
curl -L -o yolov8n.pt \
  https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

#### Whisper Model (Auto-downloads on first use)

Whisper Medium model (~1.5GB) downloads automatically when first used. To pre-download:

```bash
python -c "import whisper; whisper.load_model('medium')"
```

#### BLIP Model (Auto-downloads on first use)

BLIP model (~1GB) downloads automatically from HuggingFace on first use.

#### Verify Models

```bash
ls -lh backend/models/
```

Expected output:
```
Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf  (4.6GB)
yolov8n.pt                               (6.0MB)
```

### 5. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

**Key Dependencies:**
- React 18
- TypeScript
- Vite (build tool)
- TailwindCSS (styling)
- Tauri (desktop wrapper)

#### Build Frontend (Optional)

```bash
npm run build
```

This creates an optimized production build in `frontend/dist/`.

### 6. Create Required Directories

```bash
# From project root
mkdir -p backend/uploads
mkdir -p backend/logs
mkdir -p backend/tests/results
mkdir -p backend/data
```

### 7. Environment Configuration (Optional)

Create `.env` file for custom configuration:

```bash
cd backend
cp .env.example .env
```

Edit `.env` to customize:
```bash
# Model paths
LLAMA_MODEL_PATH=models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
YOLO_MODEL_PATH=models/yolov8n.pt

# Server ports
GRPC_PORT=50051
HTTP_PORT=8080
FRONTEND_PORT=1420

# Model settings
LLAMA_N_CTX=4096
LLAMA_N_GPU_LAYERS=-1  # -1 = use all GPU layers
WHISPER_MODEL=medium
```

---

## Verify Installation

### Quick Backend Test

```bash
cd backend
source venv/bin/activate

# Test imports
python -c "
import llama_cpp
import whisper
import grpc
import cv2
from ultralytics import YOLO
print('✓ All imports successful')
"
```

### Test Model Loading

```bash
cd backend/tests
source ../venv/bin/activate

# Test Llama model
python -c "
from llama_cpp import Llama
llm = Llama(model_path='../models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf', n_ctx=2048, n_gpu_layers=-1)
print('✓ Llama model loaded')
"

# Test YOLO model
python -c "
from ultralytics import YOLO
model = YOLO('../models/yolov8n.pt')
print('✓ YOLO model loaded')
"
```

### Run Test Suite

```bash
cd backend/tests
source ../venv/bin/activate

# Run all tests
./test_all.sh
```

Expected output:
```
✓ Transcription test passed
✓ Vision test passed
✓ Generation test passed
✓ Orchestrator test passed
✓ gRPC test passed
```

---

## Post-Installation

### Start the System

```bash
# Option 1: All-in-one script
./start-all.sh

# Option 2: Manual (3 terminals)
# Terminal 1:
cd backend && source venv/bin/activate && python main.py

# Terminal 2:
cd backend && source venv/bin/activate && python http_bridge.py

# Terminal 3:
cd frontend && npm run dev
```

### Verify System Health

**Check gRPC Server:**
```bash
# Should see: "✓ gRPC server started on port 50051"
# Should see: "Loaded X video mappings from registry"
```

**Check HTTP Bridge:**
```bash
curl http://localhost:8080/health
# Output: {"status":"ok","service":"http-bridge"}
```

**Check Frontend:**
- Open browser to `http://localhost:1420`
- Should see "Video Analysis AI" interface

---

## Troubleshooting Installation

### Python Version Issues

```bash
# Check Python version
python3.12 --version

# If not found, install:
brew install python@3.12

# Link it:
brew link python@3.12
```

### Metal Acceleration Not Working

```bash
# Reinstall llama-cpp-python with Metal support
pip uninstall llama-cpp-python -y
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --no-cache-dir
```

### Model Download Fails

**Use wget instead of curl:**
```bash
brew install wget
cd backend/models
wget https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

**Or download via browser:**
1. Visit the HuggingFace link
2. Download manually
3. Move to `backend/models/`

### Import Errors

```bash
# Reinstall requirements
cd backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Permission Errors

```bash
# Fix script permissions
chmod +x backend/download-models.sh
chmod +x start-all.sh
chmod +x backend/run.sh
```

### Node/npm Issues

```bash
# Clear npm cache
npm cache clean --force

# Reinstall node_modules
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Uninstallation

### Remove Project

```bash
cd ..
rm -rf "Intel Assignment"
```

### Remove Models Only

```bash
cd "Intel Assignment/backend"
rm -rf models/*
rm -rf ~/.cache/huggingface  # Cached models
rm -rf ~/.cache/whisper      # Whisper cache
```

### Keep Project, Remove venv

```bash
cd backend
rm -rf venv
```

---

## Next Steps

- [Getting Started Guide](getting-started.md) - First steps after installation
- [Architecture Documentation](architecture.md) - System overview
- [Development Guide](development-guide.md) - Contributing to the project

---

*Last Updated: January 9, 2026*
