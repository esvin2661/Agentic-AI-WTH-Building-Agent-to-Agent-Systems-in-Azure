from typing import Dict, Any, List
from .base_agent import BaseAgent
from azure.ai.projects import AIProjectClient

class MonitorAgent(BaseAgent):
    def __init__(self, project: AIProjectClient):
        """
        Initialize the Monitor Agent.
        
        Args:
            project (AIProjectClient): Azure AI Foundry project client
        """
        super().__init__("MonitorAgent", project)
        self.metrics_to_monitor = [
            "cpu_usage",
            "memory_usage",
            "network_io",
            "disk_io"
        ]
        self.thresholds = {
            "cpu_usage": 80.0,    # 80% threshold
            "memory_usage": 85.0,  # 85% threshold
            "network_io": 90.0,    # 90% threshold
            "disk_io": 85.0       # 85% threshold
        }

    async def initialize(self) -> None:
        """Initialize monitoring configuration"""
        await super().initialize()
        self.state.update({
            "metrics": self.metrics_to_monitor,
            "thresholds": self.thresholds,
            "alerts": []
        })
        print(f"{self.name} initialized with metrics: {self.metrics_to_monitor}")

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process monitoring data and generate alerts if needed.
        
        Args:
            message (Dict[str, Any]): Message containing metrics data
            
        Returns:
            Dict[str, Any]: Processing results and any alerts
        """
        alerts = []
        metrics = message.get("metrics", {})
        
        for metric, value in metrics.items():
            if metric in self.thresholds:
                if value > self.thresholds[metric]:
                    alerts.append({
                        "metric": metric,
                        "value": value,
                        "threshold": self.thresholds[metric],
                        "severity": "high" if value > self.thresholds[metric] + 10 else "medium"
                    })
        
        result = {
            "timestamp": message.get("timestamp"),
            "processed_metrics": metrics,
            "alerts": alerts
        }
        
        # Update state with latest data
        self.state["last_processed"] = result
        
        return result

    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get list of active alerts"""
        return self.state.get("last_processed", {}).get("alerts", [])
