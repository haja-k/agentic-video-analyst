"""
Generation MCP Server
Exposes document generation capabilities via MCP protocol
"""
from typing import Dict, Any
import logging

from .base_mcp_server import BaseMCPServer
from agents.generation_agent import GenerationAgent

logger = logging.getLogger(__name__)


class GenerationMCPServer(BaseMCPServer):
    """MCP Server for document generation operations"""
    
    def __init__(self, agent=None):
        super().__init__("generation-server", "1.0.0")
        self.agent = agent
        
    async def initialize(self):
        """Register tools (agent should be set externally)"""
        
        # Register tools
        self.register_tool({
            "name": "generate_pdf",
            "description": "Generate a PDF report from content",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "object",
                        "description": "Structured content for the PDF"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path where PDF should be saved"
                    }
                },
                "required": ["content", "output_path"]
            }
        })
        
        self.register_tool({
            "name": "generate_pptx",
            "description": "Generate a PowerPoint presentation from content",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "object",
                        "description": "Structured content for the presentation"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path where PPTX should be saved"
                    }
                },
                "required": ["content", "output_path"]
            }
        })
        
        logger.info("✓ Generation MCP Server initialized")
        
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool invocations"""
        if tool_name == "generate_pdf":
            arguments["format"] = "pdf"
            return await self.agent.process(arguments)
        elif tool_name == "generate_pptx":
            arguments["format"] = "pptx"
            return await self.agent.process(arguments)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
