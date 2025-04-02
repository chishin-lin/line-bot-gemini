import os
import google.generativeai as genai
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

# 設定 Google Gemini API
GEMINI_API_KEY = "AIzaSyC0Vw3wBC9qgROahGd3tqeF5wTjuvgjIv0"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# 設定 LINE API
LINE_ACCESS_TOKEN = "8oe585e7mBCatmL4TXwEdZ7V9IlXqK8Nw97ERw8IMbmJry/e/zlL8iKAolAV4xb2lRJH3hMMu+WJf6XxI9MqOYmgtS2OFXNyMrKDCRUsEWkW95pQNmx9+lxA7OH4eCzVlgYFcf7Dxk+SCOcTAgMVNAdB04t89/1O/w1cDnyilFU="
LINE_SECRET = "7114cd13b34f8c5334f5dd24907742c3"

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_SECRET)

@app.route("/")
def home():
    return "LINE Bot is running!><"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 使用 Google Gemini 生成回覆
    response = model.generate_content([user_message])
    reply_text = response.text if response.text else "抱歉，我無法回應。"

    # 發送回覆
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
