from flask import Flask, request, redirect, url_for, render_template_string, jsonify
import uuid

app = Flask(__name__)

# Store device approvals
devices = {}
approved_devices = {}

# Admin Config
ADMIN_PATH = '/admin-faizi-panel-1000000100003737'
ADMIN_IP = '37.111.145.91'

FONT_AWESOME = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">'

# HTML Templates
user_template = f"""
{FONT_AWESOME}
<!DOCTYPE html>
<html>
<head>
  <title>The TERROR Apk</title>
  <style>
    body {{
      background: linear-gradient(45deg, #ff0040, #ffd000);
      font-family: Arial, sans-serif;
      color: #fff;
      text-align: center;
      padding: 30px;
    }}
    .box {{
      background: rgba(255,255,255,0.1);
      border-radius: 20px;
      padding: 20px;
      margin: 20px;
      box-shadow: 0 0 20px rgba(255,255,255,0.2);
    }}
    button {{
      background: #fff;
      border: none;
      border-radius: 8px;
      padding: 10px 20px;
      font-size: 14px;
      margin: 10px;
      cursor: pointer;
      transition: 0.3s;
    }}
    button:hover {{
      background: #ff0040;
      color: white;
    }}
    a {{
      color: #ffd000;
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <div class="box">
    <h2>👋 Hi Welcome to <b>The TERROR Apk</b></h2>
    <p>This APK is made for <b>Convo Server</b>, Posts, and Tools!</p>
    <p>👇 Send your ID for Approval 👇</p>
    <p><b>📱 Your Device ID:</b><br>{{device_id}}</p>
    <form method="post" action="/send">
      <input type="hidden" name="device_id" value="{{device_id}}">
      <button type="submit">📤 Send ID to Admin</button>
    </form>
    <br>
    <p>Send to: 
      <a href="https://www.facebook.com/The.Unbeatble.Stark" target="_blank">Faiizu</a> |
      <a href="https://www.facebook.com/asadmeer.645927" target="_blank">Stuner</a>
    </p>
  </div>
</body>
</html>
"""

approved_template = f"""
{FONT_AWESOME}
<!DOCTYPE html>
<html>
<head>
  <title>Welcome User</title>
  <style>
    body {{
      background: linear-gradient(45deg, #ff0040, #ffd000);
      font-family: Arial, sans-serif;
      text-align: center;
      color: white;
      padding: 30px;
    }}
    .box {{
      background: rgba(255,255,255,0.1);
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 20px rgba(255,255,255,0.2);
    }}
    button {{
      background: #fff;
      border: none;
      border-radius: 8px;
      padding: 10px 20px;
      font-size: 14px;
      margin-top: 20px;
      cursor: pointer;
      transition: 0.3s;
    }}
    button:hover {{
      background: #ffd000;
    }}
  </style>
</head>
<body>
  <div class="box">
    <h2>🎉 Hi Mr, Now You're a Paid & Approved User</h2>
    <p>Welcome to <b>The TERROR Apk</b></p>
    <p>Credits: <b>Stuner</b> x <b>Faiizu</b> for APK & Hosting 💖</p>
    <form action="https://faiizuapk.unaux.com/">
      <button type="submit">🚀 Start</button>
    </form>
  </div>
</body>
</html>
"""

admin_template = f"""
{FONT_AWESOME}
<!DOCTYPE html>
<html>
<head>
  <title>Admin Panel</title>
  <style>
    body {{
      background: #111;
      color: white;
      font-family: monospace;
      padding: 20px;
    }}
    .user-box {{
      background: #222;
      padding: 10px;
      margin: 10px 0;
      border-radius: 10px;
    }}
    button {{
      margin-left: 10px;
      background: #444;
      border: none;
      padding: 5px 10px;
      color: white;
      border-radius: 5px;
    }}
    button:hover {{
      background: #ff0040;
    }}
  </style>
</head>
<body>
  <h2>🔐 Admin Panel (Protected)</h2>
  <h3>Pending Device IDs</h3>
  {% for device_id in pending %}
    <div class="user-box">
      {{device_id}}
      <form method="post" action="/admin/approve" style="display:inline;">
        <input type="hidden" name="device_id" value="{{device_id}}">
        <button type="submit">✅ Approve</button>
      </form>
      <form method="post" action="/admin/reject" style="display:inline;">
        <input type="hidden" name="device_id" value="{{device_id}}">
        <button type="submit">❌ Reject</button>
      </form>
    </div>
  {% endfor %}

  <h3>Approved Users</h3>
  {% for device_id in approved %}
    <div class="user-box">
      {{device_id}}
      <form method="post" action="/admin/delete" style="display:inline;">
        <input type="hidden" name="device_id" value="{{device_id}}">
        <button type="submit">🗑️ Delete</button>
      </form>
    </div>
  {% endfor %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    device_id = str(uuid.uuid4())[:12]  # Unique per session/device
    if device_id in approved_devices:
        return render_template_string(approved_template)
    return render_template_string(user_template, device_id=device_id)

@app.route('/send', methods=['POST'])
def send_id():
    device_id = request.form.get("device_id")
    if device_id:
        devices[device_id] = "pending"
    return f"<h3 style='color:white;text-align:center;'>✅ ID sent to admin! Wait for approval.<br><a href='/'>Back</a></h3>"

@app.route(ADMIN_PATH, methods=['GET'])
def admin_panel():
    if request.remote_addr != ADMIN_IP:
        return "Access Denied"
    pending = [d for d, s in devices.items() if s == "pending"]
    approved = list(approved_devices.keys())
    return render_template_string(admin_template, pending=pending, approved=approved)

@app.route('/admin/approve', methods=['POST'])
def approve():
    device_id = request.form.get("device_id")
    if device_id:
        devices[device_id] = "approved"
        approved_devices[device_id] = True
    return redirect(ADMIN_PATH)

@app.route('/admin/reject', methods=['POST'])
def reject():
    device_id = request.form.get("device_id")
    if device_id in devices:
        del devices[device_id]
    return redirect(ADMIN_PATH)

@app.route('/admin/delete', methods=['POST'])
def delete():
    device_id = request.form.get("device_id")
    if device_id in approved_devices:
        del approved_devices[device_id]
    return redirect(ADMIN_PATH)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
