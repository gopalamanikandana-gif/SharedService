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
    order_id = request.form.get("order_id", "").strip()
    if not recipient or not order_id:
        return render_template("index.html", suffix="", service_status="Connected", result=None, error="Please enter both student name and order ID.")
    try:
        response = requests.post(f"{SERVICE_URL}/api/v1/notifications", json={
            "app_name": "Smart Campus Canteen",
            "recipient": recipient,
            "message": f"Your canteen order #{order_id} has been placed successfully."
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
    print("Canteen client available at http://127.0.0.1:5001")
    app.run(host="127.0.0.1", port=5001, debug=False)
