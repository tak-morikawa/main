import logging
from flask import Flask, request, abort
import openai
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

line_bot_api = LineBotApi('ro4RkwujGQyLO3RlwbnPZaazK28meiyLjn0irPIz6JqEDKxSZtcAhT2vsbFi82Q+XM/yCzNl4wuqJvMqb3yty29gR1pKgcdEzmuz2WGWaindPipstV4iLGjZa/273kSuRKSVOyXjGIIcPFhwvzxHcgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('413f2f5dd5a6a38d4c2820264ed7d509')

# OpenAI API Key
openai.api_key = os.environ["OPENAI_API_KEY"]
@app.route("/")
def test():
    return "OK TEST"

@app.route("/answer")
def test_answer():
    input_message = request.args["text"].strip()
    reply_message = create_answer(input_message=input_message).replace("\n", "<br>")
    return reply_message

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    ai_reply = ask_openai(user_text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ai_reply)
    )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 画像のバイナリを取得
    try:
        message_content = line_bot_api.get_message_content(event.message.id)
    except Exception as e:
        print(f"その他のエラー: {e}")
    
    image_data = b""
    for chunk in message_content.iter_content():
        image_data += chunk
    
    encoded_image = base64.b64encode(image_data).decode("utf-8").replace("\n", "")

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Vision対応モデル
        messages=[
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": "この画像の内容を説明してください"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ]  
    )

def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 必要に応じて変更
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]

#初期起動
if __name__ == "__main__":
    app.run()