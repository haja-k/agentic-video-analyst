#!/bin/bash

# Test all agents in sequence
# Usage: ./test_all.sh [video_path]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIDEO_PATH="${1:-}"

echo "==================================="
echo "AI Video Analysis - Full Test Suite"
echo "==================================="
echo ""

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/../venv" ]; then
    echo "Error: Virtual environment not found"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$SCRIPT_DIR/../venv/bin/activate"

echo ""
echo "===================================="
echo "Test 1: Orchestrator Intent Analysis"
echo "===================================="
echo ""
python test_orchestrator.py --intent-only

if [ -n "$VIDEO_PATH" ] && [ -f "$VIDEO_PATH" ]; then
    echo ""
    echo "===================================="
    echo "Test 2: Full Orchestrator with Video"
    echo "===================================="
    echo ""
    python test_orchestrator.py "$VIDEO_PATH"
    
    echo ""
    echo "===================================="
    echo "Test 3: Transcription Agent"
    echo "===================================="
    echo ""
    python test_transcription.py "$VIDEO_PATH"
    
    echo ""
    echo "===================================="
    echo "Test 4: Vision Agent"
    echo "===================================="
    echo ""
    python test_vision.py "$VIDEO_PATH"
    
    echo ""
    echo "===================================="
    echo "Test 5: Generation Agent"
    echo "===================================="
    echo ""
    python test_generation.py
else
    echo ""
    echo "No video provided. Skipping full tests."
    echo "Usage: ./test_all.sh <video_path>"
fi

echo ""
echo "===================================="
echo "All tests complete!"
echo "===================================="
