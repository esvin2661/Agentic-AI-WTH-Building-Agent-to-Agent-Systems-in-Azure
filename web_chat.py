from flask import Flask, request, render_template_string, redirect, session, url_for
import asyncio
import sys
import os
import importlib.util
import contextlib
import io

app = Flask(__name__)
app.secret_key = "dev-secret-for-local-testing-only"

BASE_DIR = os.path.dirname(__file__)
AGENTS_PATH = os.path.join(BASE_DIR, "src", "agents")
if AGENTS_PATH not in sys.path:
    sys.path.insert(0, AGENTS_PATH)

# Robustly load agent_orchestrator.handle_user_input
handle_user_input_fn = None
try:
    from agent_orchestrator import handle_user_input as handle_user_input_fn
except Exception:
    try:
        spec = importlib.util.spec_from_file_location(
            "agent_orchestrator",
            os.path.join(AGENTS_PATH, "agent_orchestrator.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        handle_user_input_fn = getattr(mod, "handle_user_input", None)
    except Exception as e:
        print("Warning: could not load agent_orchestrator:", e)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Agentic AI Chat</title>
  <style>
    body { font-family: Arial, sans-serif; background:#f4f4f9; padding:24px }
    .card { max-width:900px; margin:24px auto; background:#fff; padding:20px; border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,0.06) }
    .controls { display:flex; gap:8px; align-items:center }
    input[type=text] { flex:1; padding:10px; font-size:15px }
    button { padding:10px 14px; font-size:15px; background:#0078D4; color:#fff; border:none; cursor:pointer }
    .response { white-space:pre-wrap; margin-top:18px; background:#eef; border:1px solid #0078D4; padding:12px; border-radius:6px }
    .meta { color:#666; font-size:13px; margin-top:8px }
  </style>
</head>
<body>
  <div class="card">
    <h2>Agentic AI Chat</h2>
    <form method="post" action="/chat" class="controls">
      <input type="text" name="user_input" placeholder="Ask about a metric (eg: Percentage CPU) or ask something else" required>
      <button type="submit">Send</button>
      <button formaction="/clear" formmethod="post" style="background:#888">Clear</button>
    </form>
    <div class="meta">Note: responses are scoped to the resource/metrics configured for the agents; unrelated questions return an out-of-scope reply.</div>

    {% if response %}
      <div class="response">{{ response }}</div>
    {% endif %}
  </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("chat"))


@app.route("/chat", methods=["GET", "POST"])
def chat():
    response = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input:
            if handle_user_input_fn is None:
                response = "Error: agent orchestrator not available. Check server logs."
            else:
                # Capture printed output from the agents and present it along with structured results
                out_buf = io.StringIO()
                err_buf = io.StringIO()
                try:
                    with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
                        try:
                            result = asyncio.run(handle_user_input_fn(user_input))
                        except RuntimeError:
                            # fallback when event loop already active
                            import nest_asyncio
                            nest_asyncio.apply()
                            result = asyncio.get_event_loop().run_until_complete(handle_user_input_fn(user_input))
                finally:
                    printed = out_buf.getvalue() or ""
                    printed_err = err_buf.getvalue() or ""

                # Normalize result to string
                if isinstance(result, (list, tuple)):
                    structured = "\n".join(str(r) for r in result)
                else:
                    structured = str(result)

                parts = []
                if printed.strip():
                    parts.append(printed.strip())
                if printed_err.strip():
                    parts.append("STDERR:\n" + printed_err.strip())
                if structured.strip():
                    parts.append(structured.strip())
                response = "\n\n".join(parts) if parts else "(no response)"
    return render_template_string(HTML_TEMPLATE, response=response)


@app.route("/clear", methods=["POST"])
def clear():
    # For a simple UI we don't persist conversation; clear returns to the chat page with no response
    return redirect(url_for("chat"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
