import logging
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

line_bot_api = LineBotApi('ro4RkwujGQyLO3RlwbnPZaazK28meiyLjn0irPIz6JqEDKxSZtcAhT2vsbFi82Q+XM/yCzNl4wuqJvMqb3yty29gR1pKgcdEzmuz2WGWaindPipstV4iLGjZa/273kSuRKSVOyXjGIIcPFhwvzxHcgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('413f2f5dd5a6a38d4c2820264ed7d509')

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
    #ログを出力
    app.logger.info("ユーザー入力値: " + event.message.text)

    #ユーザ入力値から前後の改行を削除
    input_message = event.message.text.strip()

    #回答文を作成
    reply_message = create_answer(input_message=input_message)

    #回答文を返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))
 
def create_answer(input_message):
    #入力値に合わせた回答文を編集
    if input_message in answers:
        return answers[input_message]
    else:
        #入力対象外は番号を選択させる文を回答
        return anserelse

if __name__ == "__main__":
    app.run()