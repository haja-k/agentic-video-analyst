"""
Test script for VisionAgent
Usage: python test_vision.py <video_file_path>
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

from agents.vision_agent import VisionAgent


async def test_vision(video_path: str):
    """Test the vision agent with a video file"""
    
    if not Path(video_path).exists():
        print(f"Error: Video file not found: {video_path}")
        return
    
    print(f"\nTesting Vision Agent")
    print(f"Video: {video_path}")
    print("-" * 60)
    
    agent = VisionAgent()
    
    print("\nInitializing vision models (BLIP-2 + YOLOv8)...")
    print("   First run will download models (~2.7GB for BLIP, ~6MB for YOLO)")
    await agent.initialize()
    
    print("\nExtracting frames and analyzing...")
    result = await agent.process({
        "video_path": video_path,
        "task": "analyze",
        "num_frames": 8
    })
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        return
    
    print("\n" + "=" * 60)
    print("VISION ANALYSIS COMPLETE")
    print("=" * 60)
    
    print(f"\nFrames analyzed: {result['frames_analyzed']}")
    
    for i, frame_result in enumerate(result['results'], 1):
        print(f"\n{'='*60}")
        print(f"Frame {i}/{len(result['results'])}")
        print(f"{'='*60}")
        print(f"Timestamp: {frame_result['timestamp']:.2f}s")
        print(f"Frame number: {frame_result['frame_number']}")
        
        if 'caption' in frame_result:
            print(f"\nScene Description:")
            print(f"   {frame_result['caption']}")
        
        if 'objects' in frame_result:
            objects = frame_result['objects']
            print(f"\nObjects Detected ({len(objects)}):")
            
            if objects:
                object_summary = {}
                for obj in objects:
                    class_name = obj['class']
                    confidence = obj['confidence']
                    if class_name not in object_summary:
                        object_summary[class_name] = []
                    object_summary[class_name].append(confidence)
                
                for class_name, confidences in sorted(object_summary.items()):
                    avg_conf = sum(confidences) / len(confidences)
                    count = len(confidences)
                    print(f"   • {class_name}: {count}x (avg confidence: {avg_conf:.2f})")
            else:
                print("   No objects detected in this frame")
    
    print("\n" + "=" * 60)
    
    output_file = "results/vision_result.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Full result saved to: {output_file}")
    
    await agent.cleanup()


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_vision.py <video_file_path>")
        print("\nExample:")
        print("  python test_vision.py uploads/test_video.mp4")
        print("  python test_vision.py ~/Downloads/my_video.mov")
        sys.exit(1)
    
    video_path = sys.argv[1]
    asyncio.run(test_vision(video_path))


if __name__ == "__main__":
    main()
