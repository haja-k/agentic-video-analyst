"""
Simple test to verify gRPC server is running and accepting connections
"""
import asyncio
import sys
from pathlib import Path
import grpc

# Add parent directory to path to import generated proto files
sys.path.insert(0, str(Path(__file__).parent.parent))

import video_analysis_pb2
import video_analysis_pb2_grpc

async def test_connection():
    """Test if server is accepting connections"""
    try:
        # Set options for larger messages (50MB)
        options = [
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024),
        ]
        
        async with grpc.aio.insecure_channel('localhost:50051', options=options) as channel:
            # Wait for channel to be ready
            await channel.channel_ready()
            print("✓ Successfully connected to gRPC server on localhost:50051")
            
            stub = video_analysis_pb2_grpc.VideoAnalysisServiceStub(channel)
            
            # Test with chat history request (doesn't need video)
            request = video_analysis_pb2.ChatHistoryRequest(
                session_id="test-session",
                limit=5
            )
            
            response = await stub.GetChatHistory(request)
            print(f"✓ Chat history request successful: {len(response.messages)} messages")
            
            print("\n[SUCCESS] gRPC server is running and responding correctly!")
            return True
            
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_connection())
    exit(0 if result else 1)
