from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random as rd

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

    exitNum = rd.randint(0,100)
    if event.message.text == '今天的幸運數字':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=exitNum))

    if event.message.text == '野':
        if exitNum <= 60 and exitNum >= 50:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='斷'))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='格'))
    elif event.message.text == '炸':
        if exitNum <= 70 and exitNum >= 50:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='斷'))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='彈'))
    elif event.message.text == '我':
        if exitNum <= 70 and exitNum >= 50:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='斷'))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='的'))
    elif event.message.text == '最':
        if exitNum <= 70 and exitNum >= 50:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='斷'))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='愛'))
    
    
    if event.message.text == '田':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='勝'))
    elif event.message.text == '傑':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='是'))
    elif event.message.text == '口':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='交'))
    elif event.message.text == '惡':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='徒'))
    
    if event.message.text == '南':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='一'))
    elif event.message.text == '中':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='蜜'))

    if event.message.text == '當天是空的':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='地是乾的'))
    elif event.message.text == '我要為你':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='倒進狂熱'))
    elif event.message.text == '讓你瘋狂':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='讓你渴'))
    elif event.message.text == '讓全世界知道':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='你是我的'))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
