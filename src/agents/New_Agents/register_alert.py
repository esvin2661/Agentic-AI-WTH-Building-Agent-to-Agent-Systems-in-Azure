"""Register the AlertManagerAgent with Azure AI Foundry (resilient stub).

Modeled after `register_anomaly.py` and `register_optimizer.py`.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from current or parent directories
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
    print("No .env found; relying on process environment variables.")

# Normalize endpoint / api key env var names
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

# Try to import real client
try:
    from azure.ai.agents import AgentsClient as _RealAgentsClient
    REAL_AGENTS_CLIENT = True
except Exception:
    _RealAgentsClient = None
    REAL_AGENTS_CLIENT = False


class AgentClient:
    def __init__(self):
        self._client = None
        self._ready = False
        if REAL_AGENTS_CLIENT:
            endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
            credential = None
            try:
                from azure.identity import DefaultAzureCredential
                credential = DefaultAzureCredential()
            except Exception:
                credential = None

            if endpoint and credential is not None:
                try:
                    self._client = _RealAgentsClient(endpoint=endpoint, credential=credential)
                    self._ready = True
                    print("Real AgentsClient instantiated")
                    return
                except Exception as e:
                    print("Failed to instantiate real AgentsClient:", e)

        print("AgentClient fallback: using lightweight stub")

    def register_agent(self, agent):
        if self._client is not None and self._ready:
            try:
                return self._client.create_agent(
                    model=agent.model,
                    name=agent.name,
                    instructions=agent.instructions,
                    tools=agent.tools,
                )
            except Exception as e:
                print("Error during agent registration:", e)
                return False
        else:
            print(f"Fallback register_agent called for {agent.__class__.__name__}")
            return True


from alert_manager import AlertManagerAgent


def main():
    client = AgentClient()
    agent = AlertManagerAgent()
    client.register_agent(agent)


if __name__ == "__main__":
    main()
