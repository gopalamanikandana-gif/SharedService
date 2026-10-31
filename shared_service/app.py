from datetime import datetime, timezone
from flask import Flask, jsonify, render_template_string, request
from templates import MESSAGE_SUFFIX

app = Flask(__name__)
notifications = []

DASHBOARD = """
<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shared Service Dashboard</title>
<style>
body{font-family:Arial,sans-serif;background:#f3f6fb;margin:0;color:#172033}
main{max-width:900px;margin:40px auto;padding:24px}
.card{background:white;padding:24px;border-radius:14px;box-shadow:0 5px 20px #10204012;margin:16px 0}
h1{margin-bottom:8px}code{background:#eef2ff;padding:3px 7px;border-radius:5px}
a{color:#2456c5}li{margin:8px 0}.badge{display:inline-block;background:#dff8e8;color:#17663a;padding:5px 9px;border-radius:99px}
</style></head><body><main>
<h1>Reusable Shared Notification Service</h1>
<p>SOA Task 3 · Central REST API used by two client applications</p>
<div class="card"><span class="badge">Service running</span>
<h2>Current shared template</h2><p>{{ suffix }}</p>
<p>Both client apps retrieve this centrally configured template through the API.</p></div>
<div class="card"><h2>API endpoints</h2><ul>
<li><code>GET /health</code> — service status</li>
<li><code>GET /api/v1/template</code> — current shared message format</li>
<li><code>POST /api/v1/notifications</code> — create a notification</li>
<li><code>GET /api/v1/notifications</code> — list notifications</li></ul></div>
<div class="card"><h2>Client applications</h2>
<ul><li><a href="http://127.0.0.1:5001">Smart Campus Canteen (port 5001)</a></li>
<li><a href="http://127.0.0.1:5002">Student Management (port 5002)</a></li></ul></div>
<div class="card"><h2>Try the update</h2><p>Edit <code>shared_service/templates.py</code>, change <code>MESSAGE_SUFFIX</code>, restart this service, then submit a notification in each client app.</p></div>
</main></body></html>
"""

@app.get("/")
def dashboard():
    return render_template_string(DASHBOARD, suffix=MESSAGE_SUFFIX)

@app.get("/health")
def health():
    return jsonify(status="ok", service="shared-notification-service")

@app.get("/api/v1/template")
def get_template():
    return jsonify(template_version="v1", message_suffix=MESSAGE_SUFFIX)

@app.post("/api/v1/notifications")
def create_notification():
    data = request.get_json(silent=True) or {}
    app_name = str(data.get("app_name", "")).strip()
    recipient = str(data.get("recipient", "")).strip()
    message = str(data.get("message", "")).strip()
    if not app_name or not recipient or not message:
        return jsonify(error="app_name, recipient, and message are required"), 400
    # Use the current central template in every request.
    full_message = f"Hello {recipient}!\n\n{message}\n\n{MESSAGE_SUFFIX}"
    record = {
        "id": len(notifications) + 1,
        "app_name": app_name,
        "recipient": recipient,
        "message": full_message,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    notifications.append(record)
    return jsonify(record), 201

@app.get("/api/v1/notifications")
def list_notifications():
    return jsonify(notifications=notifications)

if __name__ == "__main__":
    print("Shared service available at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
