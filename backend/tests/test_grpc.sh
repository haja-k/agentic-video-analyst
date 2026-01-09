#!/bin/bash
# Simple test script for gRPC service

cd "/Users/hajjariah/Documents/MyGit/Intel Assignment/backend"
source venv/bin/activate

echo "Starting gRPC server in background..."
nohup python main.py > tests/results/server.log 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"

echo "Waiting for server to initialize (30 seconds)..."
sleep 30

echo ""
echo "==== Testing Connection ===="
python tests/test_connection.py

if [ $? -eq 0 ]; then
    echo ""
    echo "==== Running Full Test Suite ===="
    python tests/test_grpc_client.py uploads/SolarPower.mp4
fi

echo ""
echo "Stopping server (PID: $SERVER_PID)..."
kill $SERVER_PID 2>/dev/null

echo "Test complete!"
