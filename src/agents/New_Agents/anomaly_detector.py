import os
import importlib
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv

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

# Resolve MetricsQueryClient and MetricAggregationType across package versions
def _resolve_class(possible_modules, class_name):
    for mod_path in possible_modules:
        try:
            mod = importlib.import_module(mod_path)
            cls = getattr(mod, class_name, None)
            if cls:
                return cls
        except Exception:
            continue
    return None

MetricsQueryClient = _resolve_class([
    "azure.monitor.query",
    "azure.monitor.query.metrics",
    "azure.monitor.query._metrics",
    "azure.monitor.query._client",
    "azure.monitor.query._generated.metrics_client",
], "MetricsQueryClient")

MetricAggregationType = _resolve_class([
    "azure.monitor.query.models",
    "azure.monitor.query",
    "azure.monitor.query._models",
], "MetricAggregationType")

if MetricsQueryClient is None:
    try:
        import azure.monitor.query as _amq
        available = [n for n in dir(_amq) if not n.startswith("__")]
    except Exception:
        available = None
    msg = "MetricsQueryClient not found in azure.monitor.query; metrics functionality will be disabled."
    if available is not None:
        msg += f" Available names in azure.monitor.query: {available}"
    print(msg)

if MetricAggregationType is None:
    class MetricAggregationType:
        AVERAGE = "Average"

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
        # Required attributes for Foundry registration
        self.name = "AnomalyDetectorAgent"
        self.model = "gpt-35-turbo"
        self.instructions = "Detect anomalies in Azure metrics like CPU, memory, and disk I/O."
        self.tools = []  # Add OpenApiTool instances here if needed

        # Initialize base agent
        try:
            super().__init__(name=self.name)
        except TypeError:
            super().__init__()

        # Metrics client (optional)
        try:
            from azure.identity import DefaultAzureCredential
            self.client = MetricsQueryClient(credential=DefaultAzureCredential()) if MetricsQueryClient else None
        except Exception:
            self.client = None
            print("Warning: could not instantiate MetricsQueryClient; metrics disabled.")

        # Build resource ID based on resource type
        subscription = os.getenv("AZURESUBSCRIPTIONID", "")
        rg = os.getenv("AZURERESOURCEGROUP", "")
        resource = os.getenv("AZURERESOURCENAME", "")
        resource_type = os.getenv("AZURERESOURCETYPE", "webapp").lower()

        if resource_type == "webapp":
            self.resource_id = (
                f"/subscriptions/{subscription}/resourceGroups/{rg}"
                f"/providers/Microsoft.Web/sites/{resource}"
            )
        elif resource_type == "foundry":
            self.resource_id = (
                f"/subscriptions/{subscription}/resourceGroups/{rg}"
                f"/providers/Microsoft.CognitiveServices/accounts/{resource}"
            )
        else:
            self.resource_id = ""
            print("Unsupported resource type specified in AZURERESOURCETYPE.")

        metrics_env = os.getenv("AZUREMETRICS", "")
        self.metrics = [m.strip() for m in metrics_env.split(",") if m.strip()]

    def get_latest_metric(self, metric_name: str):
        if not self.client:
            return None
        try:
            response = self.client.query_resource(
                resource_id=self.resource_id,
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
            print(f"Error querying metric {metric_name}: {e}")
        return None

    def run(self, thread, message):
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