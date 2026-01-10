"""
HTTP/JSON Bridge for Frontend Communication

This module provides an HTTP server that bridges the frontend React app
with the gRPC backend. It converts HTTP/JSON requests to gRPC calls.

Note: This uses FastAPI which is already in requirements.txt
"""

import asyncio
import json
import logging
from typing import Dict, Any
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn

# Import gRPC client (already in requirements)
import grpc
from generated import video_analysis_pb2, video_analysis_pb2_grpc

logger = logging.getLogger(__name__)

# gRPC connection
channel = None
stub = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage gRPC connection lifecycle."""
    global channel, stub
    # Startup
    channel = grpc.aio.insecure_channel('localhost:50051')
    stub = video_analysis_pb2_grpc.VideoAnalysisServiceStub(channel)
    logger.info("Connected to gRPC backend on port 50051")
    yield
    # Shutdown
    if channel:
        await channel.close()
    logger.info("HTTP bridge stopped")


# FastAPI app
app = FastAPI(title="Video Analysis HTTP Bridge", lifespan=lifespan)
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "http-bridge"}


@app.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    """Handle video upload."""
    try:
        content = await video.read()
        
        grpc_request = video_analysis_pb2.UploadVideoRequest(
            filename=video.filename,
            content=content,
            mime_type=video.content_type or 'video/mp4'
        )
        
        response = await stub.UploadVideo(grpc_request)
        
        # Return metadata from response
        metadata = response.metadata
        return {
            'videoId': response.video_id,
            'filename': video.filename,
            'duration': metadata.duration_seconds,
            'resolution': f"{metadata.width}x{metadata.height}",
            'fps': metadata.fps,
            'fileSize': metadata.file_size
        }
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query_video(request: Dict[str, Any]):
    """Handle single query."""
    logger.info(f"[QUERY] Received request: {request}")
    try:
        logger.info(f"[QUERY] Creating gRPC request with videoId={request.get('videoId')}, query={request.get('query')}")
        grpc_request = video_analysis_pb2.QueryRequest(
            session_id=request.get('sessionId', ''),
            video_id=request['videoId'],
            query=request['query']
        )
        
        logger.info(f"[QUERY] Calling gRPC stub.QueryVideo...")
        response = await stub.QueryVideo(grpc_request)
        logger.info(f"[QUERY] Got gRPC response: {response.response_text[:100]}...")
        
        return {
            'response': response.response_text,
            'actions': [response.type],
            'artifacts': [
                {
                    'type': a.type,
                    'content': a.path,
                    'metadata': dict(a.metadata) if a.metadata else {}
                }
                for a in response.artifacts
            ],
            'sessionId': request.get('sessionId', '')
        }
    except Exception as e:
        logger.error(f"[QUERY] Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stream")
async def stream_query(request: Dict[str, Any]):
    """Handle streaming query."""
    logger.info(f"[STREAM] Received request: {request}")
    try:
        video_id = request.get('videoId')
        query = request.get('query')
        session_id = request.get('sessionId', '')
        
        logger.info(f"[STREAM] videoId={video_id}, query={query}, sessionId={session_id}")
        
        if not video_id:
            logger.error("[STREAM] Missing videoId in request")
            raise HTTPException(status_code=400, detail="Missing videoId")
        
        if not query:
            logger.error("[STREAM] Missing query in request")
            raise HTTPException(status_code=400, detail="Missing query")
        
        grpc_request = video_analysis_pb2.QueryRequest(
            session_id=session_id,
            video_id=video_id,
            query=query
        )
        
        logger.info(f"[STREAM] Calling gRPC stub.StreamQuery...")
        
        async def generate():
            try:
                last_update = None
                async for update in stub.StreamQuery(grpc_request):
                    logger.info(f"[STREAM] Received update from gRPC: {update.response_text[:100]}...")
                    last_update = update
                    # Send progress update
                    chunk = json.dumps({
                        'update': update.response_text,
                        'progress': 0,
                        'sessionId': session_id
                    }) + '\n'
                    yield chunk
                
                # Send final complete response
                if last_update:
                    logger.info(f"[STREAM] Sending final response")
                    final_chunk = json.dumps({
                        'response': last_update.response_text,
                        'actions': [str(last_update.type)],
                        'artifacts': [
                            {
                                'type': a.type,
                                'content': a.path,
                                'metadata': dict(a.metadata) if a.metadata else {}
                            }
                            for a in last_update.artifacts
                        ],
                        'sessionId': session_id
                    }) + '\n'
                    yield final_chunk
                    
                logger.info(f"[STREAM] Streaming complete")
            except Exception as stream_error:
                logger.error(f"[STREAM] Error in generator: {stream_error}", exc_info=True)
                error_chunk = json.dumps({
                    'error': str(stream_error),
                    'sessionId': session_id
                }) + '\n'
                yield error_chunk
        
        return StreamingResponse(generate(), media_type='application/x-ndjson')
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[STREAM] Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history(sessionId: str, limit: int = 50):
    """Handle chat history request."""
    try:
        grpc_request = video_analysis_pb2.ChatHistoryRequest(
            session_id=sessionId,
            limit=limit
        )
        
        response = await stub.GetChatHistory(grpc_request)
        
        messages = [
            {
                'role': m.role,
                'content': m.content,
                'timestamp': m.timestamp,
                'artifacts': [
                    {
                        'type': a.type,
                        'content': a.path,
                        'metadata': dict(a.metadata) if a.metadata else {}
                    }
                    for a in m.artifacts
                ]
            }
            for m in response.messages
        ]
        
        return messages
    except Exception as e:
        logger.error(f"History error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/report")
async def generate_report(request: Dict[str, Any]):
    """Handle report generation."""
    logger.info(f"[REPORT] Received request: {request}")
    try:
        session_id = request.get('sessionId')
        format_type = request.get('format')
        
        logger.info(f"[REPORT] sessionId={session_id}, format={format_type}")
        
        grpc_request = video_analysis_pb2.ReportRequest(
            session_id=session_id,
            format=format_type
        )
        
        logger.info(f"[REPORT] Calling gRPC stub.GenerateReport...")
        response = await stub.GenerateReport(grpc_request)
        logger.info(f"[REPORT] Got gRPC response")
        
        return {
            'filePath': response.file_path if hasattr(response, 'file_path') else '',
            'success': response.status == 'success' if hasattr(response, 'status') else True,
            'message': response.message if hasattr(response, 'message') else 'Report generated'
        }
    except Exception as e:
        logger.error(f"[REPORT] Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 60)
    print("HTTP Bridge Starting")
    print("=" * 60)
    print("Listening on: http://localhost:8080")
    print("gRPC Backend: localhost:50051")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    uvicorn.run(app, host="localhost", port=8080, log_level="info")
