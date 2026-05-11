```python
from flask import Flask, request
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText

app = Flask(__name__)

# =========================
# EMAIL CONFIG
# =========================

EMAIL_ADDRESS = "kalpvininsurance@gmail.com"
EMAIL_PASSWORD = "onux qafp agzz sflk"

# =========================
# TELEGRAM CONFIG
# =========================

BOT_TOKEN = "8657217148:AAHicOlpVqUqmu4olHwGnnFvhkQqNvxGPKs"

CHAT_ID = "1190014186"

# =========================
# HOME ROUTE
# =========================

@app.route("/")
def home():
    return "TradingView Alert Server Running 🚀"

# =========================
# WEBHOOK ROUTE
# =========================

@app.route('/webhook', methods=['POST'])
def webhook():

    try:

        data = request.json

        signal = data.get("signal")
        symbol = data.get("symbol")
        price  = data.get("price")

        time_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # =========================
        # MESSAGE BODY
        # =========================

        body = f"""
📈 TradingView Alert

Signal : {signal}
Symbol : {symbol}
Price  : {price}
Time   : {time_now}
"""

        # =========================
        # EMAIL ALERT
        # =========================

        msg = MIMEText(body)

        msg["Subject"] = f"{signal} Alert - {symbol}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

        # =========================
        # TELEGRAM ALERT
        # =========================

        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": body
        }

        requests.post(telegram_url, json=payload)

        return {
            "status": "success",
            "message": "Alert Sent Successfully"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```
