
🎯 Goal:
Track when anomalies are detected and how they are resolved by your agents, using logs and visual summaries.

 Step 1: Log Anomalies and Resolutions
Update each agent to log its actions to a local file or database.
Example for Anomaly Detector:

```
import logging

logging.basicConfig(filename='agentlog.txt', level=logging.INFO)

def loganomaly(metric, value):
    logging.info(f"Anomaly Detected: {metric} = {value}")

Example for Resource Optimizer:

def log_resolution(action):
    logging.info(f"Resolution Applied: {action}")
```

 Step 2: Structure the Log Format
Use a consistent format like:
```
[2025-08-21 14:32:10] Anomaly Detected: CPU = 92%
[2025-08-21 14:32:15] Resolution Applied: Scaled VM to Standard_DS2_v2
```

 Step 3: Visualize with Streamlit (Optional)
Create a simple dashboard to display logs:

```
import streamlit as st

st.title("Anomaly & Resolution Tracker")

with open("agent_log.txt") as f:
    logs = f.readlines()

for line in logs:
    st.text(line.strip())

Run with:

streamlit run dashboard.py
```

 Step 4: (Optional) Store Logs in Azure Table or Cosmos DB
If you want cloud-based tracking:

Use azure-data-tables or azure-cosmos SDK 
Store each anomaly and resolution as a record 
Query and visualize with Power BI or Azure Workbooks 

That’s it! You now have a lightweight system to track and visualize anomalies and resolutions.

