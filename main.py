
from flask import Flask, request, render_template_string, redirect
import json
import os
from uuid import uuid4
from flask import abort

app = Flask(__name__)

ADMIN_PASSWORD = "/admin-faizi-panel-1000000100003737"
ADMIN_IP = "37.111.145.91"
DEVICE_FILE = "devices.json"

if not os.path.exists(DEVICE_FILE):
    with open(DEVICE_FILE, "w") as f:
        json.dump({}, f)

def load_devices():
    with open(DEVICE_FILE, "r") as f:
        return json.load(f)

def save_devices(data):
    with open(DEVICE_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    device_id = "TERROR-" + str(uuid4()).split("-")[0].upper()
    return render_template_string(WELCOME_HTML, device_id=device_id)

@app.route("/submit", methods=["POST"])
def submit():
    device_id = request.form.get("device_id")
    devices = load_devices()
    if device_id not in devices:
        devices[device_id] = "pending"
        save_devices(devices)
    return redirect(f"/check/{device_id}")

@app.route("/check/<device_id>")
def check_status(device_id):
    devices = load_devices()
    status = devices.get(device_id, "not_found")
    if status == "approved":
        return render_template_string(APPROVED_HTML)
    elif status == "pending":
        return render_template_string(PENDING_HTML, device_id=device_id)
    elif status == "rejected":
        return render_template_string(REJECTED_HTML)
    else:
        return "Device ID not found."

@app.route(ADMIN_PASSWORD)
def admin_panel():
    if request.remote_addr != ADMIN_IP:
        abort(403)
    devices = load_devices()
    return render_template_string(ADMIN_HTML, devices=devices)

@app.route("/approve/<device_id>")
def approve(device_id):
    if request.remote_addr != ADMIN_IP:
        abort(403)
    devices = load_devices()
    if device_id in devices:
        devices[device_id] = "approved"
        save_devices(devices)
    return redirect(ADMIN_PASSWORD)

@app.route("/reject/<device_id>")
def reject(device_id):
    if request.remote_addr != ADMIN_IP:
        abort(403)
    devices = load_devices()
    if device_id in devices:
        devices[device_id] = "rejected"
        save_devices(devices)
    return redirect(ADMIN_PASSWORD)

@app.route("/delete/<device_id>")
def delete(device_id):
    if request.remote_addr != ADMIN_IP:
        abort(403)
    devices = load_devices()
    if device_id in devices:
        del devices[device_id]
        save_devices(devices)
    return redirect(ADMIN_PASSWORD)

WELCOME_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Welcome to The TERROR Apk</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>
    body { background: #111; color: #fff; font-family: Arial; text-align: center; padding: 20px; }
    .box { background: #222; padding: 20px; border-radius: 12px; display: inline-block; margin-top: 100px; }
    .btn { background: #ff3c00; color: white; border: none; padding: 10px 20px; font-size: 14px; border-radius: 10px; cursor: pointer; }
    .btn:hover { background: #ff5500; }
    small { font-size: 12px; color: #ccc; }
  </style>
</head>
<body>
  <div class="box">
    <h3>ðŸ‘‹ Hi Welcome to The <b>TERROR</b> Apk</h3>
    <p>This apk is made for <b>Convo Server</b>, Post & Tools</p>
    <p><b>Send your device ID to approval ðŸ‘‡</b></p>
    <form method="POST" action="/submit">
      <input type="hidden" name="device_id" value="{{ device_id }}">
      <p><b>Your Device ID:</b><br> <code>{{ device_id }}</code></p>
      <button class="btn" type="submit">ðŸ“¤ Send ID to Admin</button>
    </form>
    <p><small>Send to <a href="https://www.facebook.com/The.Unbeatble.Stark" target="_blank">Faiizu</a> or <a href="https://www.facebook.com/asadmeer.645927" target="_blank">Stuner</a></small></p>
  </div>
</body>
</html>
"""

PENDING_HTML = """
<h2>ðŸ•’ Your ID is sent to Admin for approval.</h2>
<p>Please wait while we verify your request.</p>
"""

REJECTED_HTML = """
<h2>âŒ Sorry, your request was rejected.</h2>
<p>You are not authorized to use the app.</p>
"""

APPROVED_HTML = """
<h2>âœ… Hi Mr, now you're a paid & approved user!</h2>
<p>Welcome to <b>The TERROR Apk</b> ðŸŽ‰</p>
<p>All credit goes to <b>Stuner Ã— Faiizu</b> for this Apk & hosting.</p>
<a href="https://faiizuapk.unaux.com/" target="_blank"><button class="btn">ðŸš€ Start</button></a>
"""

ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head><title>Admin Panel</title></head>
<body style="background:#000; color:#0f0; font-family:monospace;">
<h2>ðŸ‘‘ Admin Panel - TERROR Apk</h2>
<h3>Pending Requests:</h3>
<ul>
{% for id, status in devices.items() if status == 'pending' %}
  <li>{{ id }} - <a href="/approve/{{ id }}">âœ… Approve</a> | <a href="/reject/{{ id }}">âŒ Reject</a></li>
{% endfor %}
</ul>
<h3>Approved Users:</h3>
<ul>
{% for id, status in devices.items() if status == 'approved' %}
  <li>{{ id }} - <a href="/delete/{{ id }}">ðŸ—‘ï¸ Delete</a></li>
{% endfor %}
</ul>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
