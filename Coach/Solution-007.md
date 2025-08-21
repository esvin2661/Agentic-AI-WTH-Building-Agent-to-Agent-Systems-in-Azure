
⚠️ Challenge 007: Simulate Anomalies (Using Real Azure Data When No Anomalies Exist)
🎯 Goal:
Use real Azure metrics and inject controlled triggers to simulate anomalies when none are naturally present.

✅ Step-by-Step Strategy
🧠 Step 1: Confirm Real-Time Monitoring Is Active
Your Monitor Agent is already configured to:

Collect metrics like CPU, memory, and disk I/O
Feed data to the Anomaly Detector

Challenge 002 Build and Deploy Core Agents 1
Ensure it's running and connected to Azure Monitor.

🧪 Step 2: Use Time-Based or Threshold-Based Triggers
From your Challenge 003 Build and Deploy Core Agents and Challenge 007 Simulate Anomalies 1:

Challenge 003 Build and Deploy Core Agents+1

Set thresholds slightly lower than normal to catch borderline casesCPU > 60%
Memory < 2GB
Disk I/O > 30MB/sec
This allows your Anomaly Detector to flag real but non-critical spikes.

🧪 Step 3: Inject Controlled Load (Optional)
If you want to force anomalies:

Run a CPU-intensive script on your VM
Allocate memory-heavy processes
Simulate disk reads/writes
Example (Python):

Python

```
# Simulate CPU load
import multiprocessing
def cpu_stress():
    while True:
        pass

for _ in range(multiprocessing.cpu_count()):
    multiprocessing.Process(target=cpu_stress).start()
```

📊 Step 4: Observe Agent Responses
Your agents should:

Detect the anomaly
Log the event
Trigger optimization and alerting workflows

Challenge 003 Build and Deploy Core Agents
Use your dashboard from Challenge 006 to visualize the flow.

Challenge 006 Monitor and Visualize

🧠 Step 5: Document Edge Cases
From your project breakdown:cloud

Note which anomalies are missed
Track how agents recover
Log alert escalation paths

✅ You’ve now completed Challenge 007 using real Azure metrics with controlled triggers to simulate anomalies.
