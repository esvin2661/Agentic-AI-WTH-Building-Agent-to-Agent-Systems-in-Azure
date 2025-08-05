"""
Test connection to Azure AI Foundry
"""

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

def test_connection():
    try:
        project = AIProjectClient(
            endpoint="https://esvin-test-project.services.ai.azure.com/",  # Replace with your endpoint
            credential=DefaultAzureCredential()
        )
        
        # Try to access project information
        # This will verify our connection
        print("Successfully connected to Azure AI Foundry!")
        print("Project information:", project)
        return True
        
    except Exception as e:
        print(f"Failed to connect to Azure AI Foundry: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
