from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
MY_WHATSAPP_NUMBER = os.environ["MY_WHATSAPP_NUMBER"]

TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

@app.route('/send', methods=['POST'])
def send_whatsapp():
    data = request.json

    title = data.get("title", "")
    pub_date_raw = data.get("pub_date", "")

    pub_time = "Unknown time"

    if pub_date_raw:
        try:
            # Regex to extract HH:MM from string like "Mon, 16 Jun 2025 22:11:51 +0300"
            match = re.search(r"\b(\d{2}):(\d{2}):\d{2}\b", pub_date_raw)
            if match:
                hour = match.group(1)
                minute = match.group(2)
                pub_time = f"{hour}:{minute}"
            else:
                pub_time = "Unknown time"
        except Exception as e:
            print("Regex parse error:", e)
            pub_time = "Bad date format"

    message_body = f"{pub_time}: {title}"

    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"

    payload = {
        'From': TWILIO_WHATSAPP_NUMBER,
        'To': f"whatsapp:{MY_WHATSAPP_NUMBER}",
        'Body': message_body
    }

    resp = requests.post(url, data=payload, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))

    if resp.status_code == 201:
        return jsonify({"status": "sent"}), 200
    else:
        return jsonify({"error": resp.text}), 400
    
@app.route('/')
def hello():
    return "Webhook running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

