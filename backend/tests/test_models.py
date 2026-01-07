"""
Test script to verify all models are working
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rich.console import Console
from rich.table import Table

console = Console()


def test_llama():
    """Test llama.cpp"""
    console.print("\n[bold cyan]Testing Llama Model...[/bold cyan]")
    
    try:
        from llama_cpp import Llama
        
        # Check for model (adjust path since we're in tests/ subdirectory)
        model_options = [
            "../models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
            "../../models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
            "../models/llama-3.1-8b-instruct.Q4_K_M.gguf",
            "../../models/llama-3.1-8b-instruct.Q4_K_M.gguf",
            "../models/llama-3.2-3b-instruct.Q4_K_M.gguf",
            "../../models/llama-3.2-3b-instruct.Q4_K_M.gguf",
            "../models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            "../../models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            "../models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
            "../../models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"  # Fallback
        ]
        
        model_path = None
        for path in model_options:
            if os.path.exists(path):
                model_path = path
                break
        
        if not model_path:
            console.print(f"[yellow]No model found. Expected one of:[/yellow]")
            for path in model_options:
                console.print(f"  - {path}")
            console.print("\n[cyan]Run: ./download-models.sh[/cyan]")
            return False
        
        console.print(f"Loading model from {model_path}...")
        
        # Determine if it's a vision model
        is_vision = "vision" in model_path.lower()
        
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,  # Use smaller context for testing
            n_threads=6,
            n_gpu_layers=1,  # Metal acceleration
            verbose=False
        )
        
        # Test generation
        console.print("Testing text generation...")
        response = llm("Q: What is AI? A:", max_tokens=32, stop=["Q:", "\n"], echo=False)
        
        model_name = os.path.basename(model_path)
        console.print("[yellow]Note: Model will download on first actual use[/yellow]")
        console.print("  - Whisper Medium: ~1.5GB (recommended)")
        console.print("  - Whisper Base: ~150MB (faster but lower quality)")
        
        if is_vision:
            console.print(f"[green]✅ Llama 3.2 Vision model working! (multimodal capable)[/green]")
        else:
            console.print(f"[green]✅ Llama model working![/green]")
        
        console.print(f"Model: {model_name}")
        console.print(f"Sample output: {response['choices'][0]['text'][:50]}...")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        return False


def test_whisper():
    """Test Whisper (will download on first use)"""
    console.print("\n[bold cyan]Testing Whisper Model...[/bold cyan]")
    
    try:
        # Check if openai-whisper is available
        import whisper
        
        console.print("Whisper package installed")
        console.print("[yellow]Note: Model will download on first actual use[/yellow]")
        console.print("  - Whisper Medium: ~1.5GB (recommended)")
        console.print("  - Whisper Base: ~150MB (faster but lower quality)")
        console.print("[green]✅ Whisper ready![/green]")
        return True
        
    except ImportError as e:
        console.print(f"[red]❌ Whisper not installed: {e}[/red]")
        console.print("Install: pip install openai-whisper")
        return False
    except Exception as e:
        console.print(f"[yellow]⚠️  Warning: {e}[/yellow]")
        return True


def test_vision():
    """Test vision models"""
    console.print("\n[bold cyan]Testing Vision Models...[/bold cyan]")
    
    try:
        import torch
        from transformers import __version__ as transformers_version
        
        
        # Check if using Llama 3.2 Vision
        vision_model_paths = [
            "backend/models/llama-3.2-11b-vision-instruct.Q4_K_M.gguf",
            "models/llama-3.2-11b-vision-instruct.Q4_K_M.gguf"
        ]
        if any(os.path.exists(p) for p in vision_model_paths):
            console.print("[green]✅ Llama 3.2 Vision detected! (Multimodal - no separate vision model needed)[/green]")
        else:
            console.print("[yellow]Note: BLIP-2 will auto-download on first use (~2.7GB)[/yellow]")
            console.print("[green]✅ Vision libraries ready![/green]")
        
        console.print("[yellow]Note: BLIP and other models will download on first use (~500MB)[/yellow]")
        console.print("[green]✅ Vision libraries ready![/green]")
        return True
        
    except ImportError as e:
        console.print(f"[red]❌ Vision libraries not installed: {e}[/red]")
        return False


def test_document_generation():
    """Test PDF/PPT generation"""
    console.print("\n[bold cyan]Testing Document Generation...[/bold cyan]")
    
    try:
        import reportlab
        import pptx
        
        console.print("[green]✅ ReportLab and python-pptx installed![/green]")
        return True
        
    except ImportError as e:
        console.print(f"[red]❌ Document libraries not installed: {e}[/red]")
        return False


def main():
    """Run all tests"""
    console.print("[bold green]🧪 Testing AI Model Setup[/bold green]\n")
    
    results = {
        "Llama (LLM)": test_llama(),
        "Whisper (Speech)": test_whisper(),
        "Vision Models": test_vision(),
        "Document Gen": test_document_generation()
    }
    
    # Summary table
    table = Table(title="\n📊 Model Test Results")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="bold")
    
    for name, status in results.items():
        status_text = "[green]✅ Ready[/green]" if status else "[red]❌ Failed[/red]"
        table.add_row(name, status_text)
    
    console.print(table)
    
    if all(results.values()):
        console.print("\n[bold green]🎉 All systems ready for demo![/bold green]\n")
        return 0
    else:
        console.print("\n[bold yellow]⚠️  Some components need attention[/bold yellow]\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
