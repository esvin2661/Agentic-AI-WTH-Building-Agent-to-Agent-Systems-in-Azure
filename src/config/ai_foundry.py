from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(
    endpoint="your_project_endpoint",  # Replace with your endpoint
    credential=DefaultAzureCredential())
