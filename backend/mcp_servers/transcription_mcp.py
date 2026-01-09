"""
Transcription MCP Server
Exposes transcription capabilities via MCP protocol
"""
from typing import Dict, Any
import logging

from .base_mcp_server import BaseMCPServer
from agents.transcription_agent import TranscriptionAgent

logger = logging.getLogger(__name__)


class TranscriptionMCPServer(BaseMCPServer):
    """MCP Server for transcription operations"""
    
    def __init__(self, agent=None):
        super().__init__("transcription-server", "1.0.0")
        self.agent = agent
        
    async def initialize(self):
        """Register tools and prompts (agent should be set externally)"""
        
        # Register tools
        self.register_tool({
            "name": "transcribe_video",
            "description": "Transcribe audio from a video file to text",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to the video file"
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code (e.g., 'en', 'es')",
                        "default": "en"
                    }
                },
                "required": ["video_path"]
            }
        })
        
        # Register prompts
        self.register_prompt({
            "name": "transcription_summary",
            "description": "Summarize a transcription",
            "arguments": [
                {
                    "name": "transcription",
                    "description": "The full transcription text",
                    "required": True
                }
            ]
        })
        
        logger.info("✓ Transcription MCP Server initialized")
        
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool invocations"""
        if tool_name == "transcribe_video":
            return await self.agent.process(arguments)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
