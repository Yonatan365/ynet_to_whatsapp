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
    print(data)

    title = data.get("title")
    datetime = data.get("pub_date", "")

    # convert datetime in the format: "Mon, 16 Jun 2025 22:11:51 +0300" to only local time
    if datetime:
        from datetime import datetime as dt
        from pytz import timezone

        local_tz = timezone("Asia/Jerusalem")
        naive_datetime = dt.strptime(datetime, "%a, %d %b %Y %H:%M:%S %z")
        local_datetime = naive_datetime.astimezone(local_tz)
        pub_time = local_datetime.strftime("%H:%M")
    else:
        datetime = "Unknown time"

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

