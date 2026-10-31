import requests
from flask import Flask, render_template, request

app = Flask(__name__)
SERVICE_URL = "http://127.0.0.1:5000"

@app.get("/")
def home():
    try:
        template = requests.get(f"{SERVICE_URL}/api/v1/template", timeout=3).json()
        suffix = template["message_suffix"]
        service_status = "Connected"
    except requests.RequestException:
        suffix = "Service unavailable"
        service_status = "Not connected — start shared_service/app.py first"
    return render_template("index.html", suffix=suffix, service_status=service_status, result=None, error=None)

@app.post("/notify")
def notify():
    recipient = request.form.get("recipient", "").strip()
    update_type = request.form.get("update_type", "").strip()
    if not recipient or not update_type:
        return render_template("index.html", suffix="", service_status="Connected", result=None, error="Please enter both student name and update details.")
    try:
        response = requests.post(f"{SERVICE_URL}/api/v1/notifications", json={
            "app_name": "Student Management System",
            "recipient": recipient,
            "message": f"Your student record update: {update_type}."
        }, timeout=5)
        if response.ok:
            result = response.json()["message"]
            error = None
        else:
            result, error = None, response.json().get("error", "Request failed")
    except requests.RequestException:
        result, error = None, "Cannot connect to shared service. Start it on port 5000."
    return render_template("index.html", suffix="", service_status="Connected", result=result, error=error)

if __name__ == "__main__":
    print("Student client available at http://127.0.0.1:5002")
    app.run(host="127.0.0.1", port=5002, debug=False)
