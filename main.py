import os
from flask import Flask, request
import requests
import threading
import time

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
PHONE_ID = os.environ.get("PHONE_ID")
URL = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"

@app.route('/')
def home():
    return "Bot is alive"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'messages' in data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}):
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        from_number = msg['from']
        text = msg['text']['body'].lower()

        if text == 'hi':
            send_message(from_number, "Yo bro 👋 WhatsApp bot is live")
    return "ok", 200

def send_message(to, text):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(URL, json=payload, headers=headers)

def keep_alive():
    while True:
        print("Bot started...")
        time.sleep(3)

if __name__ == '__main__':
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
