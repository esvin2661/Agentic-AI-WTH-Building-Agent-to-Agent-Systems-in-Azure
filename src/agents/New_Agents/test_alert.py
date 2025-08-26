from alert_manager import AlertManagerAgent


def run_test():
    agent = AlertManagerAgent()
    event = {"message": "High CPU on vm-01", "severity": "critical", "action": "Investigate"}
    alert = agent.format_alert(event)
    result = agent.send_alert(alert)
    print("Test result:", result)


if __name__ == "__main__":
    run_test()
