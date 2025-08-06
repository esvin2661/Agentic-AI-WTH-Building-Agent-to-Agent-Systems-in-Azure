from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from typing import Dict, Any

class BaseAgent:
    def __init__(self, name: str, project: AIProjectClient):
        """
        Initialize a base agent.
        
        Args:
            name (str): Name of the agent
            project (AIProjectClient): Azure AI Foundry project client
        """
        self.name = name
        self.project = project
        self.status = "initialized"
        self.state: Dict[str, Any] = {}

    async def initialize(self) -> None:
        """Initialize agent resources and configurations"""
        self.status = "ready"
    
    async def start(self) -> None:
        """Start the agent's main processing loop"""
        self.status = "running"
    
    async def stop(self) -> None:
        """Stop the agent's processing"""
        self.status = "stopped"
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming messages.
        
        Args:
            message (Dict[str, Any]): The message to process
            
        Returns:
            Dict[str, Any]: The response or result
        """
        raise NotImplementedError("Each agent must implement process_message")
    
    def get_status(self) -> str:
        """Get the current status of the agent"""
        return self.status
