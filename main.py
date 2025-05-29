from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    token = None
    error = None

    if request.method == "POST":
        try:
            appstate_json = request.form.get("appstate")
            cookies = {}
            for item in json.loads(appstate_json):
                cookies[item['key']] = item['value']

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }

            url = "https://business.facebook.com/business_locations"
            response = requests.get(url, cookies=cookies, headers=headers)

            token_start = response.text.find("EAA")
            if token_start != -1:
                token = response.text[token_start:token_start + 200].split('"')[0]
            else:
                error = "Access token not found. The session might be expired or invalid."
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("index.html", token=token, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
