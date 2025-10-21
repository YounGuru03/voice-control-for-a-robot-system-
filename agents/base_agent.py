"""
Base Agent Class
Defines the interface for all agent modules
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import logging


class BaseAgent(ABC):
    """Abstract base class for all agents in the system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the agent with configuration
        
        Args:
            config: Configuration dictionary for the agent
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the agent and its resources
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """
        Process input data and return result
        
        Args:
            data: Input data to process
            
        Returns:
            Processed result
        """
        pass
    
    @abstractmethod
    def shutdown(self):
        """Clean up resources and shutdown the agent"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the agent
        
        Returns:
            Dictionary containing agent status information
        """
        return {
            'name': self.__class__.__name__,
            'initialized': self.initialized,
            'config': self.config
        }
