"""
Test script for TranscriptionAgent
Usage: python test_transcription.py <video_file_path>
"""
import asyncio
import sys
import logging
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from agents.transcription_agent import TranscriptionAgent


async def test_transcription(video_path: str):
    """Test the transcription agent with a video file"""
    
    if not Path(video_path).exists():
        print(f"Error: Video file not found: {video_path}")
        return
    
    print(f"\nTesting Transcription Agent")
    print(f"Video: {video_path}")
    print("-" * 60)
    
    agent = TranscriptionAgent(model_size="medium")
    
    print("\nInitializing Whisper model (first run will download ~1.5GB)...")
    await agent.initialize()
    
    print("\nExtracting audio and transcribing...")
    result = await agent.process({"video_path": video_path})
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        return
    
    print("\n" + "=" * 60)
    print("TRANSCRIPTION COMPLETE")
    print("=" * 60)
    
    print(f"\nLanguage: {result['language']}")
    print(f"\nFull Transcription:\n{result['transcription']}")
    
    if result['segments']:
        print(f"\nTimestamped Segments ({len(result['segments'])} total):")
        print("-" * 60)
        for i, segment in enumerate(result['segments'][:5], 1):
            start = segment['start']
            end = segment['end']
            text = segment['text']
            print(f"[{start:.2f}s - {end:.2f}s] {text}")
        
        if len(result['segments']) > 5:
            print(f"... and {len(result['segments']) - 5} more segments")
    
    print("\n" + "=" * 60)
    
    output_file = "results/transcription_result.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Full result saved to: {output_file}")
    
    await agent.cleanup()


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_transcription.py <video_file_path>")
        print("\nExample:")
        print("  python test_transcription.py uploads/test_video.mp4")
        print("  python test_transcription.py ~/Downloads/my_video.mov")
        sys.exit(1)
    
    video_path = sys.argv[1]
    asyncio.run(test_transcription(video_path))


if __name__ == "__main__":
    main()
