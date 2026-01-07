#!/bin/bash

# Setup script for MacBook Air M2
# This script sets up the Python virtual environment and installs all dependencies

set -e  # Exit on error

echo "🚀 Setting up AI Video Analysis Backend for M2 Mac..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Create virtual environment
echo "📦 Creating virtual environment..."
cd backend
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install basic dependencies first
echo "📥 Installing basic dependencies..."
pip install wheel setuptools

# Install llama-cpp-python with Metal support for M2
echo "🦙 Installing llama-cpp-python with Metal acceleration for M2..."
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python==0.2.90 --force-reinstall --no-cache-dir

# Install remaining dependencies
echo "📥 Installing remaining dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p models
mkdir -p data
mkdir -p uploads

# Copy .env.example to .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file (please configure as needed)"
fi

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Download AI models (see docs/model-setup.md)"
echo "2. Activate venv: source backend/venv/bin/activate"
echo "3. Run backend: python backend/main.py"
echo ""
echo "🎯 For M2 optimization, llama.cpp is configured with Metal acceleration"
