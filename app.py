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
        
        buttons_template_message = TemplateSendMessage(
        alt_text='這個是跳訊息的預覽',
        template=ButtonsTemplate(               ##最多4個
            thumbnail_image_url='https://i.imgur.com/GLElBwY.jpg',
            title='調酒推薦',
            text='選單功能－TemplateSendMessage',
            actions=[
                PostbackAction(
                    label='POST',
                    display_text='顯示文字',
                    data='action=檯面下'
                ),
                MessageAction(
                    label='直接傳',
                    text=event.reply_token
                ),
                URIAction(
                    label='傳url',
                    uri='https://www.twitch.tv/gunguno'
                ),
                MessageAction(
                    label='confirm template',
                    text='confirm template'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message) 
        
        ### quick reply
        '''
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
        '''
        
        ##迴圈
        '''
        for i in [5,4,3,2,1]:
            line_bot_api.push_message(yourID, TextSendMessage(text= '倒數:'+str(i)))
            time.sleep(1)
        '''
        
    elif re.match('confirm template',message):
        confirm_template_message = TemplateSendMessage(
            alt_text='問問題',
            template=ConfirmTemplate(
                text='踢掉嗎',
                actions=[
                    MessageAction(
                        label='踢掉',
                        text=event.reply_token
                    ),
                    MessageAction(
                        label='carousel template',
                        text='carousel template'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, confirm_template_message)
        
        
        
        
        
    elif re.match('carousel template',message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='圖片',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/Aax1R2U.jpg',
                        action=URIAction(
                            label='附近有什麽酒吧',
                            uri='https://www.google.com.tw/maps/search/%E9%85%92%E5%90%A7/@24.1708234,120.6552069,15z/data=!3m1!4b1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://imgur.dcard.tw/KQ3NxARh.jpg',
                        action=URIAction(
                            label='我要喝這個',
                            uri='https://www.twitch.tv/gunguno'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/0mC9Ix6.jpg',
                        action=URIAction(
                            label='我要喝這個',
                            uri='https://www.twitch.tv/gunguno'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
        
    else :  
        '''
        ##貼圖 
        sticker_message = StickerSendMessage(package_id=1,sticker_id=1)
        line_bot_api.reply_message(event.reply_token, sticker_message)
        
        
        ##位置
        location_message  = LocationSendMessage(title = '推薦酒吧', address = '準備中',
                                                latitude=24.155732100748097, longitude=120.64707590363155)
        line_bot_api.reply_message(event.reply_token, location_message)
        
        ##圖片
        image_message = ImageSendMessage(
        original_content_url='https://memeprod.ap-south-1.linodeobjects.com/user-template/e34fbd9d0e8fbd3b135283d9131fb51c.png',
        preview_image_url= 'https://memeprod.ap-south-1.linodeobjects.com/user-template/e34fbd9d0e8fbd3b135283d9131fb51c.png')
        line_bot_api.reply_message(event.reply_token, image_message)
        '''
        
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage('test！'))
        
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    #testing
