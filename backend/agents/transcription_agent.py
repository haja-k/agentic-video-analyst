"""
Transcription Agent - Handles speech-to-text extraction from videos
"""
from typing import Dict, Any, Optional
import logging
from pathlib import Path
import tempfile
import os

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class TranscriptionAgent(BaseAgent):
    """Agent responsible for transcribing audio from video files"""
    
    def __init__(self, model_size: str = "medium"):
        super().__init__("Transcription Agent", model_size)
        self.whisper_model = None
        self.model_size = model_size
        
    async def initialize(self):
        """Initialize Whisper model for transcription"""
        try:
            import whisper
            logger.info(f"Loading Whisper {self.model_size} model...")
            self.whisper_model = whisper.load_model(self.model_size)
            logger.info("✓ Transcription model loaded")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transcribe audio from video file
        
        Args:
            input_data: {
                "video_path": str,
                "language": Optional[str] = None (auto-detect if not specified)
            }
            
        Returns:
            {
                "transcription": str (full text),
                "segments": List[Dict] (timestamped segments),
                "language": str (detected language)
            }
        """
        video_path = input_data.get("video_path")
        if not video_path or not Path(video_path).exists():
            return {"error": f"Video file not found: {video_path}"}
        
        logger.info(f"Transcribing video: {video_path}")
        
        try:
            audio_path = await self.extract_audio(video_path)
            
            language = input_data.get("language", None)
            transcribe_options = {}
            if language:
                transcribe_options["language"] = language
            
            result = self.whisper_model.transcribe(audio_path, **transcribe_options)
            
            os.unlink(audio_path)
            
            segments = []
            for segment in result.get("segments", []):
                segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                })
            
            return {
                "transcription": result["text"].strip(),
                "segments": segments,
                "language": result.get("language", "unknown")
            }
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return {"error": str(e)}
    
    async def extract_audio(self, video_path: str) -> str:
        """Extract audio from video file to temporary WAV file"""
        try:
            from moviepy.editor import VideoFileClip
            
            temp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_audio_path = temp_audio.name
            temp_audio.close()
            
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(temp_audio_path, logger=None)
            video.close()
            
            return temp_audio_path
            
        except Exception as e:
            logger.error(f"Audio extraction failed: {e}")
            raise
