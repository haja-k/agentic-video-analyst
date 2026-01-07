"""
Base MCP Server implementation
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class BaseMCPServer(ABC):
    """Base class for MCP servers following Model Context Protocol"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: List[Dict[str, Any]] = []
        self.prompts: List[Dict[str, Any]] = []
        logger.info(f"Initializing MCP Server: {name} v{version}")
        
    @abstractmethod
    async def initialize(self):
        """Initialize the MCP server and register tools/prompts"""
        pass
    
    @abstractmethod
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a tool invocation"""
        pass
    
    def register_tool(self, tool: Dict[str, Any]):
        """Register a tool with this MCP server"""
        self.tools.append(tool)
        logger.info(f"Registered tool: {tool.get('name')}")
        
    def register_prompt(self, prompt: Dict[str, Any]):
        """Register a prompt template"""
        self.prompts.append(prompt)
        logger.info(f"Registered prompt: {prompt.get('name')}")
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return server capabilities"""
        return {
            "name": self.name,
            "version": self.version,
            "tools": self.tools,
            "prompts": self.prompts
        }
