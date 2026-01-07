"""
Main entry point for the AI Video Analysis Backend
"""
import asyncio
import logging
from concurrent import futures
from pathlib import Path
import grpc

from rich.console import Console
from rich.logging import RichHandler

from agents.orchestrator_agent import OrchestratorAgent
from agents.transcription_agent import TranscriptionAgent
from agents.vision_agent import VisionAgent
from agents.generation_agent import GenerationAgent

from mcp_servers.transcription_mcp import TranscriptionMCPServer
from mcp_servers.vision_mcp import VisionMCPServer
from mcp_servers.generation_mcp import GenerationMCPServer

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
        
        self.server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=10)
        )
        
        # TODO: Add gRPC servicers when proto definitions are ready
        # For now, the server is ready to accept connections
        
        self.server.add_insecure_port(f'[::]:{self.port}')
        await self.server.start()
        
        console.print(f"\n[bold green]✓ Server started on port {self.port}[/bold green]")
        console.print("\n[bold cyan]Ready to process video queries![/bold cyan]")
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
