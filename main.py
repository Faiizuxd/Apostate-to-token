from flask import Flask, request, render_template_string
import requests
import re
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>FAIZU | AppState to Token Converter</title>
<style>
  body {
    background: linear-gradient(135deg,#8e2de2,#4a00e0,#ff416c,#ff4b2b,#00c6ff,#0072ff);
    color: #fff;
    font-family: 'Poppins', sans-serif;
    padding: 30px;
    text-align: center;
  }
  h1 { margin-bottom: 20px; }
  textarea {
    width: 90%;
    height: 250px;
    border-radius: 15px;
    border: 2px solid #ff4b2b;
    background: #111;
    color: #fff;
    font-family: monospace;
    font-size: 0.9rem;
    padding: 15px;
    resize: vertical;
  }
  button {
    margin-top: 20px;
    padding: 15px 40px;
    font-size: 1.25rem;
    font-weight: 700;
    color: #111;
    background: linear-gradient(45deg,#ff4b2b,#ff416c,#8e2de2,#4a00e0);
    border: none;
    border-radius: 50px;
    cursor: pointer;
  }
  .result {
    margin-top: 30px;
    padding: 20px;
    border-radius: 20px;
    background: rgba(0,0,0,0.85);
    font-family: monospace;
    font-size: 1.1rem;
    color: #00ffaa;
    user-select: all;
    word-wrap: break-word;
  }
  .error {
    margin-top: 30px;
    padding: 20px;
    border-radius: 20px;
    background: rgba(200,0,0,0.85);
    font-weight: 700;
    font-size: 1.1rem;
    color: #ff5555;
  }
</style>
</head>
<body>
  <h1>🔥 FAIZU | AppState to Access Token 🔥</h1>
  <form method="POST" action="/">
    <textarea name="appstate_json" placeholder="Paste your Facebook AppState JSON array here..." required>{{ appstate_json|default('') }}</textarea><br>
    <button type="submit">Convert to Access Token</button>
  </form>
  {% if token %}
    <div class="result" title="Click to select all">Access Token: {{ token }}</div>
  {% elif error %}
    <div class="error">{{ error }}</div>
  {% endif %}
</body>
</html>
'''

def extract_token_from_appstate(appstate):
    try:
        cookies = {cookie['key']: cookie['value'] for cookie in appstate}

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36',
            'Accept': 'application/json',
        }

        url = 'https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed'

        response = requests.get(url, cookies=cookies, headers=headers, timeout=10)
        if response.status_code != 200:
            return None, f"Failed to fetch Facebook data, status code: {response.status_code}"

        # Find token pattern starting with EAA and ending before a quote or backslash
        match = re.search(r'"accessToken\\":\\"(EAA[\w\d]+)', response.text)
        if match:
            return match.group(1), None
        else:
            return None, "Access token not found. The session might be expired or invalid."
    except Exception as e:
        return None, f"Error processing appstate: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    error = None
    appstate_json = ''

    if request.method == 'POST':
        appstate_json = request.form.get('appstate_json', '').strip()
        if not appstate_json:
            error = "Please paste your AppState JSON."
        else:
            try:
                appstate = json.loads(appstate_json)
                if not isinstance(appstate, list):
                    error = "Invalid JSON format. AppState should be a JSON array."
                else:
                    token, error = extract_token_from_appstate(appstate)
            except json.JSONDecodeError:
                error = "Invalid JSON. Please ensure your input is correct JSON format."

    return render_template_string(html_code, token=token, error=error, appstate_json=appstate_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
