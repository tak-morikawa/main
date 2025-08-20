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

#�񓚕���ݒ肷��}�b�v
answers = {}
#1�����͂��ꂽ�ꍇ�̉񓚂��`
answers["1"] = ("desknet's�Ƀ��O�C�����A�ȉ��̎菇�Ő\�����Ă�������\n"
"1. ���T�C�h���j���[�̃��[�N�t���[���N���b�N���Ă�\n"
"2. �u�\���̍쐬�v �{�^�����N���b�N\n"
"3. �\���� �u�I���v �{�^�����N���b�N��A�u�ʋΒ����\�����v��I��\n"
"4. �\�����@���̓t�H�[���ɋL�����Đ\��")

#2�����͂��ꂽ�ꍇ�̉񓚂��`
answers["2"] = ("desknet's�Ƀ��O�C�����A�ȉ��̎菇�Ő\�����Ă�������\n"
"1. ���T�C�h���j���[�̃��[�N�t���[���N���b�N\n"
"2. �u�\���̍쐬�v �{�^�����N���b�N\n"
"3. �\���� �u�I���v �{�^�����N���b�N��A�u�T��v��I��\n"
"4. �\�����@���̓t�H�[���ɋL�����Đ\��\n"
"�@���\�������́u�T��+�i�Ј��ԍ��j+yyyymmdd(�T���߂̓��t)�v\n"
"�@����o���؁F���T�Ηj��")

#3�����͂��ꂽ�ꍇ�̉񓚂��`
answers["3"] = ("ManageOZO3�Ƀ��O�C�����A�ȉ��̎菇�Ő\�����Ă��������B\n"
"1.�㕔���j���[�̃��[�N�t���[���N���b�N\n"
"2.�u�V�K�쐬�v���N���b�N\n"
"3.�Y������\�����܂��͐��Z���N���b�N\n"
"4.���̓t�H�[���ɋL�����Đ\��\n"
"�@���o��Z�A�ڑҌ��۔�Z�A�o�����Z�͎��O�Ɋe�\�����K�v\n"
"�@��ManageOZO3�̃}�j���A���Fdesknet's > �����Ǘ� > �K���W > OZO3�ΑӁE�H���E�o��j�}�j���A��")

#4�����͂��ꂽ�ꍇ�̉񓚕����`
answers["4"] = "�����l���O���[�v�@�J���܂œd�b�A���[�����ł��˗����������B"

#5�����͂��ꂽ�ꍇ�̉񓚕����`
answers["6"] = ("�ȉ��̎菇�Ő\�����Ă��������B\n"
"1.desknet's > �ݔ��\��ɂāAZoom�̃X�P�W���[������\n"
"2.Zoom�Ǘ��ҁiCC:�����l���O���[�v�@�J���j���ĂɕK�v�������L�ڂ��ă��[���ɂĈ˗�\n"
"�@ Zoom�Ǘ��ҁFcss_zoom@chuoss.co.jp\n"
" �@�K�v�����F�����A�ړI�A�Q����\n"
"�\�񂪊�����A���O�C���������A���������܂��B")

#6�����͂��ꂽ�ꍇ�̉񓚕����`
answers["5"] = ("desknet's�AManageOZO3�ASYNCNEL�ɂăp�X���[�h���K���񐔈ȏ�ԈႦ��ƃ��b�N��������܂��B\n"
"���b�N�����͑����l���O���[�v�܂ł��A�����������B")

#7�����͂��ꂽ�ꍇ�̉񓚕����`
answers["7"] = ("�ȉ��̏��ނ��o���肢�������܂��B\n"
"��desknet's > ���[�N�t���[�ɂĒ�o\n"
"�E�ʋΒ����\����\n"
"�E�Ј����끦�ʋΒ����\�������[�N�t���[�ɓY�t\n"
"�������l���O���[�v���ă��[����o\n"
"�E���^�����҂̕}�{�T�����i�ٓ��j�\����\n"
"\n"
"�ʋ��蓖����������ꍇ�͎��̏��ނ���o�K�v\n"
"�����[���ŏ㒷��ʂ��đ����l���O���[�v�֒�o\n"
"�E�蓖�ٓ���\n"
"�E�ʋ��蓖�\�����R��\n"
"�E�Z���[�i���{�j�@�����ю傪�\�L���ꂽ���̂��蓖�ٓ��͂ɓY�t���Ē�o\n"
"�@���{�Вn�E�}�C�i���o�[�̋L�ڂ͕s�v\n"
"�@ �����[���Œ�o�̏ꍇ�́A�ʂ��ŉ�")

#��L�ȊO�̔ԍ������͂��ꂽ�ꍇ�̉񓚕����`
anserelse = ("�����l�ł��B�ȉ��̖₢���킹�ɂ��Ă��������܂��B�Y������ԍ����L�����Ă��������B\n"
"1.�ʋΒ����X\n"
"3.�o��Z�葱��\n"
"4.���h�ǉ�\n"
"5.Zoom�\��\n"
"6.���b�N����\n"
"7.�����z����̎葱��\n")

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
    #���O���o��
    app.logger.info("���[�U�[���͒l: " + event.message.text)

    #���[�U���͒l����O��̉��s���폜
    input_message = event.message.text.strip()

    #�񓚕����쐬
    reply_message = create_answer(input_message=input_message)

    #�񓚕���ԐM
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))
 
def create_answer(input_message):
    #���͒l�ɍ��킹���񓚕���ҏW
    if input_message in answers:
        return answers[input_message]
    else:
        #���͑ΏۊO�͔ԍ���I�������镶����
        return anserelse

if __name__ == "__main__":
    app.run()