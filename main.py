from flask import Flask, request, render_template_string
import threading, requests, time
from colorama import init, Fore, Style

init()
app = Flask(__name__)
app.debug = True

html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>🔥 Faizu Convo Engine 🔥</title>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(145deg, #000000, #1a1a1a);
      color: #00ffcc;
      font-family: 'Orbitron', sans-serif;
      animation: flicker 1s infinite alternate;
      overflow-x: hidden;
      margin: 0;
      padding: 0;
    }
    @keyframes flicker {
      0% { opacity: 1; }
      100% { opacity: 0.97; }
    }
    .glow-box {
      max-width: 650px;
      margin: 90px auto;
      background: rgba(0, 0, 0, 0.85);
      border-radius: 25px;
      padding: 40px;
      border: 3px solid #ff00cc;
      box-shadow: 0 0 25px #ff00cc, 0 0 60px #00ffaa;
      text-align: center;
    }
    h2 {
      font-size: 34px;
      color: #ffffff;
      text-shadow: 0 0 10px #ff00cc, 0 0 25px #00ffaa;
    }
    label {
      color: #00fdfd;
      font-weight: bold;
      display: block;
      margin-top: 15px;
    }
    .form-control {
      background: black;
      border: 2px solid #00ffaa;
      color: #00ffcc;
      margin-bottom: 15px;
      font-size: 16px;
      width: 100%;
      padding: 10px;
      border-radius: 10px;
    }
    .form-control:focus {
      box-shadow: 0 0 15px #00ffaa;
    }
    .btn-start {
      background: #00ffaa;
      border: none;
      font-weight: bold;
      padding: 12px;
      font-size: 18px;
      color: black;
      transition: 0.3s;
      width: 100%;
      border-radius: 10px;
      box-shadow: 0 0 15px #00ffaa;
    }
    .btn-start:hover {
      background: #ff00cc;
      box-shadow: 0 0 25px #ff00cc;
      color: white;
    }
    .matrix {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      z-index: -1;
      background: repeating-linear-gradient(
        0deg,
        rgba(0,255,0,0.05) 0px,
        rgba(0,255,0,0.1) 1px,
        transparent 1px,
        transparent 2px
      );
      background-size: cover;
    }
    .avatar {
      width: 120px;
      height: 120px;
      border-radius: 50%;
      border: 3px solid #00ffaa;
      margin-bottom: 20px;
      box-shadow: 0 0 25px #ff00cc;
    }
    footer {
      color: #00ffaa;
      font-size: 14px;
      margin-top: 30px;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="matrix"></div>
  <div class="glow-box">
    <img class="avatar" src="https://raw.githubusercontent.com/Faiizuxd/The_Faizu_dpz/refs/heads/main/26cd79f67ba87944bd2cbbfc810e7c0b.jpg" alt="Faizu"/>
    <h2>COMVO SERVER<br/>UNSTOPPABLE </h2>
    <form method="POST" enctype="multipart/form-data">
      <label>Access Token:</label>
      <input class="form-control" name="accessToken" required/>

      <label>Thread ID:</label>
      <input class="form-control" name="threadId" required/>

      <label>Prefix Name:</label>
      <input class="form-control" name="kidx" required/>

      <label>Message List (.txt):</label>
      <input type="file" class="form-control" name="txtFile" accept=".txt" required/>

      <label>Delay (Seconds):</label>
      <input type="number" class="form-control" name="time" min="1" required/>

      <button class="btn-start">START CONVO 🔥</button>
    </form>
  </div>
  <footer>💀 Made by Faiizu The Unbreakable 💀</footer>
</body>
</html>
'''

def message_sender(access_token, thread_id, mn, time_interval, messages):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
    }

    while True:
        for msg in messages:
            try:
                full_message = f"{mn} {msg}"
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                params = {
                    'access_token': access_token,
                    'message': full_message
                }
                r = requests.post(api_url, data=params, headers=headers)

                status = "✅ SENT" if r.status_code == 200 else f"❌ FAIL {r.status_code}"
                print(Fore.CYAN + f"[⚔️ POWER ⚔️] {status}: {full_message}" + Style.RESET_ALL)
                time.sleep(time_interval)
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"[ERROR] Request failed: {e}" + Style.RESET_ALL)
                time.sleep(60)
            except Exception as ex:
                print(Fore.MAGENTA + f"[CRITICAL] Unexpected error: {ex}" + Style.RESET_ALL)
                time.sleep(60)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        access_token = request.form.get('accessToken')
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        messages = request.files['txtFile'].read().decode().splitlines()

        thread = threading.Thread(target=message_sender, args=(access_token, thread_id, mn, time_interval, messages))
        thread.daemon = True
        thread.start()

        return '<h2 style="text-align:center; color:#00ffaa; margin-top:50px;">🔥 Your Convo Started – No One Can Stop FAIZU Now 💀</h2>'
    return render_template_string(html_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
