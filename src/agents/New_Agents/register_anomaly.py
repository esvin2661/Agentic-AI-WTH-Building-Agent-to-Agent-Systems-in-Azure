
"""Register the anomaly detector agent with a Foundry AgentsClient.

This module is resilient when `azure.ai.foundry` is not installed: a small
fallback AgentClient is used that simply prints the registration action.
"""

import os
import inspect
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from current or parent directories
script_path = Path(__file__).resolve()
found_dotenv = None
for parent in [script_path] + list(script_path.parents):
    candidate = parent / ".env"
    if candidate.exists():
        load_dotenv(dotenv_path=candidate)
        found_dotenv = candidate
        break

if found_dotenv:
    print(f"Loaded .env from: {found_dotenv}")
else:
    print("No .env found in parent folders; relying on process environment variables.")

# Normalize environment variable names
endpoint_aliases = [
    "AZURE_AI_FOUNDRY_ENDPOINT",
    "AZUREAIFOUNDRYENDPOINT",
    "AZURE_AI_FOUNDRY",
    "AZURE_AI_FOUNDRY_URL",
]
apikey_aliases = [
    "AZURE_AI_FOUNDRY_API_KEY",
    "AZUREAIFOUNDRYAPI_KEY",
    "AZUREAIFOUNDRYAPIKEY",
    "AZURE_AI_FOUNDRY_KEY",
    "AZURE_AGENT_API_KEY",
    "AZURE_API_KEY",
]

found_endpoint_name = None
for name in endpoint_aliases:
    if os.getenv(name):
        os.environ["AZURE_AI_FOUNDRY_ENDPOINT"] = os.getenv(name)
        found_endpoint_name = name
        break

found_apikey_name = None
for name in apikey_aliases:
    if os.getenv(name):
        os.environ["AZURE_AI_FOUNDRY_API_KEY"] = os.getenv(name)
        found_apikey_name = name
        break

print("Endpoint source:", found_endpoint_name or "missing")
print("API key source:", found_apikey_name or "missing")

# Try to use the real AgentsClient if available
try:
    from azure.ai.agents import AgentsClient as _RealAgentsClient
    REAL_AGENTS_CLIENT = True
except Exception:
    _RealAgentsClient = None
    REAL_AGENTS_CLIENT = False

class AgentClient:
    def __init__(self, *args, **kwargs):
        self._client = None
        self._ready = False

        if REAL_AGENTS_CLIENT:
            endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
            api_key = os.getenv("AZURE_AI_FOUNDRY_API_KEY")
            credential = None
            # Prefer a TokenCredential (DefaultAzureCredential). If not available,
            # do not attempt to use AzureKeyCredential because the AgentsClient
            # implementation may expect a TokenCredential with get_token().
            try:
                from azure.identity import DefaultAzureCredential
                credential = DefaultAzureCredential()
            except Exception:
                # DefaultAzureCredential not available; do not use AzureKeyCredential
                api_key = os.getenv("AZURE_AGENT_API_KEY") or os.getenv("AZURE_API_KEY") or os.getenv("AZURE_AI_FOUNDRY_API_KEY")
                if api_key:
                    print("API key present but DefaultAzureCredential unavailable; AgentsClient likely requires TokenCredential. Falling back to lightweight client.")
                credential = None

            # Try to instantiate real client only if endpoint and a TokenCredential are available
            if endpoint and credential is not None:
                try:
                    self._client = _RealAgentsClient(endpoint=endpoint, credential=credential)
                    self._ready = True
                    print("Real AgentsClient instantiated")
                    return
                except Exception as inst_e:
                    print("Failed to instantiate real AgentsClient:", inst_e)

        if not self._ready:
            print("AgentClient fallback: using lightweight stub")

    def register_agent(self, agent):
        if self._client is not None and self._ready:
            try:
                return self._client.create_agent(
                    model=agent.model,
                    name=agent.name,
                    instructions=agent.instructions,
                    tools=agent.tools
                )
            except Exception as e:
                print("Error during agent registration:", e)
                return False
        else:
            print(f"Fallback register_agent called for {agent.__class__.__name__}")
            return True

# Import your anomaly detector agent
from anomaly_detector import AnomalyDetectorAgent

def main():
    client = AgentClient()
    agent = AnomalyDetectorAgent()
    client.register_agent(agent)

if __name__ == "__main__":
    main()
