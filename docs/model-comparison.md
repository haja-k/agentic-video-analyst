# Model Comparison

## Current Setup

**Llama 3.1 8B (Q4_K_M) - 4.6GB** ✅

Why this one:
- Publicly available (no auth needed)
- Good at query routing and structured output
- ~12-15 tok/s on M2
- 128K context (using 4-8K)
- Leaves RAM for vision models

**Setup:**
- LLM: Llama 3.1 8B (~5GB RAM)
- Vision: BLIP-2 (~2GB) + YOLOv8 (~6MB)
- Speech: Whisper Medium (~1.5GB)
- Total: ~8-9GB RAM used

---

## Speech Model

**Whisper Medium** (what we're using)

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | 75MB | fast | ~80% |
| base | 150MB | good | ~85% |
| **medium** | 1.5GB | decent | **~92%** |
| large | 3GB | slow | ~95% |

Medium gives way better transcripts without being too slow.



---

## Performance (M2, 16GB RAM)

| Component | Load Time | Speed | RAM |
|-----------|-----------|-------|-----|
| Llama 3.1 8B | ~3-5s | 12-15 tok/s | ~5GB |
| Whisper Medium | ~1s | 0.7x realtime | ~1.5GB |
| BLIP-2 | ~3s | 2s/image | ~2GB |
| YOLOv8 | instant | fast | ~6MB |

Everything runs comfortably with RAM to spare.
