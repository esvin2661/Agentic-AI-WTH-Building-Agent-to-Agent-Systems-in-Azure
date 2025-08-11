from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Replace with your actual Foundry endpoint
project_endpoint = "https://esvin-test-project.services.ai.azure.com/"

# Create the AIProjectClient using the endpoint and default Azure credentials
project = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)
