import os
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Load .env using find_dotenv so it works even when the script is run from a different cwd
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path=dotenv_path)
    print(f"Loaded .env from: {dotenv_path}")
else:
    print("No .env file found by find_dotenv(); environment variables will come from the process environment.")

# Debug: show presence of expected keys (do NOT print secret values)
for _k in ("AZURESUBSCRIPTIONID", "AZURERESOURCEGROUP", "AZURERESOURCENAME", "AZUREMETRICS"):
    print(f"{_k}:", "present" if os.getenv(_k) else "missing")

# Normalize foundry endpoint/api key environment variable names
_endpoint_aliases = [
    "AZURE_AI_FOUNDRY_ENDPOINT",
    "AZUREAIFOUNDRYENDPOINT",
    "AZURE_AI_FOUNDRY",
    "AZURE_AI_FOUNDRY_URL",
]
_apikey_aliases = [
    "AZURE_AI_FOUNDRY_API_KEY",
    "AZUREAIFOUNDRYAPI_KEY",
    "AZUREAIFOUNDRYAPIKEY",
    "AZURE_AI_FOUNDRY_KEY",
    "AZURE_AGENT_API_KEY",
    "AZURE_API_KEY",
]

for name in _endpoint_aliases:
    v = os.getenv(name)
    if v:
        os.environ["AZURE_AI_FOUNDRY_ENDPOINT"] = v
        break

for name in _apikey_aliases:
    v = os.getenv(name)
    if v:
        os.environ["AZURE_AI_FOUNDRY_API_KEY"] = v
        break

# Import MetricsQueryClient and MetricAggregationType
try:
    from azure.monitor.query import MetricsQueryClient, MetricAggregationType
except ImportError:
    MetricsQueryClient = None
    MetricAggregationType = None
    print("MetricsQueryClient not found in azure.monitor.query; metrics functionality will be disabled.")

# Fallback for environments without azure.ai.agents
try:
    from azure.ai.agents import Agent, Message, Thread
except Exception:
    class Agent:
        def __init__(self, *args, **kwargs):
            pass

    class Message:
        def __init__(self, content: str = "", role: str | None = None):
            self.content = content
            self.role = role

    class Thread:
        def send_message(self, msg):
            print("Thread.send_message:", getattr(msg, "content", msg))

class AnomalyDetectorAgent(Agent):
    def __init__(self):
        self.name = "AnomalyDetectorAgent"
        self.model = "gpt-35-turbo"
        self.instructions = "Detect anomalies in Azure metrics like CPU, memory, and disk I/O."
        self.tools = []

        try:
            super().__init__(name=self.name)
        except TypeError:
            super().__init__()

        try:
            from azure.identity import DefaultAzureCredential
            self.client = MetricsQueryClient(credential=DefaultAzureCredential()) if MetricsQueryClient else None
        except Exception:
            self.client = None
            print("Warning: could not instantiate MetricsQueryClient; metrics disabled.")

        subscription = os.getenv("AZURESUBSCRIPTIONID", "")
        rg = os.getenv("AZURERESOURCEGROUP", "")
        resource = os.getenv("AZURERESOURCENAME", "")
        resource_type = (os.getenv("AZURERESOURCETYPE", "webapp") or "").strip().lower()

        # If the user provided a full resource id, use it directly
        if resource and resource.strip().lower().startswith("/subscriptions/"):
            self.resource_id = resource.strip()
        else:
            # Accept a few common aliases for resource types
            if resource_type in ("webapp", "web_app", "app", "site"):
                self.resource_id = (
                    f"/subscriptions/{subscription}/resourceGroups/{rg}"
                    f"/providers/Microsoft.Web/sites/{resource}"
                )
            elif resource_type in ("foundry", "cognitive", "ai", "aiplatform"):
                self.resource_id = (
                    f"/subscriptions/{subscription}/resourceGroups/{rg}"
                    f"/providers/Microsoft.AIPlatform/accounts/{resource}"
                )
            # Accept provider-style or longer forms like 'microsoft.compute/virtualmachines'
            elif resource_type in ("virtualmachine", "virtual_machine", "vm") or any(k in resource_type for k in ("compute", "virtualmach", "microsoft.compute")):
                # Virtual machine resource id
                self.resource_id = (
                    f"/subscriptions/{subscription}/resourceGroups/{rg}"
                    f"/providers/Microsoft.Compute/virtualMachines/{resource}"
                )
            else:
                self.resource_id = ""
                print(f"Unsupported resource type specified in AZURERESOURCETYPE: '{resource_type}'.")

        # Debug: show resolved resource id
        print(f"Resolved resource_id: {self.resource_id}")

        metrics_env = os.getenv("AZUREMETRICS", "")
        self.metrics = [m.strip() for m in metrics_env.split(",") if m.strip()]

    def get_latest_metric(self, metric_name: str):
        if not self.client:
            return None
        try:
            response = self.client.query(
                resource_uri=self.resource_id,
                metric_names=[metric_name],
                timespan=timedelta(minutes=5),
                aggregations=[MetricAggregationType.AVERAGE],
            )
            for metric in getattr(response, "metrics", []):
                for timeseries in getattr(metric, "timeseries", []):
                    for data in getattr(timeseries, "data", []):
                        if getattr(data, "average", None) is not None:
                            return data.average
        except Exception as e:
            # Provide clearer message for authorization errors which are common when
            # DefaultAzureCredential is missing proper RBAC assignments on the target
            msg = str(e)
            if "AuthorizationFailed" in msg or "does not have authorization" in msg:
                print(f"Authorization error querying metric {metric_name}: {e}")
                print("Hint: the identity used by DefaultAzureCredential needs 'Microsoft.Insights/metrics/read' permission on the resource (assign Monitoring Reader/Metric Reader role or similar). If you just granted access, refresh your credentials (re-run 'az login').")
            else:
                print(f"Error querying metric {metric_name}: {e}")
        return None

    def run(self, thread, message):
        print(f"Checking metrics: {self.metrics}")
        anomalies = []
        for metric in self.metrics:
            value = self.get_latest_metric(metric)
            print(f"{metric}: {value}")
            if value is None:
                continue
            if (
                ("CPU" in metric and value > 75)
                or ("Memory" in metric and value < 1e9)
                or ("Disk" in metric and value > 5e7)
            ):
                anomalies.append(f"{metric} = {value}")

        if anomalies:
            alert = "⚠️ Anomalies detected:\n" + "\n".join(anomalies)
            try:
                thread.send_message(Message(content=alert, role="agent"))
            except Exception:
                print(alert)
        else:
            print("No anomalies detected.")

        print("AnomalyDetectorAgent run completed.")

if __name__ == "__main__":
    agent = AnomalyDetectorAgent()
    thread = Thread()
    message = Message(content="Run anomaly check", role="user")
    agent.run(thread, message)