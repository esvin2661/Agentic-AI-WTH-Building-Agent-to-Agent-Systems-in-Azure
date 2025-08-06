"""
Test script for the Monitor Agent
"""
import asyncio
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from agents.monitor_agent import MonitorAgent
from datetime import datetime

async def main():
    # Initialize the AI Foundry client
    project = AIProjectClient(
        endpoint="https://esvin-test-project.services.ai.azure.com/",
        credential=DefaultAzureCredential()
    )
    
    # Create and initialize the Monitor Agent
    monitor = MonitorAgent(project)
    await monitor.initialize()
    
    # Test with sample metrics data
    test_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": {
            "cpu_usage": 85.5,     # Should trigger alert (> 80%)
            "memory_usage": 75.0,   # Normal
            "network_io": 95.0,     # Should trigger alert (> 90%)
            "disk_io": 60.0        # Normal
        }
    }
    
    # Process the test data
    print("\nProcessing test metrics...")
    result = await monitor.process_message(test_data)
    
    # Display results
    print("\nProcessing Results:")
    print(f"Timestamp: {result['timestamp']}")
    print("\nProcessed Metrics:")
    for metric, value in result['processed_metrics'].items():
        print(f"{metric}: {value}%")
    
    print("\nAlerts Generated:")
    if result['alerts']:
        for alert in result['alerts']:
            print(f"- {alert['metric']}: {alert['value']}% (Threshold: {alert['threshold']}%) - Severity: {alert['severity']}")
    else:
        print("No alerts generated")

if __name__ == "__main__":
    asyncio.run(main())
