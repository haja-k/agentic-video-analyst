#!/bin/bash

# Frontend Development Startup Script

set -e

echo "🚀 Starting Video Analysis AI Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
else
    echo "✅ Dependencies already installed"
fi

# Check if backend is running
if ! curl -s http://localhost:50051/health > /dev/null 2>&1; then
    echo "⚠️  Warning: Backend server doesn't seem to be running on port 50051"
    echo "   Start backend first: cd ../backend && ./run.sh"
fi

# Start development server
echo "🎨 Starting Vite dev server..."
npm run dev
