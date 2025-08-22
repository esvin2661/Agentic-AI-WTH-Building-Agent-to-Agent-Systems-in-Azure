<h1>Challenge 005 – Build a Chat Box Interface with Flask</h1>

Goal

Create a simple, interactive Flask-based chat interface that allows users to send queries and receive responses from your orchestrator agent. This chat box will serve as the front-end entry point for your multi-agent system.


<h3> Step 1: Install Required Packages </h3>

You don’t need a separate `requirements.txt` for this challenge. Just run the following commands in your terminal:

```bash
pip install Flask
pip install python-dotenv
pip install semantic-kernel
```

***

Step 2: Create `chatbox.py`

This script launches the Flask app and connects to your orchestrator agent:

```python
from flask import Flask, render_template, request, redirect, url_for
from orchestrator import handle_user_query  # Your orchestrator logic
import os

app = Flask(__name__)
chat_history = []

@app.route("/", methods=["GET", "POST"])
def chat():
    global chat_history
    if request.method == "POST":
        user_input = request.form["message"]
        response = handle_user_query(user_input)
        chat_history.append({"user": user_input, "agent": response})
        return redirect(url_for("chat"))
    return render_template("chat.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
```

***

Step 3: Create `orchestrator.py`

This file contains the logic to route user queries to the appropriate agent. You can expand this later to include real agent calls.

```python
def handle_user_query(query):
    if "cpu" in query.lower():
        return "Monitor Agent: CPU usage is stable at 45%."
    elif "anomaly" in query.lower():
        return "Anomaly Detector Agent: No anomalies detected in the last 24 hours."
    elif "optimize" in query.lower():
        return "Resource Optimizer Agent: Scaling recommendation applied to VM group A."
    elif "alert" in query.lower():
        return "Alert Manager Agent: No active alerts. All systems normal."
    else:
        return "Orchestrator Agent: I’m not sure which agent to route this to. Can you clarify?"
```

***

Step 4: Create the Chat UI

Create a folder named `templates` and inside it, add a file called `chat.html`:

***

Step 5: Run the Chat Box

Start the Flask app:

```bash
python chatbox.py
```

Then open your browser and go to:

    http://localhost:5000

You’ll see a chat interface where you can type queries and receive responses from your agents.

***

Challenge 005 Complete!

You now have a working chat interface that connects to your orchestrator agent and routes queries to your core agents. This sets the stage for **Challenge 006: Monitor and Visualize**.

***

