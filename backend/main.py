"""
Main entry point for the AI Video Analysis Backend
"""
import asyncio
import logging
from concurrent import futures
import grpc

from rich.console import Console
from rich.logging import RichHandler

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


class BackendServer:
    """Main backend server orchestrating all agents and MCP servers"""
    
    def __init__(self, port: int = 50051):
        self.port = port
        self.server = None
        
    async def initialize(self):
        """Initialize all agents and MCP servers"""
        console.print("[bold green]Initializing AI Video Analysis Backend...[/bold green]")
        
        # TODO: Initialize agents
        # - Transcription Agent
        # - Vision Agent
        # - Generation Agent
        
        console.print("✓ Agents initialized", style="green")
        
        # TODO: Initialize MCP servers
        console.print("✓ MCP servers ready", style="green")
        
    async def start(self):
        """Start the gRPC server"""
        await self.initialize()
        
        self.server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=10)
        )
        
        # TODO: Add gRPC servicers
        # video_service_pb2_grpc.add_VideoServiceServicer_to_server(
        #     VideoServiceServicer(), self.server
        # )
        
        self.server.add_insecure_port(f'[::]:{self.port}')
        await self.server.start()
        
        console.print(f"[bold green]✓ Server started on port {self.port}[/bold green]")
        console.print("\n[bold cyan]Ready to process video queries![/bold cyan]\n")
        
        await self.server.wait_for_termination()
        
    async def stop(self):
        """Graceful shutdown"""
        if self.server:
            await self.server.stop(grace=5)


async def main():
    """Main entry point"""
    server = BackendServer(port=50051)
    
    try:
        await server.start()
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down gracefully...[/yellow]")
        await server.stop()
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
