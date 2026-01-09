#!/bin/bash

# Quick model download script for M2 Mac
# Downloads the minimum viable models for a working demo

set -e

echo "📥 Downloading AI Models for Demo..."
echo ""

cd backend/models

echo "Choose your model setup:"
echo ""
echo "Option 1: Llama 3.1 8B (RECOMMENDED - proven & public)"
echo "  - Strong instruction following, good for orchestration"
echo "  - ~4.9GB download, ~5-6GB RAM usage"
echo "  - Vision via BLIP-2 (auto-downloads)"
echo ""
echo "Option 2: Mistral 7B Instruct (Fast alternative)"
echo "  - Excellent instruction following and JSON generation"
echo "  - ~4.4GB download, ~5GB RAM usage"
echo ""
echo "Option 3: Llama 3.2 3B (Smaller/faster)"
echo "  - Good for basic tasks, less RAM needed"
echo "  - ~2GB download, ~3GB RAM usage"
echo ""
read -p "Enter 1, 2, or 3: " choice

if [ "$choice" = "1" ]; then
    # Option 1: Llama 3.1 8B (RECOMMENDED)
    echo ""
    echo "1️⃣  Downloading Llama 3.1 8B Instruct (Q4_K_M)..."
    MODEL_FILE="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    
    if [ ! -f "$MODEL_FILE" ]; then
        curl -L "https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" \
             -o "$MODEL_FILE" \
             --progress-bar
        echo "✅ Llama 3.1 8B downloaded"
    else
        echo "✅ Llama 3.1 8B already exists"
    fi
    
    echo ""
    echo "📊 Storage used: ~4.9GB"
    echo "💾 RAM required: ~5-6GB during inference"
    echo "🎯 Model: Llama 3.1 8B Instruct (excellent instruction following)"
    echo "👁️  Vision: Use BLIP-2 (auto-downloads when needed)"
    
elif [ "$choice" = "2" ]; then
    # Option 2: Mistral 7B
    echo ""
    echo "2️⃣  Downloading Mistral 7B Instruct v0.2 (Q4_K_M)..."
    MODEL_FILE="mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    
    if [ ! -f "$MODEL_FILE" ]; then
        curl -L "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf" \
             -o "$MODEL_FILE" \
             --progress-bar
        echo "✅ Mistral 7B downloaded"
    else
        echo "✅ Mistral 7B already exists"
    fi
    
    echo ""
    echo "📊 Storage used: ~4.4GB"
    echo "💾 RAM required: ~5GB during inference"
    echo "🎯 Model: Mistral 7B Instruct v0.2 (fast & efficient)"
    echo "👁️  Vision: Use BLIP-2 (auto-downloads when needed)"
    
elif [ "$choice" = "3" ]; then
    # Option 3: Llama 3.2 3B
    echo ""
    echo "3️⃣  Downloading Llama 3.2 3B Instruct (Q4_K_M)..."
    MODEL_FILE="llama-3.2-3b-instruct.Q4_K_M.gguf"
    
    if [ ! -f "$MODEL_FILE" ]; then
        curl -L "https://huggingface.co/lmstudio-community/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf" \
             -o "$MODEL_FILE" \
             --progress-bar
        echo "✅ Llama 3.2 3B downloaded"
    else
        echo "✅ Llama 3.2 3B already exists"
    fi
    
    echo ""
    echo "📊 Storage used: ~2GB"
    echo "💾 RAM required: ~3GB during inference"
    echo "🎯 Model: Llama 3.2 3B Instruct (compact & fast)"
    echo "👁️  Vision: Use BLIP-2 (auto-downloads when needed)"
    
else
    echo "Invalid choice. Run script again."
    exit 1
fi

echo ""
echo "2️⃣  Whisper Medium will auto-download on first use (~1.5GB)"
echo "3️⃣  Vision models (BLIP-2/YOLO if needed) will auto-download"
echo ""
echo "✅ Model setup complete!"
echo ""
echo "Next steps:"
echo "1. Update backend/.env with model path"
echo "2. Test: source venv/bin/activate && python test_models.py"
