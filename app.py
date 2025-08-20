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

#回答文を設定するマップ
answers = {}
#1が入力された場合の回答を定義
answers["1"] = ("desknet'sにログインし、以下の手順で申請してください\n"
"1. 左サイドメニューのワークフローをクリックしてね\n"
"2. 「申請の作成」 ボタンをクリック\n"
"3. 申請書 「選択」 ボタンをクリック後、「通勤定期代申請書」を選択\n"
"4. 申請書　入力フォームに記入して申請")

#2が入力された場合の回答を定義
answers["2"] = ("desknet'sにログインし、以下の手順で申請してください\n"
"1. 左サイドメニューのワークフローをクリック\n"
"2. 「申請の作成」 ボタンをクリック\n"
"3. 申請書 「選択」 ボタンをクリック後、「週報」を選択\n"
"4. 申請書　入力フォームに記入して申請\n"
"　※申請書名は「週報+（社員番号）+yyyymmdd(週初めの日付)」\n"
"　※提出締切：翌週火曜日")

#3が入力された場合の回答を定義
answers["3"] = ("ManageOZO3にログインし、以下の手順で申請してください。\n"
"1.上部メニューのワークフローをクリック\n"
"2.「新規作成」をクリック\n"
"3.該当する申請書または精算をクリック\n"
"4.入力フォームに記入して申請\n"
"　※経費精算、接待交際費精算、出張精算は事前に各申請が必要\n"
"　※ManageOZO3のマニュアル：desknet's > 文書管理 > 規程集 > OZO3勤怠・工数・経費）マニュアル")

#4が入力された場合の回答文を定義
answers["4"] = "総務人事グループ　谷口まで電話、メール等でご依頼ください。"

#5が入力された場合の回答文を定義
answers["6"] = ("以下の手順で申請してください。\n"
"1.desknet's > 設備予約にて、Zoomのスケジュール入力\n"
"2.Zoom管理者（CC:総務人事グループ　谷口）宛てに必要事項を記載してメールにて依頼\n"
"　 Zoom管理者：css_zoom@chuoss.co.jp\n"
" 　必要事項：日時、目的、参加者\n"
"予約が完了後、ログイン情報をご連絡いたします。")

#6が入力された場合の回答文を定義
answers["5"] = ("desknet's、ManageOZO3、SYNCNELにてパスワードを規程回数以上間違えるとロックがかかります。\n"
"ロック解除は総務人事グループまでご連絡ください。")

#7が入力された場合の回答文を定義
answers["7"] = ("以下の書類を提出お願いいたします。\n"
"■desknet's > ワークフローにて提出\n"
"・通勤定期代申請書\n"
"・社員名簿※通勤定期代申請書ワークフローに添付\n"
"■総務人事グループ宛てメール提出\n"
"・給与所得者の扶養控除等（異動）申告書\n"
"\n"
"別居手当が発生する場合は次の書類も提出必要\n"
"■メールで上長を通じて総務人事グループへ提出\n"
"・手当異動届\n"
"・別居手当申請理由書\n"
"・住民票（原本）　※世帯主が表記されたものを手当異動届に添付して提出\n"
"　※本籍地・マイナンバーの記載は不要\n"
"　 ※メールで提出の場合は、写しで可")

#上記以外の番号が入力された場合の回答文を定義
anserelse = ("お疲れ様です。以下の問い合わせについてお答えします。該当する番号を記入してください。\n"
"1.通勤定期代更\n"
"3.経費精算手続き\n"
"4.名刺追加\n"
"5.Zoom予約\n"
"6.ロック解除\n"
"7.引っ越し後の手続き\n")

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

#初期起動
if __name__ == "__main__":
    app.run()