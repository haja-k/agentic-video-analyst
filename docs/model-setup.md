# Model Setup

## What You Need

Running this on M2 with 16GB RAM, so need models that aren't massive.

## Language Model

**Using: Llama 3.1 8B (already downloaded)**

It's in `backend/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf` - 4.6GB quantized version.

If you need to re-download:
```bash
cd backend/models
curl -L "https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" -o Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

**RAM usage:** ~5GB when loaded

## Speech-to-Text

**Using: Whisper Medium**

Auto-downloads when you first run transcription (~1.5GB).

Sizes if you want to change:
- tiny: 75MB, fast but meh accuracy
- base: 150MB, decent
- medium: 1.5GB, what I'm using
- large: 3GB, overkill for short videos

## Vision Models

**BLIP-2 (image captioning):**  
Auto-downloads from HuggingFace (~2.7GB). Generates scene descriptions for each frame.

**YOLOv8 (object detection):**  
Downloads on first use (~6MB). Identifies and locates objects in frames.

Both in requirements.txt, just pip install.

## 4. Quick Start - Minimum Viable Demo

For fastest setup with minimal storage:

```bash
# 1. LLM: TinyLlama (669MB)
cd backend/models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# 2. Whisper: Use faster-whisper tiny (auto-downloads)
# Already in requirements.txt

# 3. Vision: BLIP base (auto-downloads)
# Already in requirements.txt
```

**Total Storage:** ~1.5GB  
**Total RAM Usage:** ~3-4GB during inference

## 5. Testing Model Installation

```python
# Test script in backend/test_models.py
from llama_cpp import Llama
from faster_whisper import WhisperModel

# Test LLM
llm = Llama(model_path="models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", n_gpu_layers=1)
print("✅ LLM loaded")

# Test Whisper
whisper = WhisperModel("base.en", device="cpu", compute_type="int8")
print("✅ Whisper loaded")
```

## Performance Tips for M2

1. **Use Metal Acceleration:**
   - llama.cpp: Built with `-DLLAMA_METAL=on`
   - Set `n_gpu_layers=1` in Llama initialization

2. **Quantization:**
   - Use Q4_K_M quantization (good balance)
   - Avoid FP16 models (too large)

3. **Batch Processing:**
   - Process video frames in batches
   - Use frame sampling (every Nth frame)

4. **Memory Management:**
   - Unload models when not in use
   - Use `del model` and `gc.collect()`

## Model Configuration

Update `backend/.env`:
```bash
# Use the model you downloaded
LLAMA_MODEL_PATH=models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
# or
LLAMA_MODEL_PATH=models/llama-2-7b-chat.Q4_K_M.gguf

WHISPER_MODEL_PATH=base.en
VISION_MODEL_PATH=Salesforce/blip-image-captioning-base
```
