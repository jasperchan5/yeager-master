# coding:utf-8
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
from crawler import nHentaiSearcher, pixivSearcher, tagSearcher, covid19

solitaireList = []

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

    message = event.message.text
    if message == '指令':
        orders = '很高興認識你，我是接龍大師。\n\n【 功能列表 】\n\n─〔接龍〕─\n野格炸彈\n星爆\n田勝傑\n南一中蜜蜂\n我難過\n\n─〔推本子〕─\n隨機推本：請輸入「神之語言」\n本號查詢：請輸入「神之語言 <任意數字>」\n標籤查詢：請輸入「找本子 <tag1> <tag2>...」\n\n─〔推圖〕─\nR-18：請輸入「可以色色」（開發中）\n正常向：請輸入「不可以色色」（開發中）\n\n─〔每日疫情資訊〕─\n請輸入「疫情報告」\n\n更多功能敬請期待...'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=orders))
    elif message == '神之語言':
        randNum = rd.randint(0,400000)
        hentaiSearch = nHentaiSearcher(str(randNum))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hentaiSearch.searchTitle()))
    elif '神之語言 ' in message:
        doujinNum = message.split(" ")[1]
        hentaiSearch = nHentaiSearcher(doujinNum)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hentaiSearch.searchTitle()))
    elif '找本子 ' in message:
        temp = message.split(" ")
        tag = ""
        tagCnt = 0
        for i in temp:
            if tagCnt != 0:
                tag += temp[tagCnt]
                if tagCnt < len(temp)-1:
                    tag += '+'
                    tagCnt += 1
            else:
                tagCnt += 1
        doujinSearch = tagSearcher(tag)
        try:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=doujinSearch.searchDoujin()))
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="哭啊，找本失敗！"))
    elif message == '不可以色色' or message == '可以色色':
        pixivBot = pixivSearcher(message)
        try:
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                                                            original_content_url = pixivBot.getImage(),
                                                            preview_image_url = pixivBot.getImage()))
        except:
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                                                            original_content_url = 'https://imgur.com/2CWEKvS.png',
                                                            preview_image_url = 'https://imgur.com/2CWEKvS.png'))
    elif message == '疫情報告':
        covidBot = covid19()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=covidBot.getDailyInfo()))
    elif message == '星爆':

        line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                                                            original_content_url = 'https://imgur.com/2CWEKvS.png',
                                                            preview_image_url = 'https://imgur.com/2CWEKvS.png'))
    elif message == '接龍進度':
        if len(solitaireList) == 0:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無接龍進行中"))
        else:
            cnt = 0
            tempStr = ""
            for i in solitaireList:
                tempStr += solitaireList[cnt]
                cnt += 1
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=tempStr))
    else:
        soliModel = Solitaire(message,solitaireList)
        answer = soliModel.processer()
        if len(solitaireList) != 0 and solitaireList[len(solitaireList) - 1] == '秒':
            solitaireList.clear()
            replyArr = []
            replyArr.append(textSendMessage(text="秒"))
            replyArr.append(ImageSendMessage(
                                            original_content_url = 'https://imgur.com/2CWEKvS.png',
                                            preview_image_url = 'https://imgur.com/2CWEKvS.png'))
            line_bot_api.reply_message(event.reply_token, replyArr)
        elif len(solitaireList) >= 0:
            line_bot_api.reply_message(event.reply_token, textSendMessage(text=answer))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
