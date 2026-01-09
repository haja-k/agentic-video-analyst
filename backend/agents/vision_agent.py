"""
Vision Agent - Handles object detection, image captioning, and scene analysis
"""
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path
import tempfile
import os
import cv2
import numpy as np
from PIL import Image

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class VisionAgent(BaseAgent):
    """Agent responsible for visual analysis of video frames"""
    
    def __init__(self, blip_model_name: str = "Salesforce/blip-image-captioning-base"):
        super().__init__("Vision Agent", blip_model_name)
        self.caption_processor = None
        self.caption_model = None
        self.detector_model = None
        self.device = None
        
    async def initialize(self):
        """Initialize vision models for captioning and object detection"""
        try:
            import torch
            from transformers import BlipProcessor, BlipForConditionalGeneration
            from ultralytics import YOLO
            
            self.device = "mps" if torch.backends.mps.is_available() else "cpu"
            logger.info(f"Using device: {self.device}")
            
            logger.info(f"Loading BLIP captioning model: {self.model_path}")
            self.caption_processor = BlipProcessor.from_pretrained(self.model_path)
            self.caption_model = BlipForConditionalGeneration.from_pretrained(self.model_path)
            self.caption_model.to(self.device)
            
            logger.info("Loading YOLOv8 nano model for object detection")
            self.detector_model = YOLO("models/yolov8n.pt")
            
            logger.info("✓ Vision models loaded")
            
        except Exception as e:
            logger.error(f"Failed to load vision models: {e}")
            raise
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze video frames with object detection and scene description
        
        Args:
            input_data: {
                "video_path": str,
                "task": str (optional) - "detect_objects", "describe_scene", "analyze" (default)
                "num_frames": int (optional) - number of frames to sample (default: 10)
                "interval": int (optional) - sample every N seconds (overrides num_frames)
            }
            
        Returns:
            {
                "frames_analyzed": int,
                "results": List[Dict] with frame_number, timestamp, objects, caption
            }
        """
        video_path = input_data.get("video_path")
        if not video_path or not Path(video_path).exists():
            return {"error": f"Video file not found: {video_path}"}
        
        task = input_data.get("task", "analyze")
        num_frames = input_data.get("num_frames", 10)
        interval = input_data.get("interval", None)
        
        logger.info(f"Vision analysis on: {video_path} (task: {task})")
        
        try:
            frames_data = await self.extract_frames(video_path, num_frames, interval)
            results = []
            
            for frame_info in frames_data:
                frame_path = frame_info["path"]
                frame_num = frame_info["frame_number"]
                timestamp = frame_info["timestamp"]
                
                result = {
                    "frame_number": frame_num,
                    "timestamp": timestamp
                }
                
                if task in ["detect_objects", "analyze"]:
                    objects = await self.detect_objects(frame_path)
                    result["objects"] = objects
                
                if task in ["describe_scene", "analyze"]:
                    caption = await self.caption_image(frame_path)
                    result["caption"] = caption
                
                results.append(result)
                os.unlink(frame_path)
            
            return {
                "frames_analyzed": len(results),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Vision analysis failed: {e}")
            return {"error": str(e)}
    
    async def extract_frames(self, video_path: str, num_frames: int = 10, 
                           interval: Optional[int] = None) -> List[Dict]:
        """Extract frames from video at regular intervals"""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        if interval:
            frame_indices = [int(i * fps * interval) for i in range(int(duration / interval))]
        else:
            frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        
        frames_data = []
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            
            if ret:
                temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                cv2.imwrite(temp_file.name, frame)
                
                timestamp = idx / fps if fps > 0 else 0
                frames_data.append({
                    "path": temp_file.name,
                    "frame_number": int(idx),
                    "timestamp": round(timestamp, 2)
                })
        
        cap.release()
        return frames_data
    
    async def detect_objects(self, frame_path: str) -> List[Dict]:
        """Detect objects in a frame using YOLOv8"""
        results = self.detector_model(frame_path, verbose=False)
        
        objects = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                objects.append({
                    "class": result.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist()
                })
        
        return objects
    
    async def caption_image(self, frame_path: str) -> str:
        """Generate descriptive caption for an image using BLIP-2"""
        import torch
        
        image = Image.open(frame_path).convert("RGB")
        inputs = self.caption_processor(image, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            output = self.caption_model.generate(**inputs, max_length=50)
        
        caption = self.caption_processor.decode(output[0], skip_special_tokens=True)
        return caption
