from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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
def yeager(event):
    if event.message.text == '野':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='格'))
    elif event.message.text == '炸':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='彈'))
    elif event.message.text == '我':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='的'))
    elif event.message.text == '最':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='愛'))

@handler.add(MessageEvent, message=TextMessage)
def jayTien(event):
    if event.message.text == '田':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='勝'))
    elif event.message.text == '傑':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='是'))
    elif event.message.text == '口':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='交'))
    elif event.message.text == '惡':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='徒'))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
