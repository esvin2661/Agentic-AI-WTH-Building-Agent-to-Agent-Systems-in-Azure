import os
import semantic_kernel as sk


def orchestratedynamic(self, userinput, use_semantic_kernel=False):
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

    # Optional: Use Semantic Kernel for planning
    if use_semantic_kernel:
        try:
            kernel = sk.Kernel()
            plan = kernel.createplan("Detect and respond to system anomalies")
            for step in plan.steps:
                self.sendtoagent(thread, step.plugin_name, step.description)
        except Exception as e:
            print("Semantic Kernel planning failed:", e)

    # Return all messages with role awareness
    messages = self.getthreadmessages(thread)
    return [f"{msg.role}: {msg.content}" for msg in messages]






























    