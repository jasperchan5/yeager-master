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
from crawler import nHentaiSearcher, imageSearcher, tagSearcher, covid19
from ticTacToe import TicTacToe

solitaireList = []
TicTacToeMode = False
TicTacToeStarted = False
playerInfo = ""
botInfo = ""
infos = []
nowCourt = ""

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

    global TicTacToeMode
    message = event.message.text

    if TicTacToeMode == False:

        if message == '指令':
            orders = '很高興認識你，我是接龍大師。\n\n【 功能列表 】\n\n─〔接龍〕─\n野格炸彈\n星爆\n田勝傑\n南一中蜜蜂\n我難過\n\n輸入「接龍進度」以查看進行中的接龍\n\n─〔井字遊戲〕─\n請輸入「井字遊戲」切換\n\n─〔推本子〕─\n隨機推本：請輸入「神之語言」\n本號查詢：請輸入「神之語言 <任意數字>」\n標籤查詢：請輸入「找本子 <tag1> <tag2>...」\n\n─〔推圖〕─\nR-18：請輸入「可以色色」（開發中）\n正常向：請輸入「不可以色色」（開發中）\n\n─〔每日疫情資訊〕─\n請輸入「疫情報告」\n\n更多功能敬請期待...'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=orders))

        elif message == '井字遊戲':
            TicTacToeMode = True
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Switch！！！\n\n【井字遊戲模式】\n\n─〔規則說明〕─\n首先輸入英文大寫O或X來選擇自己的符號\n接著就輸入<座標一 座標二>來決定劃記地點\n棋盤為3x3，向下為X座標，向右為Y座標\n輸入「別玩了」終止遊戲"))
        
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
            if message == '不可以色色':
                imgBot = imageSearcher(message)
                imgLink = imgBot.getImage()
            else:
                imgLink = 'https://imgur.com/mj4CCdA.png'
            try:
                line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                                                                original_content_url = imgLink,
                                                                preview_image_url = imgLink))
            except:
                line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                                                                original_content_url = 'https://imgur.com/mj4CCdA.png',
                                                                preview_image_url = 'https://imgur.com/mj4CCdA.png'))
        
        elif message == '疫情報告':
            covidBot = covid19()
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=covidBot.getDailyInfo()))
        
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
                replyArr.append(TextSendMessage(text="秒"))
                replyArr.append(ImageSendMessage(
                                                original_content_url = 'https://imgur.com/2CWEKvS.png',
                                                preview_image_url = 'https://imgur.com/2CWEKvS.png'))
                line_bot_api.reply_message(event.reply_token, replyArr)
            
            elif len(solitaireList) >= 0:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=answer))

    ### 井字遊戲 ###
    else:
        global TicTacToeStarted, playerInfo, botInfo, infos, nowCourt
        
        if message == "別玩了":
            TicTacToeStarted = False
            TicTacToeMode = False
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="雖然是遊戲，但可不是鬧著玩的！"))
        
        else:
            if TicTacToeStarted  == True:
                returnCourt = "" # string格式的棋盤
                message = message.split(" ")
                try:
                    game = TicTacToe(playerInfo,TicTacToeStarted,nowCourt)
                    game.loadInfo(infos,TicTacToeStarted)
                except:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="遊戲初始化失敗"))
                
                try:    
                    game.displayPlayer(message[0],message[1])
                except:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="玩家放置失敗"))
                
                returnCourt = game.recordCourt()
                
                if game.endGame() == True:
                    returnCourt += "\n\n遊戲結束，玩家勝。"
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=returnCourt))
                
                try:
                    game.displayBot()
                except:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="機器人放置失敗"))
                
                returnCourt = game.recordCourt()
                
                if game.endGame() == True:
                    returnCourt += "\n\n遊戲結束，機器人勝。"
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=returnCourt))
                
                nowCourt = game.recordCourt()          
                
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=returnCourt))
            
            else:   
                if message == "O" or message == "X":
                    infos = []
                    game = TicTacToe(message,TicTacToeStarted,nowCourt)
                    game.loadInfo(infos,TicTacToeStarted)
                    nowCourt = game.recordCourt()
                    playerInfo = infos[0]
                    botInfo = infos[1]
                    TicTacToeStarted = True
                    temp = "玩家為："
                    temp += playerInfo
                    temp += "\n設定完畢"
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=temp))
                    

                
            
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
