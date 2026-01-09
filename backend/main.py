"""
Main entry point for the AI Video Analysis Backend
"""
import asyncio
import logging
from concurrent import futures
from pathlib import Path
import grpc
import uuid
import json
from datetime import datetime
from typing import Dict, List
import cv2

from rich.console import Console
from rich.logging import RichHandler

from agents.orchestrator_agent import OrchestratorAgent
from agents.transcription_agent import TranscriptionAgent
from agents.vision_agent import VisionAgent
from agents.generation_agent import GenerationAgent

from mcp_servers.transcription_mcp import TranscriptionMCPServer
from mcp_servers.vision_mcp import VisionMCPServer
from mcp_servers.generation_mcp import GenerationMCPServer

import video_analysis_pb2
import video_analysis_pb2_grpc

# Initialize rich console for better logging
console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)

logger = logging.getLogger(__name__)


class VideoAnalysisServicer(video_analysis_pb2_grpc.VideoAnalysisServiceServicer):
    """gRPC service implementation for video analysis"""
    
    def __init__(self, orchestrator: OrchestratorAgent):
        self.orchestrator = orchestrator
        self.sessions: Dict[str, dict] = {}  # session_id -> session data
        self.videos: Dict[str, str] = {}  # video_id -> file path
        self.chat_history: Dict[str, List[dict]] = {}  # session_id -> messages
        self.session_results: Dict[str, Dict] = {}  # session_id -> accumulated results
        
        # Ensure uploads directory exists
        self.uploads_dir = Path("uploads")
        self.uploads_dir.mkdir(exist_ok=True)
    
    async def UploadVideo(self, request, context):
        """Handle video upload and extract metadata"""
        try:
            # Generate unique video ID
            video_id = str(uuid.uuid4())
            
            # Save video file
            video_path = self.uploads_dir / f"{video_id}_{request.filename}"
            video_path.write_bytes(request.content)
            
            # Extract metadata using OpenCV
            cap = cv2.VideoCapture(str(video_path))
            
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = int(frame_count / fps) if fps > 0 else 0
            
            cap.release()
            
            # Store video reference
            self.videos[video_id] = str(video_path)
            
            logger.info(f"Video uploaded: {video_id} ({request.filename})")
            
            return video_analysis_pb2.UploadVideoResponse(
                video_id=video_id,
                status="success",
                message=f"Video uploaded successfully: {request.filename}",
                metadata=video_analysis_pb2.VideoMetadata(
                    duration_seconds=duration,
                    width=width,
                    height=height,
                    fps=fps,
                    file_size=len(request.content)
                )
            )
            
        except Exception as e:
            logger.error(f"Video upload failed: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return video_analysis_pb2.UploadVideoResponse(
                video_id="",
                status="error",
                message=f"Upload failed: {str(e)}"
            )
    
    async def QueryVideo(self, request, context):
        """Process a single query about the video"""
        try:
            session_id = request.session_id or str(uuid.uuid4())
            
            # Initialize session if needed
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "video_id": request.video_id,
                    "created_at": datetime.now().isoformat()
                }
                self.chat_history[session_id] = []
            
            # Get video path
            video_path = self.videos.get(request.video_id)
            if not video_path:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Video not found")
                return video_analysis_pb2.QueryResponse(
                    response_id="",
                    query=request.query,
                    response_text="Video not found. Please upload a video first.",
                    type=video_analysis_pb2.ResponseType.TEXT
                )
            
            # Add user message to history
            self.chat_history[session_id].append({
                "role": "user",
                "content": request.query,
                "timestamp": datetime.now().isoformat()
            })
            
            # Process query through orchestrator
            logger.info(f"Processing query: {request.query}")
            result = await self.orchestrator.process({
                "query": request.query,
                "video_path": video_path
            })
            
            # Store results in session for report generation
            if session_id not in self.session_results:
                self.session_results[session_id] = {}
            
            # Accumulate results from this query
            query_results = result.get("results", {})
            if "transcription" in query_results:
                self.session_results[session_id]["transcription"] = query_results["transcription"]
            if "vision" in query_results:
                self.session_results[session_id]["vision_results"] = query_results["vision"]
            if "summary" in query_results:
                self.session_results[session_id]["summary"] = query_results["summary"]
            
            # Map response type
            response_type = self._map_response_type(result.get("actions_taken", []))
            
            # Create artifacts from results
            artifacts = self._create_artifacts(result)
            
            # Add assistant message to history
            self.chat_history[session_id].append({
                "role": "assistant",
                "content": result["response"],
                "timestamp": datetime.now().isoformat(),
                "artifacts": [{"type": a.type, "path": a.path} for a in artifacts]
            })
            
            response_id = str(uuid.uuid4())
            
            return video_analysis_pb2.QueryResponse(
                response_id=response_id,
                query=request.query,
                response_text=result["response"],
                type=response_type,
                artifacts=artifacts,
                confidence=1.0
            )
            
        except Exception as e:
            logger.error(f"Query processing failed: {e}", exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return video_analysis_pb2.QueryResponse(
                response_id="",
                query=request.query,
                response_text=f"Error processing query: {str(e)}",
                type=video_analysis_pb2.ResponseType.TEXT
            )
    
    async def StreamQuery(self, request, context):
        """Stream responses for long-running queries"""
        try:
            session_id = request.session_id or str(uuid.uuid4())
            
            # Initialize session if needed
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "video_id": request.video_id,
                    "created_at": datetime.now().isoformat()
                }
                self.chat_history[session_id] = []
            
            # Get video path
            video_path = self.videos.get(request.video_id)
            if not video_path:
                yield video_analysis_pb2.QueryResponse(
                    response_id="",
                    query=request.query,
                    response_text="Video not found. Please upload a video first.",
                    type=video_analysis_pb2.ResponseType.TEXT
                )
                return
            
            # Add user message to history
            self.chat_history[session_id].append({
                "role": "user",
                "content": request.query,
                "timestamp": datetime.now().isoformat()
            })
            
            # Send initial response
            yield video_analysis_pb2.QueryResponse(
                response_id=str(uuid.uuid4()),
                query=request.query,
                response_text="Processing your query...",
                type=video_analysis_pb2.ResponseType.TEXT,
                confidence=0.0
            )
            
            # Process query through orchestrator
            result = await self.orchestrator.process({
                "query": request.query,
                "video_path": video_path
            })
            
            # Map response type and create artifacts
            response_type = self._map_response_type(result.get("actions_taken", []))
            artifacts = self._create_artifacts(result)
            
            # Add to history
            self.chat_history[session_id].append({
                "role": "assistant",
                "content": result["response"],
                "timestamp": datetime.now().isoformat(),
                "artifacts": [{"type": a.type, "path": a.path} for a in artifacts]
            })
            
            # Send final response
            yield video_analysis_pb2.QueryResponse(
                response_id=str(uuid.uuid4()),
                query=request.query,
                response_text=result["response"],
                type=response_type,
                artifacts=artifacts,
                confidence=1.0
            )
            
        except Exception as e:
            logger.error(f"Stream query failed: {e}", exc_info=True)
            yield video_analysis_pb2.QueryResponse(
                response_id="",
                query=request.query,
                response_text=f"Error: {str(e)}",
                type=video_analysis_pb2.ResponseType.TEXT
            )
    
    async def GetChatHistory(self, request, context):
        """Retrieve chat history for a session"""
        try:
            session_id = request.session_id
            
            if session_id not in self.chat_history:
                return video_analysis_pb2.ChatHistoryResponse(messages=[])
            
            messages = []
            history = self.chat_history[session_id]
            
            # Apply limit if specified
            limit = request.limit if request.limit > 0 else len(history)
            history_slice = history[-limit:]
            
            for msg in history_slice:
                # Convert artifacts if present
                artifacts = []
                if "artifacts" in msg:
                    for art in msg["artifacts"]:
                        artifacts.append(video_analysis_pb2.Artifact(
                            type=art["type"],
                            path=art["path"]
                        ))
                
                messages.append(video_analysis_pb2.ChatMessage(
                    message_id=str(uuid.uuid4()),
                    role=msg["role"],
                    content=msg["content"],
                    timestamp=int(datetime.fromisoformat(msg["timestamp"]).timestamp()),
                    artifacts=artifacts
                ))
            
            return video_analysis_pb2.ChatHistoryResponse(messages=messages)
            
        except Exception as e:
            logger.error(f"Failed to get chat history: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return video_analysis_pb2.ChatHistoryResponse(messages=[])
    
    async def GenerateReport(self, request, context):
        """Generate PDF or PowerPoint report"""
        try:
            # Build content for report generation
            content_dict = {
                "title": request.content.title,
                "sections": list(request.content.sections),
                "data": dict(request.content.data)
            }
            
            # Get session context with actual analysis results
            session_context = self.session_results.get(request.session_id, {})
            
            # Use generation agent directly through orchestrator context
            query = f"Generate a {request.format.upper()} report with title: {content_dict['title']}"
            
            result = await self.orchestrator.process({
                "query": query,
                "video_path": "",  # Report generation doesn't need video
                "context": session_context  # Pass accumulated context
            })
            
            # Extract file path from results
            file_path = ""
            results = result.get("results", {})
            
            # Check for PDF or PPTX in results
            if request.format.lower() == "pdf" and "pdf" in results:
                file_path = results["pdf"].get("output_path", "")
            elif request.format.lower() == "pptx" and "pptx" in results:
                file_path = results["pptx"].get("output_path", "")
            
            if file_path and Path(file_path).exists():
                file_data = Path(file_path).read_bytes()
                
                return video_analysis_pb2.ReportResponse(
                    status="success",
                    file_path=file_path,
                    file_data=file_data,
                    message=f"Report generated successfully: {file_path}"
                )
            else:
                logger.error(f"Report generation failed. File path: {file_path}, Results: {results.keys()}")
                return video_analysis_pb2.ReportResponse(
                    status="error",
                    file_path="",
                    message=f"Report generation failed - no file produced"
                )
                
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return video_analysis_pb2.ReportResponse(
                status="error",
                file_path="",
                message=f"Error: {str(e)}"
            )
    
    def _map_response_type(self, actions: List[str]) -> int:
        """Map action types to proto ResponseType enum"""
        if not actions:
            return video_analysis_pb2.ResponseType.TEXT
        
        # Check most recent action
        last_action = actions[-1] if actions else ""
        
        if "transcribe" in last_action:
            return video_analysis_pb2.ResponseType.TRANSCRIPTION
        elif "detect_objects" in last_action:
            return video_analysis_pb2.ResponseType.OBJECT_DETECTION
        elif "caption" in last_action or "describe" in last_action:
            return video_analysis_pb2.ResponseType.IMAGE_CAPTION
        elif "graph" in last_action or "chart" in last_action:
            return video_analysis_pb2.ResponseType.GRAPH_ANALYSIS
        elif "summarize" in last_action:
            return video_analysis_pb2.ResponseType.SUMMARY
        else:
            return video_analysis_pb2.ResponseType.TEXT
    
    def _create_artifacts(self, result: dict) -> List:
        """Create Artifact messages from orchestrator results"""
        artifacts = []
        
        # Check for generated files in artifacts
        for artifact in result.get("artifacts", []):
            artifact_type = artifact.get("type", "")
            artifact_path = artifact.get("path", "")
            
            if artifact_path and Path(artifact_path).exists():
                # Read file data
                file_data = Path(artifact_path).read_bytes()
                
                artifacts.append(video_analysis_pb2.Artifact(
                    type=artifact_type,
                    path=artifact_path,
                    data=file_data
                ))
        
        # Check for JSON results (transcription, vision)
        if "transcription" in result.get("context", {}):
            trans_data = json.dumps(result["context"]["transcription"]).encode()
            artifacts.append(video_analysis_pb2.Artifact(
                type="json",
                path="transcription.json",
                data=trans_data
            ))
        
        if "vision_results" in result.get("context", {}):
            vision_data = json.dumps(result["context"]["vision_results"]).encode()
            artifacts.append(video_analysis_pb2.Artifact(
                type="json",
                path="vision_results.json",
                data=vision_data
            ))
        
        return artifacts


class BackendServer:
    """Main backend server orchestrating all agents and MCP servers"""
    
    def __init__(self, port: int = 50051):
        self.port = port
        self.server = None
        self.orchestrator = None
        self.transcription_mcp = None
        self.vision_mcp = None
        self.generation_mcp = None
        
    async def initialize(self):
        """Initialize all agents and MCP servers"""
        console.print("[bold green]Initializing AI Video Analysis Backend...[/bold green]\n")
        
        try:
            # Find Llama model
            model_path = Path("models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")
            if not model_path.exists():
                logger.error("Llama model not found at models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")
                logger.info("Please download the model using: ./download-models.sh")
                raise FileNotFoundError("Llama model not found")
            
            # Initialize specialized agents
            console.print("Initializing specialized agents...")
            
            transcription_agent = TranscriptionAgent(model_size="medium")
            await transcription_agent.initialize()
            console.print("  ✓ Transcription agent ready", style="green")
            
            vision_agent = VisionAgent()
            await vision_agent.initialize()
            console.print("  ✓ Vision agent ready", style="green")
            
            generation_agent = GenerationAgent()
            await generation_agent.initialize()
            console.print("  ✓ Generation agent ready", style="green")
            
            # Initialize MCP servers wrapping the agents
            console.print("\nInitializing MCP servers...")
            
            self.transcription_mcp = TranscriptionMCPServer(agent=transcription_agent)
            await self.transcription_mcp.initialize()
            console.print("  ✓ Transcription MCP server ready", style="green")
            
            self.vision_mcp = VisionMCPServer(agent=vision_agent)
            await self.vision_mcp.initialize()
            console.print("  ✓ Vision MCP server ready", style="green")
            
            self.generation_mcp = GenerationMCPServer(agent=generation_agent)
            await self.generation_mcp.initialize()
            console.print("  ✓ Generation MCP server ready", style="green")
            
            # Initialize orchestrator with MCP servers
            console.print("\nInitializing orchestrator...")
            self.orchestrator = OrchestratorAgent(
                model_path=str(model_path),
                transcription_mcp=self.transcription_mcp,
                vision_mcp=self.vision_mcp,
                generation_mcp=self.generation_mcp
            )
            await self.orchestrator.initialize()
            console.print("  ✓ Orchestrator ready", style="green")
            
            console.print("\n[bold green]✓ All agents and MCP servers initialized successfully[/bold green]")
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}", exc_info=True)
            raise
        
    async def start(self):
        """Start the gRPC server"""
        await self.initialize()
        
        # Set larger message sizes (50MB) to handle video uploads
        options = [
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024),
        ]
        
        self.server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=10),
            options=options
        )
        
        # Add VideoAnalysis service
        servicer = VideoAnalysisServicer(orchestrator=self.orchestrator)
        video_analysis_pb2_grpc.add_VideoAnalysisServiceServicer_to_server(
            servicer, self.server
        )
        
        self.server.add_insecure_port(f'[::]:{self.port}')
        await self.server.start()
        
        console.print(f"\n[bold green]✓ gRPC server started on port {self.port}[/bold green]")
        console.print("\n[bold cyan]Ready to process video queries via gRPC![/bold cyan]")
        console.print("[dim]Press Ctrl+C to stop[/dim]\n")
        
        await self.server.wait_for_termination()
        
    async def stop(self):
        """Graceful shutdown"""
        console.print("\n[yellow]Shutting down...[/yellow]")
        
        if self.orchestrator:
            await self.orchestrator.cleanup()
        
        # MCP servers will be cleaned up through their wrapped agents
        if self.transcription_mcp and self.transcription_mcp.agent:
            await self.transcription_mcp.agent.cleanup()
        if self.vision_mcp and self.vision_mcp.agent:
            await self.vision_mcp.agent.cleanup()
        if self.generation_mcp and self.generation_mcp.agent:
            await self.generation_mcp.agent.cleanup()
        
        if self.server:
            await self.server.stop(grace=5)
        
        console.print("[green]Shutdown complete[/green]")


async def main():
    """Main entry point"""
    server = BackendServer(port=50051)
    
    try:
        await server.start()
    except KeyboardInterrupt:
        await server.stop()
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        await server.stop()
        raise


if __name__ == "__main__":
    asyncio.run(main())
