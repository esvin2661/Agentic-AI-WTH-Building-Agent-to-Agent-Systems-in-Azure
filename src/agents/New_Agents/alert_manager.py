import json
from typing import Dict


class AlertManagerAgent:
    """Agent that formats and sends alerts for critical events.

    Lightweight, simulation-first implementation. In a production setup this
    would integrate with email/SMS/Teams/webhooks and the orchestrator's
    messaging primitives.
    """

    def __init__(self):
        self.name = "AlertManagerAgent"
        self.model = "gpt-35-turbo"
        self.instructions = "Monitor threads for critical events and notify stakeholders. Escalate unresolved issues."
        self.tools = []
        self.description = "Agent that formats and sends alerts based on anomaly and optimization outputs."

    def format_alert(self, event: Dict) -> Dict:
        """Create a standardized alert dict from an event dict."""
        return {
            "severity": event.get("severity", "high"),
            "message": f"🚨 Alert: {event.get('message')}",
            "action": event.get("action", "Notify stakeholders"),
            "status": event.get("status", "pending"),
        }

    def send_alert(self, alert: Dict) -> Dict:
        """Send or simulate sending the alert. Returns a result dict."""
        # Simulation: print JSON to stdout. Replace with real delivery code.
        print("Sending alert...")
        print(json.dumps(alert, indent=2))
        return {"status": "sent", "alert": alert}


if __name__ == "__main__":
    # Quick manual test
    agent = AlertManagerAgent()
    sample_event = {"message": "High CPU on vm-01", "severity": "critical"}
    alert = agent.format_alert(sample_event)
    res = agent.send_alert(alert)
    print("Result:", res)
