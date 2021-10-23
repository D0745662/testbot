# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com
Line Bot聊天機器人
第四章 選單功能
快速回復QuickReply
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
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('F49hdXd2BxZ8DzznS+0I7GUhQYGI6OT97CvHWRihzS/1z/pcu9tTFB31s08ZqahgJy6WsZuSXMZH7PQGVEI8agVH9Z7LSYE0gDg5BQ0RdVVOPbfr5TQgtXVfI48/kqDCHCOxbaRJfKwrCUG6bVgjJQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('bca5248a9c30651b6730179bdd37515b')

line_bot_api.push_message('U6ec9a01882a0c90ceaa97f7c7ae90ab8', TextSendMessage(text='你可以開始了'))

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
    if re.match('告訴我秘密',message):
        flex_message = TextSendMessage(text='以下有雷，請小心',
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="別按我", text="你按屁喔！爆炸了拉！！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                   QuickReplyButton(action=MessageAction(label="按我", text="按！"))
                               ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)