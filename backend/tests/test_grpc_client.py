"""
Test client for gRPC Video Analysis Service
"""
import asyncio
import grpc
from pathlib import Path
import sys
# Add parent directory to path to import generated proto files
sys.path.insert(0, str(Path(__file__).parent.parent))
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from generated import video_analysis_pb2
from generated import video_analysis_pb2_grpc

console = Console()


async def test_upload_video(stub, video_path: str):
    """Test video upload"""
    console.print("\n[bold cyan]Testing Video Upload...[/bold cyan]")
    
    video_file = Path(video_path)
    if not video_file.exists():
        console.print(f"[red]Error: Video file not found: {video_path}[/red]")
        return None
    
    # Read video content
    video_content = video_file.read_bytes()
    
    # Create upload request
    request = video_analysis_pb2.UploadVideoRequest(
        filename=video_file.name,
        content=video_content,
        mime_type="video/mp4"
    )
    
    # Upload video
    response = await stub.UploadVideo(request)
    
    if response.status == "success":
        console.print(f"[green]✓ Video uploaded successfully[/green]")
        console.print(f"  Video ID: {response.video_id}")
        console.print(f"  Duration: {response.metadata.duration_seconds}s")
        console.print(f"  Resolution: {response.metadata.width}x{response.metadata.height}")
        console.print(f"  FPS: {response.metadata.fps:.2f}")
        console.print(f"  Size: {response.metadata.file_size / 1024 / 1024:.2f} MB")
        return response.video_id
    else:
        console.print(f"[red]✗ Upload failed: {response.message}[/red]")
        return None


async def test_query_video(stub, video_id: str, session_id: str, query: str):
    """Test single query"""
    console.print(f"\n[bold cyan]Testing Query: {query}[/bold cyan]")
    
    request = video_analysis_pb2.QueryRequest(
        session_id=session_id,
        video_id=video_id,
        query=query
    )
    
    response = await stub.QueryVideo(request)
    
    # Display response
    table = Table(title="Query Response", show_header=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Response ID", response.response_id)
    table.add_row("Query", response.query)
    table.add_row("Type", str(video_analysis_pb2.ResponseType.Name(response.type)))
    table.add_row("Confidence", f"{response.confidence:.2f}")
    table.add_row("Artifacts", str(len(response.artifacts)))
    
    console.print(table)
    
    # Display response text
    console.print(Panel(
        response.response_text,
        title="Response",
        border_style="green"
    ))
    
    # Display artifacts
    if response.artifacts:
        console.print("\n[bold]Artifacts:[/bold]")
        for artifact in response.artifacts:
            console.print(f"  • {artifact.type}: {artifact.path} ({len(artifact.data)} bytes)")


async def test_stream_query(stub, video_id: str, session_id: str, query: str):
    """Test streaming query"""
    console.print(f"\n[bold cyan]Testing Stream Query: {query}[/bold cyan]")
    
    request = video_analysis_pb2.QueryRequest(
        session_id=session_id,
        video_id=video_id,
        query=query
    )
    
    async for response in stub.StreamQuery(request):
        console.print(f"[dim]Stream update:[/dim] {response.response_text[:100]}...")
        if response.confidence >= 1.0:
            # Final response
            console.print(Panel(
                response.response_text,
                title="Final Response",
                border_style="green"
            ))
            if response.artifacts:
                console.print(f"[green]Received {len(response.artifacts)} artifacts[/green]")


async def test_chat_history(stub, session_id: str):
    """Test chat history retrieval"""
    console.print("\n[bold cyan]Testing Chat History...[/bold cyan]")
    
    request = video_analysis_pb2.ChatHistoryRequest(
        session_id=session_id,
        limit=10
    )
    
    response = await stub.GetChatHistory(request)
    
    console.print(f"[green]Retrieved {len(response.messages)} messages[/green]")
    
    for i, msg in enumerate(response.messages, 1):
        style = "cyan" if msg.role == "user" else "green"
        console.print(f"\n[bold {style}]{i}. {msg.role.upper()}:[/bold {style}]")
        console.print(f"  {msg.content[:200]}...")
        if msg.artifacts:
            console.print(f"  [dim]Artifacts: {len(msg.artifacts)}[/dim]")


async def test_generate_report(stub, session_id: str, format: str = "pdf"):
    """Test report generation"""
    console.print(f"\n[bold cyan]Testing {format.upper()} Report Generation...[/bold cyan]")
    
    request = video_analysis_pb2.ReportRequest(
        session_id=session_id,
        format=format,
        content=video_analysis_pb2.ReportContent(
            title="Video Analysis Report",
            sections=["Summary", "Transcription", "Visual Analysis"],
            data={"generated_by": "Test Client"}
        )
    )
    
    response = await stub.GenerateReport(request)
    
    if response.status == "success":
        console.print(f"[green]✓ Report generated: {response.file_path}[/green]")
        console.print(f"  Size: {len(response.file_data) / 1024:.2f} KB")
    else:
        console.print(f"[red]✗ Report generation failed: {response.message}[/red]")


async def run_tests(video_path: str):
    """Run all gRPC tests"""
    # Set larger message sizes (50MB) for video uploads
    options = [
        ('grpc.max_send_message_length', 50 * 1024 * 1024),
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),
    ]
    
    # Connect to server
    async with grpc.aio.insecure_channel('localhost:50051', options=options) as channel:
        stub = video_analysis_pb2_grpc.VideoAnalysisServiceStub(channel)
        
        console.print("\n[bold green]===== gRPC Service Test Suite =====[/bold green]\n")
        
        # Generate session ID
        import uuid
        session_id = str(uuid.uuid4())
        console.print(f"[dim]Session ID: {session_id}[/dim]")
        
        # Test 1: Upload video
        video_id = await test_upload_video(stub, video_path)
        if not video_id:
            console.print("[red]Cannot continue without video ID[/red]")
            return
        
        # Test 2: Query video (single)
        await test_query_video(stub, video_id, session_id, "Transcribe the video")
        
        # Test 3: Query video (objects)
        await test_query_video(stub, video_id, session_id, "What objects can you see?")
        
        # Test 4: Stream query
        await test_stream_query(stub, video_id, session_id, "Describe what's happening in the video")
        
        # Test 5: Chat history
        await test_chat_history(stub, session_id)
        
        # Test 6: Generate PDF report
        await test_generate_report(stub, session_id, "pdf")
        
        console.print("\n[bold green]✓ All tests completed![/bold green]\n")


async def interactive_mode(video_path: str):
    """Interactive query mode"""
    # Set larger message sizes (50MB) for video uploads
    options = [
        ('grpc.max_send_message_length', 50 * 1024 * 1024),
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),
    ]
    
    async with grpc.aio.insecure_channel('localhost:50051', options=options) as channel:
        stub = video_analysis_pb2_grpc.VideoAnalysisServiceStub(channel)
        
        console.print("\n[bold green]===== Interactive Mode =====[/bold green]\n")
        
        # Upload video
        video_id = await test_upload_video(stub, video_path)
        if not video_id:
            return
        
        import uuid
        session_id = str(uuid.uuid4())
        console.print(f"\n[dim]Session ID: {session_id}[/dim]")
        console.print("[cyan]Enter queries (or 'quit' to exit):[/cyan]\n")
        
        while True:
            try:
                query = input("Query> ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not query:
                    continue
                
                # Send query
                request = video_analysis_pb2.QueryRequest(
                    session_id=session_id,
                    video_id=video_id,
                    query=query
                )
                
                response = await stub.QueryVideo(request)
                console.print(Panel(
                    response.response_text,
                    title="Response",
                    border_style="green"
                ))
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
        
        console.print("\n[green]Goodbye![/green]")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[red]Usage: python test_grpc_client.py <video_path> [--interactive][/red]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    interactive = "--interactive" in sys.argv or "-i" in sys.argv
    
    if interactive:
        asyncio.run(interactive_mode(video_path))
    else:
        asyncio.run(run_tests(video_path))
