from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

EMAIL_ADDRESS = "kalpvininsurance@gmail.com"
EMAIL_PASSWORD = "onux qafp agzz sflk"

@app.route('/webhook', methods=['POST'])
def webhook():

    data = request.json

    signal = data.get("signal")
    symbol = data.get("symbol")
    price  = data.get("price")

    body = f"""
    TradingView Alert

    Signal : {signal}
    Symbol : {symbol}
    Price  : {price}
    """

    msg = MIMEText(body)

    msg["Subject"] = f"{signal} Alert - {symbol}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

    return {"status": "success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
