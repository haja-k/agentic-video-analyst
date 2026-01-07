"""
Test script for Orchestrator Agent
Tests query routing and multi-agent coordination
"""
import sys
import os
import asyncio
import json
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.orchestrator_agent import OrchestratorAgent
from agents.transcription_agent import TranscriptionAgent
from agents.vision_agent import VisionAgent
from agents.generation_agent import GenerationAgent

from mcp_servers.transcription_mcp import TranscriptionMCPServer
from mcp_servers.vision_mcp import VisionMCPServer
from mcp_servers.generation_mcp import GenerationMCPServer

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


async def test_orchestrator(video_path: str = None):
    """Test the orchestrator with various queries"""
    
    console.print(Panel.fit(
        "[bold cyan]Orchestrator Agent Test[/bold cyan]\n" +
        "Testing query understanding and agent routing",
        border_style="cyan"
    ))
    
    # Initialize agents
    console.print("\n[yellow]Initializing agents...[/yellow]")
    
    model_path = "../models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    if not os.path.exists(model_path):
        model_path = "models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    
    if not os.path.exists(model_path):
        console.print("[red]Error: Llama model not found[/red]")
        console.print(f"Expected at: {model_path}")
        return
    
    transcription_agent = TranscriptionAgent(model_size="base")
    vision_agent = VisionAgent()
    generation_agent = GenerationAgent()
    
    # Wrap agents with MCP servers
    transcription_mcp = TranscriptionMCPServer(agent=transcription_agent)
    vision_mcp = VisionMCPServer(agent=vision_agent)
    generation_mcp = GenerationMCPServer(agent=generation_agent)
    
    orchestrator = OrchestratorAgent(
        model_path=model_path,
        transcription_mcp=transcription_mcp,
        vision_mcp=vision_mcp,
        generation_mcp=generation_mcp
    )
    
    try:
        await orchestrator.initialize()
        await transcription_agent.initialize()
        await vision_agent.initialize()
        await generation_agent.initialize()
        
        # Initialize MCP servers
        await transcription_mcp.initialize()
        await vision_mcp.initialize()
        await generation_mcp.initialize()
        
        console.print("[green]All agents and MCP servers initialized[/green]\n")
        
    except Exception as e:
        console.print(f"[red]Initialization failed: {e}[/red]")
        return
    
    # Test queries
    test_queries = [
        {
            "query": "Transcribe the video",
            "description": "Simple transcription request"
        },
        {
            "query": "What objects can you see in the video?",
            "description": "Object detection request"
        },
        {
            "query": "Describe what's happening in the video",
            "description": "Scene description request"
        },
        {
            "query": "Are there any graphs or charts shown?",
            "description": "Graph detection request"
        },
        {
            "query": "Create a PDF report with the key points discussed",
            "description": "Report generation (may need clarification)"
        },
        {
            "query": "Summarize our discussion so far",
            "description": "Summary request"
        }
    ]
    
    # Run tests
    context = {}
    
    for i, test in enumerate(test_queries, 1):
        console.print(f"\n[bold]Test {i}: {test['description']}[/bold]")
        console.print(f"Query: [cyan]{test['query']}[/cyan]")
        
        try:
            result = await orchestrator.process({
                "query": test["query"],
                "video_path": video_path,
                "context": context
            })
            
            console.print(f"\n[yellow]Actions taken:[/yellow]")
            if result.get("actions_taken"):
                for action in result.get("actions_taken", []):
                    console.print(f"  - {action}")
            else:
                console.print("  (none - using existing context)")
            
            console.print(f"\n[yellow]Response:[/yellow]")
            console.print(Panel(result["response"], border_style="green"))
            
            if result.get("requires_clarification"):
                console.print("[yellow]  (Requires user clarification)[/yellow]")
            
            # Update context with NEW results only
            if "results" in result:
                if "transcription" in result["results"]:
                    context["transcription"] = result["results"]["transcription"]
                if "vision" in result["results"]:
                    context["vision_results"] = result["results"]["vision"]
                if "summary" in result["results"]:
                    context["summary"] = result["results"]["summary"]
            
            console.print("\n" + "="*60)
            
        except Exception as e:
            error_msg = str(e).replace('[', '\\[').replace(']', '\\]')
            console.print(f"[red]Test failed: {error_msg}[/red]")
            import traceback
            traceback.print_exc()
    
    # Show final context
    console.print("\n[bold cyan]Final Context Summary:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    
    table.add_row("Transcription", "Available" if "transcription" in context else "Not available")
    table.add_row("Vision Analysis", "Available" if "vision_results" in context else "Not available")
    table.add_row("Summary", "Available" if "summary" in context else "Not available")
    
    console.print(table)
    
    console.print("\n[bold green]Orchestrator test complete![/bold green]")


async def test_intent_analysis():
    """Test intent analysis without full agent initialization"""
    
    console.print(Panel.fit(
        "[bold cyan]Intent Analysis Test[/bold cyan]\n" +
        "Testing query understanding without executing actions",
        border_style="cyan"
    ))
    
    model_path = "../models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    if not os.path.exists(model_path):
        model_path = "models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    
    if not os.path.exists(model_path):
        console.print("[red]Error: Llama model not found[/red]")
        return
    
    orchestrator = OrchestratorAgent(model_path=model_path)
    
    try:
        await orchestrator.initialize()
        console.print("[green]Orchestrator initialized[/green]\n")
        
    except Exception as e:
        console.print(f"[red]Initialization failed: {e}[/red]")
        return
    
    test_queries = [
        "Transcribe this video",
        "What objects are in the video?",
        "Generate a PDF report",
        "Are there any graphs?",
        "Summarize the video",
        "What was discussed in the meeting?",
        "Create a presentation about the key points"
    ]
    
    results_table = Table(show_header=True, header_style="bold magenta")
    results_table.add_column("Query", style="cyan", width=40)
    results_table.add_column("Primary Action", style="yellow")
    results_table.add_column("Needs Clarification", style="red")
    
    for query in test_queries:
        try:
            intent = await orchestrator.analyze_intent(query, {})
            
            results_table.add_row(
                query[:40],
                intent.get("primary_action", "unknown"),
                "Yes" if intent.get("needs_clarification") else "No"
            )
            
        except Exception as e:
            console.print(f"[red]Failed on query '{query}': {e}[/red]")
    
    console.print(results_table)
    console.print("\n[bold green]Intent analysis test complete![/bold green]")


def main():
    """Main test runner"""
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--intent-only":
            asyncio.run(test_intent_analysis())
        else:
            video_path = sys.argv[1]
            if not os.path.exists(video_path):
                console.print(f"[red]Error: Video file not found: {video_path}[/red]")
                sys.exit(1)
            
            asyncio.run(test_orchestrator(video_path))
    else:
        console.print("[yellow]Testing intent analysis only (no video provided)[/yellow]")
        console.print("[yellow]To test with video: python test_orchestrator.py <video_path>[/yellow]\n")
        asyncio.run(test_intent_analysis())


if __name__ == "__main__":
    main()
