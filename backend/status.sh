#!/bin/bash

# Display project structure and status
# Usage: ./status.sh

echo "======================================"
echo "AI Video Analysis - Project Status"
echo "======================================"
echo ""

# Check virtual environment
if [ -d "venv" ]; then
    echo "✓ Virtual environment: venv/"
else
    echo "✗ Virtual environment not found"
fi

# Check model
if [ -f "models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" ]; then
    SIZE=$(ls -lh models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf | awk '{print $5}')
    echo "✓ Llama model: $SIZE"
else
    echo "✗ Llama model not found"
fi

echo ""
echo "Agents:"
echo "  ✓ TranscriptionAgent (Whisper)"
echo "  ✓ VisionAgent (BLIP-2 + YOLOv8)"
echo "  ✓ GenerationAgent (PDF/PPT)"
echo "  ✓ OrchestratorAgent (Llama 3.1 8B)"

echo ""
echo "MCP Servers:"
echo "  ✓ Base MCP framework"
echo "  ✓ TranscriptionMCP"
echo "  ✓ VisionMCP"
echo "  ✓ GenerationMCP"

echo ""
echo "Test Scripts:"
echo "  - test_orchestrator.py (intent analysis & full workflow)"
echo "  - test_transcription.py"
echo "  - test_vision.py"
echo "  - test_generation.py"
echo "  - test_all.sh (run all tests)"

echo ""
echo "Run Scripts:"
echo "  - ./run.sh (start backend server)"
echo "  - ./tests/test_all.sh [video] (test suite)"

echo ""
echo "Documentation:"
echo "  - README.md (main documentation)"
echo "  - QUICKSTART.md (quick start guide)"

echo ""
echo "======================================"
echo "Quick Start:"
echo "======================================"
echo ""
echo "1. Test orchestrator:"
echo "   cd tests && source ../venv/bin/activate"
echo "   python test_orchestrator.py --intent-only"
echo ""
echo "2. Start backend:"
echo "   ./run.sh"
echo ""
echo "3. Run all tests:"
echo "   cd tests && ./test_all.sh /path/to/video.mp4"
echo ""
