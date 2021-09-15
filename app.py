# Import libraries
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random as rd

from solitaire import Solitaire

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('7bUWhyl8qAlpY/WxuwtqnDUSfXc1qIPHH/3U5MqfxcG5dT0vtAu1GWGD9QdW8zJ4ek/GpCVucdCRzxFvsuYK0nHSjG/aBNiLN6AVZm4+NeOyslqK4qrk9lLULHu7/o/xNkcA/EGYXrepyac8W39uJQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('de24db69327f19f382574de4fba4d553')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    ### 接龍區 ###

    soliModel = Solitaire(event.message.text)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=soliModel.processer()))

    # 輸入本號找tag

    randNum = rd.randint(0,400000)
    if event.message.text == '抽數字':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=randNum))
        

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
