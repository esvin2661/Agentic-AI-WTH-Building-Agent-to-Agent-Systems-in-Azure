Challenge 003.1: Build the Anomaly Detector Agent (Real Azure Metrics)
Goal:Build an agent that monitors real-time Azure metrics and detects anomalies in:

CPU Usage 
Memory Availability 
Disk I/O 

 Step 1: Install Required Python Packages
In your virtual environment:
pip install azure-monitor-query azure-identity python-dotenv

Step 2: Set Up Your .env File
In your project root, create or update .env with:

```Python
AZURESUBSCRIPTIONID=your-subscription-id
AZURERESOURCEGROUP=your-resource-group
AZURERESOURCENAME=your-vm-name
AZURE_METRICS=Percentage CPU,Available Memory Bytes,Disk Read Bytes/sec
```

Replace the values with your actual Azure VM details.

Step 3: Create the Agent File
Create a file named anomaly_detector.py and paste this code:

```Python
import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient
from azure.monitor.query.models import MetricAggregationType
from azure.ai.foundry import Agent, Message, Thread
from dotenv import loaddotenv
from datetime import timedelta

loaddotenv()

class AnomalyDetectorAgent(Agent):
    def init(self):
        super().init(name="anomaly-detector")
        self.client = MetricsQueryClient(credential=DefaultAzureCredential())
        self.resourceid = (
            f"/subscriptions/{os.getenv('AZURESUBSCRIPTIONID')}"
            f"/resourceGroups/{os.getenv('AZURERESOURCEGROUP')}"
            f"/providers/Microsoft.Compute/virtualMachines/{os.getenv('AZURERESOURCENAME')}"
        )
        self.metrics = [m.strip() for m in os.getenv("AZUREMETRICS").split(",")]

    def getlatestmetric(self, metricname):
        response = self.client.queryresource(
            resourceuri=self.resourceid,
            metricnames=[metricname],
            timespan=timedelta(minutes=5),
            aggregations=[MetricAggregationType.AVERAGE]
        )
        for metric in response.metrics:
            for timeseries in metric.timeseries:
                for data in timeseries.data:
                    if data.average is not None:
                        return data.average
        return None

    def run(self, thread: Thread, message: Message):
        anomalies = []
        for metric in self.metrics:
            value = self.getlatestmetric(metric)
            print(f"{metric}: {value}")
            if value is None:
                continue
            if (
                ("CPU" in metric and value > 75) or
                ("Memory" in metric and value < 1e9) or  # Less than 1GB available
                ("Disk" in metric and value > 5e7)       # More than ~50MB/sec
            ):
                anomalies.append(f"{metric} = {value}")

        if anomalies:
            alert = "⚠️ Anomalies detected:\n" + "\n".join(anomalies)
            thread.send_message(Message(content=alert, role="agent"))
        else:
            print("No anomalies detected.")
```

Step 4: Register the Agent
Create a script called ```register_anomaly.py:```
```Python
from azure.ai.foundry import AgentClient
from anomalydetector import AnomalyDetectorAgent

client = AgentClient()
agent = AnomalyDetectorAgent()
client.registeragent(agent)

Run it:
python register_anomaly.py
```
Step 5: Test the Agent
Create a test script ```test_anomaly.py:```

```Python
from azure.ai.foundry import AgentClient

client = AgentClient()
thread = client.createthread()
client.sendmessage(thread.id, "Run anomaly check", agent_name="anomaly-detector")

Run it:
python test_anomaly.py
You should see real metric values printed and alerts if thresholds are exceeded.
```
Your Anomaly Detector Agent is now live and monitoring real Azure metrics.
We are building the Resource Optimizer Agent next

2. Resource Optimizer Agent: 

 ⚙️ Challenge 003.2: Build the Resource Optimizer Agent (Real Azure Integration)
🎯 Goal:
Respond to real anomaly threads (e.g., high CPU, low memory, high disk I/O) and simulate or apply optimizations using Azure APIs.

Step 1: Install Azure Management SDKs
These will allow your agent to interact with Azure resources:
pip install azure-mgmt-compute azure-identity

Step 2: Update .env with Resource Info
Add these to your .env file:
```Python
AZURESUBSCRIPTIONID=your-subscription-id
AZURERESOURCEGROUP=your-resource-group
AZUREVMNAME=your-vm-name
```

Step 3: Create the Agent File
Create ```resource_optimizer.py``` and paste this:
```Python
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.ai.foundry import Agent, Message, Thread
from dotenv import loaddotenv

loaddotenv()

class ResourceOptimizerAgent(Agent):
    def init(self):
        super().init(name="resource-optimizer")
        self.subscriptionid = os.getenv("AZURESUBSCRIPTIONID")
        self.resourcegroup = os.getenv("AZURERESOURCEGROUP")
        self.vmname = os.getenv("AZUREVMNAME")
        self.computeclient = ComputeManagementClient(
            credential=DefaultAzureCredential(),
            subscriptionid=self.subscriptionid
        )

    def run(self, thread: Thread, message: Message):
        print("Optimizer received:", message.content)
        response = ""

        if "CPU" in message.content:
            response = self.scalevm("StandardDS2v2")  # Example: scale up
        elif "Memory" in message.content:
            response = "🛠️ Suggest restarting memory-heavy services."
        elif "Disk" in message.content:
            response = "🛠️ Suggest enabling disk caching or cleanup."

        thread.sendmessage(Message(content=response, role="agent"))

    def scalevm(self, newsize):
        try:
            print(f"Scaling VM {self.vmname} to {newsize}")
            vm = self.computeclient.virtualmachines.get(self.resourcegroup, self.vmname)
            vm.hardwareprofile.vmsize = newsize
            poller = self.computeclient.virtualmachines.begincreateorupdate(
                self.resourcegroup, self.vmname, vm
            )
            poller.result()
            return f"✅ VM scaled to {new_size}"
        except Exception as e:
            return f"❌ Failed to scale VM: {str(e)}"
```

Step 4: Register the Agent
Create ```register_optimizer.py:```
```Python
from azure.ai.foundry import AgentClient
from resourceoptimizer import ResourceOptimizerAgent

client = AgentClient()
agent = ResourceOptimizerAgent()
client.registeragent(agent)

Run it:
python register_optimizer.py
```

Step 5: Test the Agent
```Create test_optimizer.py:```
```Python
from azure.ai.foundry import AgentClient

client = AgentClient()
thread = client.createthread()
client.sendmessage(thread.id, "⚠️ Anomaly detected: Percentage CPU = 92", agent_name="resource-optimizer")

Run it:
python test_optimizer.py
```
You should see:
VM scaled to Standard_DS2_v2


That’s it! Your Resource Optimizer Agent is now live and can respond to real anomalies with real Azure actions.
Would you like to move on to building the 🚨 Alert Manager Agent next?

3. Copilot Alert Manager Agent: 

 🚨 Challenge 003.3: Build the Alert Manager Agent (Live Azure Integration)
🎯 Goal:
Monitor real anomaly and optimization threads, and send alerts to stakeholders using Azure Monitor’s alerting and action group infrastructure.

Step 1: Confirm You’re in an Azure Monitor Action Group
You’re already part of the AGOwner action group, which means you’ll receive notifications triggered by Azure Monitor alerts1.

Step 2: Install Required SDKs
pip install azure-monitor-query azure-identity azure-mgmt-monitor

Step 3: Update .env with Alert Info
```
AZURESUBSCRIPTIONID=your-subscription-id
AZURERESOURCEGROUP=your-resource-group
AZUREACTIONGROUP_NAME=AGOwner
```

Step 4: Create the Agent File
Create ```alert_manager.py``` and paste this:
```Python
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient
from azure.ai.foundry import Agent, Message, Thread
from dotenv import loaddotenv

loaddotenv()

class AlertManagerAgent(Agent):
    def init(self):
        super().init(name="alert-manager")
        self.subscriptionid = os.getenv("AZURESUBSCRIPTIONID")
        self.resourcegroup = os.getenv("AZURERESOURCEGROUP")
        self.monitorclient = MonitorManagementClient(
            credential=DefaultAzureCredential(),
            subscriptionid=self.subscriptionid
        )

    def run(self, thread: Thread, message: Message):
        print("Alert Manager received:", message.content)

        if "Anomaly" in message.content or "Optimization" in message.content:
            alertmsg = f"🚨 Alert triggered: {message.content}"
            thread.sendmessage(Message(content=alertmsg, role="agent"))
            print("Sending alert to Azure Monitor action group…")
            self.sendalert(alertmsg)

    def sendalert(self, alertmsg):
```
        # Simulate sending alert (real implementation would use Azure Monitor alert rule)


🔧 Note: Azure Monitor alerts are typically configured via the Azure Portal or ARM templates. This agent simulates the alert logic and can be extended to trigger real alerts via REST API or Logic Apps.


Step 5: Register the Agent
Create ```register_alert.py:```

```Python
from azure.ai.foundry import AgentClient
from alertmanager import AlertManagerAgent

client = AgentClient()
agent = AlertManagerAgent()
client.registeragent(agent)

Run it:
python register_alert.py
```
Step 6: Test the Agent
```Create test_alert.py:```
```Python
from azure.ai.foundry import AgentClient

client = AgentClient()
thread = client.createthread()
client.sendmessage(thread.id, "⚠️ Optimization failed due to high CPU usage", agent_name="alert-manager")

Run it:
python test_alert.py
You should see:
🚨 Alert triggered: ⚠️ Optimization failed due to high CPU usage
Simulated alert sent: 🚨 Alert triggered: ⚠️ Optimization failed due to high CPU usage
```

The Alert Manager Agent is now live and ready to respond to real anomaly and optimization events.
We are building the 🔗 Agent-to-Agent Communication Layer next

References
[1] You’re now in the AGOwner action group

4: Agent to Agent communication layer

Finally, Once all the layers are connected you will be able to: 

Route messages between agents 
Maintain shared memory (via threads) 
Optionally use Semantic Kernel or Autogen v2 for planning 
Support retries and orchestration logic 

 🔗 Challenge 003.4: Build the Agent-to-Agent Communication Layer
🎯 Goal:
Enable your agents (Anomaly Detector, Resource Optimizer, Alert Manager) to communicate and collaborate using threads and shared context.

Step 1: Create the Communication Layer File
Create a new file:
```touch agent_orchestrator.py```

Step 2: Define the Orchestrator Logic
```Paste this into agent_orchestrator.py:```

```Python
from azure.ai.foundry import AgentClient, Thread
from dotenv import loaddotenv
import os

loaddotenv()

class AgentOrchestrator:
    def init(self):
        self.client = AgentClient()
        self.agents = {
            "anomaly": "anomaly-detector",
            "optimizer": "resource-optimizer",
            "alert": "alert-manager"
        }

    def createthread(self):
        return self.client.createthread()

    def sendtoagent(self, thread: Thread, agentkey: str, message: str):
        agentname = self.agents.get(agentkey)
        if not agentname:
            print(f"Unknown agent: {agentkey}")
            return
        self.client.sendmessage(thread.id, message, agentname=agentname)

    def orchestrate(self):
        thread = self.createthread()
        print("🧠 Step 1: Trigger Anomaly Detector")
        self.sendtoagent(thread, "anomaly", "Check system metrics")

        print("⚙️ Step 2: Trigger Resource Optimizer")
        self.sendtoagent(thread, "optimizer", "Respond to detected anomalies")

        print("🚨 Step 3: Trigger Alert Manager")
        self.sendto_agent(thread, "alert", "Notify stakeholders of critical issues")

        print("✅ Orchestration complete.")
```


Step 3: Run the Orchestrator
Create a script called ```run_orchestrator.py:```
```Python
from agent_orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()
orchestrator.orchestrate()

Run it:
python run_orchestrator.py
You should see each agent triggered in sequence, with messages routed through a shared thread.
```
Step 4 (Optional): Add Semantic Kernel Planning
If you want to use Semantic Kernel to decide which agent to trigger based on user input:
```Python
from semantickernel import Kernel

kernel = Kernel()
plan = kernel.createplan("Detect and respond to system anomalies")
```


