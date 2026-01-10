#!/bin/bash

# Complete Application Startup Script

set -e

echo "🚀 Starting Video Analysis AI - Full Stack"
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

# Terminal commands
BACKEND_CMD="cd backend && source venv/bin/activate && python main.py"
BRIDGE_CMD="cd backend && source venv/bin/activate && python http_bridge.py"
FRONTEND_CMD="cd frontend && npm run dev"

echo "📋 This will start 3 services:"
echo "   1. gRPC Backend (port 50051)"
echo "   2. HTTP Bridge (port 8080)"
echo "   3. Frontend Dev Server (port 1420)"
echo ""
echo "⚠️  You'll need 3 terminal windows/tabs."
echo ""
echo "📝 Run these commands in separate terminals:"
echo ""
echo "Terminal 1 (Backend):"
echo "  $BACKEND_CMD"
echo ""
echo "Terminal 2 (HTTP Bridge):"
echo "  $BRIDGE_CMD"
echo ""
echo "Terminal 3 (Frontend):"
echo "  $FRONTEND_CMD"
echo ""
echo "Or use a terminal multiplexer like tmux:"
echo ""
echo "# Start all services in tmux"
echo "tmux new-session -d -s video-ai '$BACKEND_CMD'"
echo "tmux split-window -h '$BRIDGE_CMD'"
echo "tmux split-window -v '$FRONTEND_CMD'"
echo "tmux attach -t video-ai"
echo ""
echo "🌐 Once all services are running, open http://localhost:1420"
