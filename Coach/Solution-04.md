<h1> Challenge 004: Enable Agentic Communication (A2A) </h1>

Goal:Build a communication layer that allows agents to:

Share context via threads 
Pass messages between each other 
Coordinate actions based on shared memory 
Optionally use Semantic Kernel or Autogen v2 for planning 

Step 1: Use Shared Threads for Context

You’ve already started this in your orchestrator. Let’s make it more dynamic by allowing agents to respond to each other’s messages.
Update agent_orchestrator.py:

```Python
def orchestratedynamic(self, userinput):
    thread = self.createthread()

    # Step 1: Anomaly Detector
    self.sendtoagent(thread, "anomaly", userinput)

    # Step 2: Read anomaly message
    messages = self.getthreadmessages(thread)
    anomalymsg = next((m.content for m in messages if "Anomaly" in m.content), None)

    # Step 3: Resource Optimizer
    if anomalymsg:
        self.sendtoagent(thread, "optimizer", anomalymsg)

    # Step 4: Read optimization message
    messages = self.getthreadmessages(thread)
    optimizationmsg = next((m.content for m in messages if "🛠️" in m.content), None)

    # Step 5: Alert Manager
    if optimizationmsg:
        self.sendtoagent(thread, "alert", optimizationmsg)

    return self.getthreadmessages(thread)
```


 Step 2: Update Flask App to Use Dynamic Orchestration
 
In app.py, update the handler:
```Python 
async def handleuserinput(userinput):
    messages = orchestrator.orchestratedynamic(user_input)
    return [msg.content for msg in messages]
```

Step 3: Add Agent Role Awareness (Optional)

You can tag each message with the agent’s name or role for clarity:
```Python
return [f"{msg.role}: {msg.content}" for msg in messages]
```
Step 4: (Optional) Use Semantic Kernel for Planning

If you want to use Semantic Kernel to decide which agent to trigger:

```Python
from semantickernel import Kernel
```
```Python 
kernel = Kernel()
plan = kernel.createplan("Detect and respond to system anomalies")
for step in plan.steps:
    # Route step to appropriate agent
    orchestrator.sendtoagent(thread, step.plugin_name, step.description)
```

That’s it! You now have a working Agent-to-Agent Communication Layer that dynamically routes messages and coordinates actions.



