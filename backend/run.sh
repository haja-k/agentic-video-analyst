#!/bin/bash

# Run script for backend server
# Usage: ./run.sh

set -e

echo "==================================="
echo "AI Video Analysis Backend"
echo "==================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found at venv/"
    echo "Please set up the environment first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if model exists
if [ ! -f "models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" ]; then
    echo ""
    echo "Warning: Llama model not found!"
    echo "Expected: models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    echo ""
    echo "Download with:"
    echo "  cd models && curl -L https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf -o Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf --progress-bar"
    echo ""
    exit 1
fi

echo "Model found: $(ls -lh models/*.gguf | awk '{print $9, $5}')"
echo ""
echo "Starting backend server..."
echo "Press Ctrl+C to stop"
echo ""

python main.py
