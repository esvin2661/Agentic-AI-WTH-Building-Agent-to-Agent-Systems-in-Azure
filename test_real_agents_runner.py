"""Run a simple test of the real agents using the orchestrator function.
This runner creates a small Orchestrator shim that provides the methods
expected by `orchestratedynamic` in `src/agents/agent_orchestrator.py`.
"""
import sys
import os
import re

# Ensure the New_Agents folder is importable
ROOT = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.join(ROOT, "src", "agents", "New_Agents")
if AGENTS_DIR not in sys.path:
    sys.path.insert(0, AGENTS_DIR)

# Import agent implementations by file path so imports work reliably from any CWD
import importlib.util

anomaly_path = os.path.join(AGENTS_DIR, "anomaly_detector.py")
resource_path = os.path.join(AGENTS_DIR, "resource_optimizer.py")

def load_module_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

anomaly_mod = load_module_from_path("anomaly_detector", anomaly_path)
resource_mod = load_module_from_path("resource_optimizer", resource_path)

AnomalyDetectorAgent = getattr(anomaly_mod, "AnomalyDetectorAgent")
ResourceOptimizer = getattr(resource_mod, "ResourceOptimizer")

# Import the orchestrator function
from src.agents.agent_orchestrator import orchestratedynamic


class ThreadStub:
    def __init__(self):
        self.messages = []

    def send_message(self, msg):
        # Accept either module Message objects or simple strings/dicts
        try:
            content = msg.content
        except Exception:
            content = str(msg)
        self.messages.append(type("M", (), {"role": getattr(msg, "role", "agent"), "content": content}))


class OrchestratorShim:
    def __init__(self):
        self.thread = None
        # Instantiate agents
        self.anomaly = AnomalyDetectorAgent()
        # Use ResourceOptimizer for logic but wrap behavior for simple message creation
        self.optimizer = ResourceOptimizer(dry_run=True)

    def createthread(self):
        self.thread = ThreadStub()
        return self.thread

    def sendtoagent(self, thread, agent_name, message_content):
        print(f"sendtoagent -> {agent_name}: {message_content}")
        # Build a minimal message object expected by agents
        class Msg:
            def __init__(self, content, role="user"):
                self.content = content
                self.role = role

        msg = Msg(content=message_content, role="user")

        if agent_name == "anomaly":
            # Call the anomaly detector's run method
            try:
                self.anomaly.run(thread, msg)
            except Exception as e:
                print("Anomaly agent run failed:", e)
        elif agent_name == "optimizer":
            # Simulate parsing anomaly message and produce an optimization result
            # We'll look for numeric values in the message and provide a recommendation
            text = message_content
            nums = [float(n) for n in re.findall(r"\d+\.?\d*", text)]
            if nums:
                val = nums[0]
                rec = self.optimizer.recommend_action("cpu", val)
                res = self.optimizer.apply_action(rec)
                opt_msg = f"🛠️ Optimization: {res.get('message', str(res))}"
            else:
                opt_msg = "🛠️ Optimization: no numeric metrics parsed; simulated recommendation"
            try:
                thread.send_message(type("M", (), {"role": "agent", "content": opt_msg}))
            except Exception as e:
                print("Failed to send optimizer message:", e)
        elif agent_name == "alert":
            alert_msg = f"ALERT: {message_content}"
            thread.send_message(type("M", (), {"role": "agent", "content": alert_msg}))
        else:
            # Unknown agent - echo as agent
            thread.send_message(type("M", (), {"role": "agent", "content": f"{agent_name}: {message_content}"}))

    def getthreadmessages(self, thread):
        return getattr(thread, "messages", [])


def run_test():
    orchestrator = OrchestratorShim()
    # Call the orchestratedynamic function (it expects 'self' as first arg)
    results = orchestratedynamic(orchestrator, "Check CPU usage", use_semantic_kernel=False)
    print("\nFinal messages:")
    for line in results:
        print(line)


if __name__ == "__main__":
    run_test()
