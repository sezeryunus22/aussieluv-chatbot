from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

WHATSAPP_API_URL = "https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages"
WHATSAPP_TOKEN = os.getenv("WHATSAPP_API_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        user_msg = data['messages'][0]['text']['body']
        user_number = data['messages'][0]['from']

        # Get ChatGPT response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful sales assistant for a jewelry brand called Aussieluv."},
                {"role": "user", "content": user_msg}
            ]
        )
        reply = response.choices[0].message.content

        # Send WhatsApp reply
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": user_number,
            "type": "text",
            "text": {"body": reply}
        }
        requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

        return "ok", 200
    except Exception as e:
        print("Error:", e)
        return "error", 400
