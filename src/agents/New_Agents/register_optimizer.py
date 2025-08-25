
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from current or parent directories
def load_env():
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        candidate = parent / ".env"
        if candidate.exists():
            load_dotenv(dotenv_path=candidate)
            print(f"Loaded .env from: {candidate}")
            return
    print("No .env found; relying on process environment variables.")

load_env()

# Normalize environment variable aliases
endpoint_aliases = [
    "AZUREAIFOUNDRYENDPOINT", "AZUREAIFOUNDRY", "AZUREAIFOUNDRYURL"
]
apikey_aliases = [
    "AZUREAIFOUNDRYAPIKEY", "AZUREAIFOUNDRYKEY", "AZUREAGENTAPIKEY", "AZUREAPIKEY"
]

for name in endpoint_aliases:
    val = os.getenv(name)
    if val:
        os.environ["AZURE_AI_FOUNDRY_ENDPOINT"] = val
        print(f"Endpoint source: {name}")
        break
else:
    print("Endpoint source: missing")

for name in apikey_aliases:
    val = os.getenv(name)
    if val:
        os.environ["AZUREAIFOUNDRYAPIKEY"] = val
        print(f"API key source: {name}")
        break
else:
    print("API key source: missing")

# Try to import the real AgentsClient
try:
    from azure.ai.agents import AgentsClient as RealAgentsClient
    from azure.identity import DefaultAzureCredential
    USE_REAL_CLIENT = True
except Exception as e:
    RealAgentsClient = None
    DefaultAzureCredential = None
    USE_REAL_CLIENT = False
    print("Falling back to stub client due to import error:", e)

class AgentClient:
    def __init__(self):
        self._client = None
        self._ready = False

        if USE_REAL_CLIENT:
            endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
            if endpoint and DefaultAzureCredential:
                try:
                    credential = DefaultAzureCredential()
                    self._client = RealAgentsClient(endpoint=endpoint, credential=credential)
                    self._ready = True
                    print("Real AgentsClient instantiated")
                except Exception as e:
                    print("Failed to instantiate real AgentsClient:", e)

        if not self._ready:
            print("Using fallback stub client")

    def register_agent(self, agent):
        if self._client and self._ready:
            try:
                return self._client.create_agent(
                    model=agent.model,
                    name=agent.name,
                    instructions=agent.instructions,
                    tools=agent.tools,
                    description=agent.description,
                    capabilities=agent.capabilities
                )
            except Exception as e:
                print("Error during agent registration:", e)
                return False
        else:
            print(f"Stub register_agent called for {agent.name}")
            print("Model:", agent.model)
            print("Instructions:", agent.instructions)
            print("Tools:", agent.tools)
            print("Description:", agent.description)
            print("Capabilities:", agent.capabilities)
            return True

# Import or define ResourceOptimizer
try:
    from resource_optimizer import ResourceOptimizer
except Exception:
    class ResourceOptimizer:
        def __init__(self):
            pass

class ResourceOptimizerAgent:
    def __init__(self):
        self.name = "ResourceOptimizerAgent"
        self.model = "gpt-35-turbo"
        self.instructions = "Monitor VM metrics and recommend or apply resource optimizations (resize/restart/cleanup)."
        self.tools = []
        self.description = "Agent that analyzes Azure VM metrics and suggests or applies optimizations to improve performance and reduce cost."
        self.capabilities = ["monitoring", "optimization", "resource-management"]
        try:
            self.optimizer = ResourceOptimizer()
        except Exception:
            self.optimizer = None

def main():
    client = AgentClient()
    agent = ResourceOptimizerAgent()
    client.register_agent(agent)

if __name__ == "__main__":
    main()
