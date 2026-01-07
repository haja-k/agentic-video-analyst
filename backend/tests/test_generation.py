"""
Test script for GenerationAgent
Usage: python test_generation.py
"""
import asyncio
import logging
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from agents.generation_agent import GenerationAgent


async def test_generation():
    """Test the generation agent with sample data"""
    
    print(f"\n📄 Testing Generation Agent")
    print("-" * 60)
    
    agent = GenerationAgent()
    
    print("\n🔄 Initializing generation tools...")
    await agent.initialize()
    
    sample_transcription = None
    sample_vision = None
    
    if Path("results/transcription_result.json").exists():
        with open("results/transcription_result.json") as f:
            sample_transcription = json.load(f)
        print("✓ Loaded transcription results")
    
    if Path("results/vision_result.json").exists():
        with open("results/vision_result.json") as f:
            sample_vision = json.load(f)
        print("✓ Loaded vision results")
    
    print("\n" + "=" * 60)
    print("📊 GENERATING PDF REPORT")
    print("=" * 60)
    
    pdf_input = {
        "format": "pdf",
        "title": "Video Analysis Report",
        "summary": "This report contains a comprehensive analysis of the uploaded video, including full transcription and visual content analysis.",
        "transcription": sample_transcription,
        "vision_results": sample_vision,
        "output_path": "results/video_report.pdf"
    }
    
    pdf_result = await agent.process(pdf_input)
    
    if pdf_result.get("status") == "success":
        print(f"\n✅ PDF generated successfully!")
        print(f"📁 Location: {pdf_result['output_path']}")
        print(f"📏 Size: {pdf_result['file_size']:,} bytes ({pdf_result['file_size']/1024:.1f} KB)")
    else:
        print(f"\n❌ PDF generation failed: {pdf_result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 60)
    print("📊 GENERATING POWERPOINT PRESENTATION")
    print("=" * 60)
    
    pptx_input = {
        "format": "pptx",
        "title": "Video Analysis Presentation",
        "summary": "Key findings from video analysis including transcription highlights and visual elements detected.",
        "transcription": sample_transcription,
        "vision_results": sample_vision,
        "output_path": "results/video_presentation.pptx"
    }
    
    pptx_result = await agent.process(pptx_input)
    
    if pptx_result.get("status") == "success":
        print(f"\n✅ PowerPoint generated successfully!")
        print(f"📁 Location: {pptx_result['output_path']}")
        print(f"📏 Size: {pptx_result['file_size']:,} bytes ({pptx_result['file_size']/1024:.1f} KB)")
    else:
        print(f"\n❌ PowerPoint generation failed: {pptx_result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 60)
    print("✅ GENERATION TESTS COMPLETE")
    print("=" * 60)
    
    if pdf_result.get("status") == "success":
        print(f"\n💡 Open PDF: open {pdf_result['output_path']}")
    if pptx_result.get("status") == "success":
        print(f"💡 Open PowerPoint: open {pptx_result['output_path']}")
    
    if not sample_transcription and not sample_vision:
        print("\n⚠️  Note: No previous results found. Documents contain placeholder data.")
        print("   Run 'python test_transcription.py <video>' and 'python test_vision.py <video>' first.")
    
    await agent.cleanup()


def main():
    print("\n" + "="*60)
    print("Generation Agent Test")
    print("="*60)
    print("This will generate sample PDF and PowerPoint documents")
    print("using any available transcription/vision results.")
    
    asyncio.run(test_generation())


if __name__ == "__main__":
    main()
