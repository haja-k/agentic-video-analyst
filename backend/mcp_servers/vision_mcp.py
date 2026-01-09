"""
Vision MCP Server
Exposes vision analysis capabilities via MCP protocol
"""
from typing import Dict, Any
import logging

from .base_mcp_server import BaseMCPServer
from agents.vision_agent import VisionAgent

logger = logging.getLogger(__name__)


class VisionMCPServer(BaseMCPServer):
    """MCP Server for vision analysis operations"""
    
    def __init__(self, agent=None):
        super().__init__("vision-server", "1.0.0")
        self.agent = agent
        
    async def initialize(self):
        """Register tools (agent should be set externally)"""
        
        # Register tools
        self.register_tool({
            "name": "detect_objects",
            "description": "Detect and identify objects in video frames",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to the video file"
                    }
                },
                "required": ["video_path"]
            }
        })
        
        self.register_tool({
            "name": "caption_video",
            "description": "Generate captions for video frames",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to the video file"
                    }
                },
                "required": ["video_path"]
            }
        })
        
        self.register_tool({
            "name": "detect_graphs",
            "description": "Detect and analyze graphs/charts in video",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to the video file"
                    }
                },
                "required": ["video_path"]
            }
        })
        
        self.register_tool({
            "name": "extract_text",
            "description": "Extract text from video frames using OCR",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to the video file"
                    }
                },
                "required": ["video_path"]
            }
        })
        
        logger.info("✓ Vision MCP Server initialized")
        
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool invocations"""
        task_map = {
            "detect_objects": "analyze",  # Get both objects and captions
            "caption_video": "analyze",   # Get both objects and captions
            "detect_graphs": "detect_graphs",
            "extract_text": "ocr"
        }
        
        if tool_name in task_map:
            arguments["task"] = task_map[tool_name]
            return await self.agent.process(arguments)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
