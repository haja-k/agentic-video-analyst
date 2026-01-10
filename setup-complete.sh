#!/bin/bash

# Complete Setup & Test Script
# Run from project root

set -e

echo "=================================================="
echo "Video Analysis AI - Complete Setup & Test"
echo "=================================================="
echo ""

# Check current directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Run this script from the project root"
    exit 1
fi

echo "📋 Step 1: Installing Backend Dependencies"
echo "--------------------------------------------------"
cd backend

if [ ! -d "venv" ]; then
    echo "❌ Error: Python virtual environment not found"
    echo "   Run backend setup first: cd backend && python3.12 -m venv venv"
    exit 1
fi

source venv/bin/activate

echo "✅ Backend dependencies already installed (FastAPI, gRPC, etc.)"
echo "   HTTP bridge uses FastAPI which is already in requirements.txt"
echo ""

cd ..

echo "📋 Step 2: Installing Frontend Dependencies"
echo "--------------------------------------------------"
cd frontend

if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found"
    exit 1
fi

echo "Installing npm packages (this may take a few minutes)..."
npm install

echo "✅ Frontend dependencies installed"
echo ""

cd ..

echo "=================================================="
echo "✅ Installation Complete!"
echo "=================================================="
echo ""
echo "🚀 To run the application:"
echo ""
echo "You need 3 terminal windows:"
echo ""
echo "Terminal 1 - Backend (gRPC):"
echo "  cd backend && source venv/bin/activate && python main.py"
echo ""
echo "Terminal 2 - HTTP Bridge:"
echo "  cd backend && source venv/bin/activate && python http_bridge.py"
echo ""
echo "Terminal 3 - Frontend:"
echo "  cd frontend && npm run dev"
echo ""
echo "Then open: http://localhost:1420"
echo ""
echo "Or use the quick start script: ./start-all.sh"
echo ""
