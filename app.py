# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com
Line Bot聊天機器人
第三章 互動回傳功能
推播push_message與回覆reply_message
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
import time
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('F49hdXd2BxZ8DzznS+0I7GUhQYGI6OT97CvHWRihzS/1z/pcu9tTFB31s08ZqahgJy6WsZuSXMZH7PQGVEI8agVH9Z7LSYE0gDg5BQ0RdVVOPbfr5TQgtXVfI48/kqDCHCOxbaRJfKwrCUG6bVgjJQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('bca5248a9c30651b6730179bdd37515b')

line_bot_api.push_message('U6ec9a01882a0c90ceaa97f7c7ae90ab8', TextSendMessage(text='你可以開始了'))
yourID = 'U6ec9a01882a0c90ceaa97f7c7ae90ab8'

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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('game',message):
        flex_message = TextSendMessage(text='以下有雷，請小心',
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="別按我", text="爆炸了！！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！"))
                               ]))     
        line_bot_api.reply_message(event.reply_token, flex_message)

        #for i in [5,4,3,2,1]:
         #   line_bot_api.push_message(yourID, TextSendMessage(text= '倒數:'+str(i)))
          #  time.sleep(1)
    else:  
        ##貼圖 
        #sticker_message = StickerSendMessage(package_id=1,sticker_id=1)
        #line_bot_api.reply_message(event.reply_token, sticker_message)
        ##位置
        #location_message  = LocationSendMessage(title = '推薦酒吧', address = '準備中',
        #                                        latitude=24.155732100748097, longitude=120.64707590363155)
        #line_bot_api.reply_message(event.reply_token, location_message)
        ##圖片
        #image_message = ImageSendMessage(
         #   original_content_url='https://memeprod.ap-south-1.linodeobjects.com/user-template/e34fbd9d0e8fbd3b135283d9131fb51c.png',
          #  preview_image_url= 'https://memeprod.ap-south-1.linodeobjects.com/user-template/e34fbd9d0e8fbd3b135283d9131fb51c.png')
        #line_bot_api.reply_message(event.reply_token, image_message)
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
        line_bot_api.reply_message(event.reply_token,TextSendMessage('test！'))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)