"""
Base Agent class for all AI agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all AI agents in the system"""
    
    def __init__(self, name: str, model_path: Optional[str] = None):
        self.name = name
        self.model_path = model_path
        self.model = None
        logger.info(f"Initializing {name}")
        
    @abstractmethod
    async def initialize(self):
        """Initialize the agent and load models"""
        pass
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return results"""
        pass
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info(f"Cleaning up {self.name}")
        if self.model:
            del self.model
            self.model = None
