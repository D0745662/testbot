# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com
Line Bot聊天機器人
第三章 互動回傳功能
推播push_message與回覆reply_message
webhook url : 
localhost: https://7580-39-9-62-241.ngrok.io 
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort, g
import json, sys

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
import time

# clawer
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

#screenshot
from time import sleep

# 載入 recommendation core
import random, urllib.parse
import recommend as pv254
import appDB.streamlit_app1 as cocktailDB
import importlib
# sys.path.remove('C:\\Users\\DLJW_\\Desktop\\CocktailAnalysis-main\\utils')
# sys.path.append('appDB\\utils')
print(sys.path)
# print(sys.path)
app = Flask(__name__)




default_image = ['https://www.thecocktaildb.com/images/media/drink/5jhyd01582579843.jpg',
                 'https://www.thecocktaildb.com/images/media/drink/ck6d0p1504388696.jpg',
                 'https://www.thecocktaildb.com/images/media/drink/jrhn1q1504884469.jpg',
                 'https://www.thecocktaildb.com/images/media/drink/swqurw1454512730.jpg',
                 'https://www.thecocktaildb.com/images/media/drink/7p607y1504735343.jpg',
                 'https://www.thecocktaildb.com/images/media/drink/1sqm7n1485620312.jpg',
                 'https://www.thecocktaildb.com/images/media/drink/8189p51504735581.jpg',
                 'https://www.liquor.com/thmb/J5D8YO2tqpeM6C3bBefc75LuHyI=/960x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/__opt__aboutcom__coeus__resources__content_migration__liquor__2019__11__20141136__temple-toddy-720x720-recipe-049dfb9bfa4340a9860c5d14590366e4.jpg',
                 'https://www.liquor.com/thmb/HTYQdDqLp_HUALyJKZmstD-XwII=/960x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/__opt__aboutcom__coeus__resources__content_migration__liquor__2019__07__12101312__Blue-Hawaii-720x720-recipe-1c521445b9394786abe8215118baf734.jpg']


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#follow區塊
##### 基本上程式編輯都在這個function #####
@handler.add(FollowEvent) 
def handle_follow(event):
    print(event.source.user_id)
    try:
        profile = line_bot_api.get_profile(event.source.user_id)
    except LineBotApiError as e:
        print(e)
    msg = '您好'+profile.display_name
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text=msg))
    flex_message = TextSendMessage(text='以下有雷，請小心',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=PostbackAction(label="附近酒吧", data="quick：")),
                                    QuickReplyButton(action=PostbackAction(label="查詢XX周圍的酒吧", data="quick：指定查詢")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                    QuickReplyButton(action=MessageAction(label="別按我", text="爆炸了！！")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！"))
                                ]))     
    line_bot_api.push_message(event.source.user_id, flex_message)

@handler.add(MessageEvent, message=LocationMessage)
def location(event):
    lat = event.message.latitude
    lng = event.message.longitude
    barSearch = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=bar&language=zh-TW".format('',lat ,lng)
    barReq = requests.get(barSearch)
    nearby_bar_dict = barReq.json()
    top20_bar= nearby_bar_dict["results"]
    res_num = (len(top20_bar))

    bravo=[]
    for i in range(res_num):
        try:
            if top20_bar[i]['rating'] > 0:
                print('rate: ', top20_bar[i]['rating'])
                bravo.append(i)
        except:
            KeyError
    if len(bravo) < 0:
        content = "沒東西可以吃"

    bar = top20_bar[random.choice(bravo)]
    barlist = []
    for i in range(0,4):
        tempbar = top20_bar[random.choice(bravo)]
        while tempbar in barlist:
            tempbar = top20_bar[random.choice(bravo)]
           
        barlist.append(tempbar)
    list_template = []    
    for i in range(0,4):
        print(i)
        if barlist[i].get("photos") is None:
            thumbnail_image_url = None
        else:
            photo_reference = barlist[i]["photos"][0]["photo_reference"]
            photo_width = barlist[i]["photos"][0]["width"]
            thumbnail_image_url = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}".format('',photo_reference,photo_width)
    
        rating = "無" if barlist[i].get("rating") is None else barlist[i]["rating"]
        address = "沒有資料" if barlist[i].get ("vicinity") is None else barlist[i]["vicinity"]
        details = "Google Map評分 : {}\n地址 : {}".format(rating, address)
        
        map_url = "https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}".format(lat=barlist[i]["geometry"]["location"]["lat"],long=barlist[i]["geometry"]["location"]["lng"],place_id=barlist[i]["place_id"])
        
        item = CarouselColumn(
           thumbnail_image_url=thumbnail_image_url,
                title=barlist[i]["name"],
                text=details,
                actions=[
                    URITemplateAction(
                        label='查看地圖',
                        uri=map_url
                    ),
                    URITemplateAction(
                        label='查看完整地圖',
                        uri="https://www.google.com/maps/search/bar/@{},{},16z".format(lat,lng)
                    ),
                ]
        )
        list_template.append(item)
    print(barlist)
    Carousel_template = TemplateSendMessage(
        alt_text='附近評價不錯的酒吧',
        template=CarouselTemplate( 
            columns=list_template
        )
    )   
    
    line_bot_api.reply_message(event.reply_token, Carousel_template)
    
    return 0



#訊息Postback區塊
##### 基本上程式編輯都在這個function #####
@handler.add(PostbackEvent) 
def handle_postback(event):
    print('this is postback')
    print()
    message = event.postback.data
    # 【回復】看調酒更多資訊
    if re.match('-->',message[3:6]):
        info_cocktail_dict = cocktailDB.getCocktailDetail(message[6:])
        print(info_cocktail_dict)
        image = info_cocktail_dict['image']
        if image == '':
            image = cocktailDB.getImg(info_cocktail_dict['name'])
            # image = default_image[random.randint(0,8)]
        replyMsg = ImageSendMessage(
            original_content_url = image,
            preview_image_url = image
        )
        print('here')
        # line_bot_api.reply_message(event.reply_token, replyMsg)
        textmessage = 'Name:  '+ info_cocktail_dict['name'] +'\n'
        textmessage += 'Ingredients:  '+ info_cocktail_dict['ingredients'] +'\n'
        textmessage += 'Garnish:  '+ info_cocktail_dict['garnish'] +'\n'
        #button 1
        label1 = '翻譯'
        data1 = "Action1:翻譯"+ info_cocktail_dict['name']
        
        #ensure reply message size lessthan 240
        if len(textmessage+info_cocktail_dict['preparation'])<226:
            textmessage += 'Preparation:  '+ info_cocktail_dict['preparation']
        else:
            label1 = 'Preparation  '
            data1 = 'Action1:Preparation:  '+ info_cocktail_dict['name']
            pass
        confirm_template_message = TemplateSendMessage(
            alt_text= info_cocktail_dict['name']+'的更多資訊...',
            template=ConfirmTemplate(
                text=textmessage,
                actions=[
                    PostbackAction(
                        label=label1,
                        data=data1#json.dumps(info_cocktail_dict)
                    ),
                    PostbackAction(
                        label='喜歡',
                        data="favourite：" + info_cocktail_dict['name']
                    ),
                ]
            )
        )   
        line_bot_api.reply_message(event.reply_token, [replyMsg,confirm_template_message])
    elif re.match('Action1',message[0:7]):
        print('Action : ')
        
        if re.match('翻譯',message[8:10]):
            cocktail_dict = cocktailDB.getCocktailDetail(message[10:])
            # cocktail_dict = json.loads(message[9:])
            print(urllib.parse.quote(cocktail_dict['name']))
            headers = {'cookie': 'ECC=GoogleBot',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
            url = 'https://translate.google.com.tw/?hl=zh-TW&sl=en&tl=zh-TW&text='+urllib.parse.quote(cocktail_dict['preparation'])+'&op=translate'
            
            line_bot_api.push_message(event.source.user_id, TextSendMessage(text='翻譯中...') )
            driver = webdriver.Chrome()
            driver.get(url)
            doTranslate = True
            while doTranslate:
                target = driver.find_elements_by_class_name('dePhmb')
                if len(target)<=0:
                    continue
                target = target[0].find_elements_by_class_name('VIiyi')
                if len(target)<=0 :
                    continue
                target = target[0].find_elements_by_tag_name('span')
                doTranslate = False
                print(target[0].text)
                print(len(target))
            # target = driver.find_element_by_xpath('/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]/span[1]').find_elements_by_tag_name('span')
            
            for i in target:
                print(i.text)
            reply = ''
            for sentence in range(1,len(target),2):
                reply += target[sentence].text
            print(reply)
            driver.close()
        
            line_bot_api.reply_message(event.reply_token,  TextSendMessage(text='配製方法： '+reply))
        elif re.match('Preparation:',message[8:20]):
            cocktail_dict = cocktailDB.getCocktailDetail(message[22:])
            confirm_template_message = TemplateSendMessage(
                alt_text=cocktail_dict['name'] + '的配製方法',
                template=ConfirmTemplate(
                    text='Preparation:  ' + cocktail_dict['preparation'],
                    actions=[
                        PostbackAction(
                            label='翻譯',
                            data="Action:翻譯"+cocktail_dict['name'] #json.dumps(info_cocktail_dict)
                        ),
                        PostbackAction(
                            label='喜歡',
                            data="favourite：" + cocktail_dict['name']
                        ),
                    ]
                )
            )   
            line_bot_api.reply_message(event.reply_token, confirm_template_message)
    elif re.match('quick：',message[0:6]):
        if re.match('指定查詢',message[6:10]):
            msg='想查詢哪個地區的酒吧？\n回復地區時\n請加上 區域@\n 範本：區域@逢甲'
            line_bot_api.reply_message(event.reply_token,  TextSendMessage(text=msg))
        # elif re.match('popup',message[6:11]):
        #     confirm_template_message = TemplateSendMessage(
        #         alt_text= '該區域更多的酒吧',
        #         template=ConfirmTemplate(
        #             text=message[11:]+'附近更多的酒吧',
        #             actions=[
        #                 PostbackAction(
        #                     label='打開',
        #                     uri='https://www.google.com.tw/maps/search/'+message[11:]+'酒吧'
        #                 ),
        #                 PostbackAction(
        #                     label='推薦調酒',
        #                     data='recommend：'
        #                 )
        #             ]
        #         )
        #     )   
        #     line_bot_api.reply_message(event.reply_token, confirm_template_message)
        else:
            quick_reply = TextSendMessage(text='以下有雷，請小心',
                                           quick_reply=QuickReply(items=[
                                                   QuickReplyButton(action=LocationAction(label="定位"))
                                        ]))
            line_bot_api.reply_message(event.reply_token, quick_reply)
    else:
        pass

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('Server get message : '+ event.message.text)
    print()
    message = text = event.message.text
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
                        data='action=檯面下'
                    ),
                    MessageAction(
                        label='直接傳',
                        text='這是資料'
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
        
        flex_message = TextSendMessage(text='以下有雷，請小心',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=PostbackAction(label="附近酒吧", data="quick：")),
                                    QuickReplyButton(action=PostbackAction(label="查詢XX周圍的酒吧", data="quick：指定查詢")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                    QuickReplyButton(action=MessageAction(label="別按我", text="爆炸了！！")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！")),
                                    QuickReplyButton(action=MessageAction(label="按我", text="按！"))
                                ]))     
        line_bot_api.push_message(event.source.user_id, flex_message)
        
        
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
                        text='舒坦啊'
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
            template = ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/Aax1R2U.jpg',
                        action=URIAction(
                            label='附近有什麽',
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
    elif re.match('區域',message[0:2]):
        # first 5 bar 
        targetarea = message[3:]
        
        headers = {'cookie': 'ECC=GoogleBot','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        url = 'https://www.google.com.tw/maps/search/'+targetarea+'酒吧'
        
        line_bot_api.push_message(event.source.user_id, TextSendMessage(text='搜尋中...') )
        driver = webdriver.Chrome()
        driver.get(url)
        img = driver.find_element_by_id('pane').find_elements_by_tag_name('a')[0].click()
        print(img)
        sleep(7)
        temp = driver.find_element_by_id('bottom-pane').find_elements_by_tag_name('img')
        barList = driver.find_element_by_id('bottom-pane').find_elements_by_class_name('GgK1If')
        imgList = []
        
        for val in temp:
            if val.get_attribute('src') != None and val.get_attribute('src')[8]=='l' :
                imgList.append(val)
                
        outputcolumns = []
        
        for i in range(0,len(imgList)):
            # print(imgList[i].get_attribute('src'))
            # print(barList[i].text)
            if i == 5:
                outputcolumns.append(
                ImageCarouselColumn(
                        image_url=imgList[i].get_attribute('src'),
                        action=URIAction(
                            label='看更多',
                            uri='https://www.google.com.tw/maps/search/'+targetarea+'酒吧'
                        )
                    )
                )
                break
            outputcolumns.append(
                ImageCarouselColumn(
                        image_url=imgList[i].get_attribute('src'),
                        action=URIAction(
                            label=barList[i].text[0:11],
                            uri='https://www.google.com.tw/maps/search/'+urllib.parse.quote(barList[i].text[0:])
                        )
                    )
                )
        driver.close()
        image_carousel_template_message = TemplateSendMessage(
            alt_text='圖片',
            template = ImageCarouselTemplate(
                columns=outputcolumns
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
    # 處理 推薦失敗狀況
    elif re.match('沒錯，這樣也不知道',message):
        noCocktail = replyRecommendCocktail(message, event)
        if not noCocktail:
            sticker_message = StickerSendMessage(package_id=11539,sticker_id=52114115)
            line_bot_api.reply_message(event.reply_token, [sticker_message, TextSendMessage(text='抱歉，沒聽説過，可以試試別的。')])
        # print(g.preStateMgs)
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=g.preStateMgs))
    elif re.match('不是的:',message):
        # example mojito 可以計算該使用者推薦的調酒 供他輸入
        sticker_message = StickerSendMessage(package_id=11539,sticker_id=52114115)
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='您可以嘗試輸入酒品的名字。\n像mojito之類的~\n我們在為您推薦。'),sticker_message])          
    elif re.match('map',message):
        imagemap_message = ImagemapSendMessage(
                        base_url='',
                        alt_text='this is an imagemap',
                        base_size=BaseSize(height=520, width=520),
                        actions=[
                            URIImagemapAction(
                                link_uri='',
                                area=ImagemapArea(
                                    x=174, y=65, width=707, height=416
                                )
                            ),
                            MessageImagemapAction(
                                text='hello',
                                area=ImagemapArea(
                                    x=520, y=0, width=520, height=520
                                )
                            )
                        ]
                    )
        line_bot_api.reply_message(event.reply_token,imagemap_message)
        
        
    # 處理 推薦部分
    # Ingredient Part
    elif re.match('是的，含有【', message[0:6]):
        ingredient = message[6:].split('】')
        print(ingredient)
        noCocktail = replyRecommendCocktail(ingredient[0], event, 5)
        if not noCocktail:
            sticker_message = StickerSendMessage(package_id=11537,sticker_id=52002754)
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text='抱歉，還是找不到有關'+ingredient[0]+'成分的調酒。'), sticker_message])
    # Unknow & cocktail name Part
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
        # 推薦是否成功 
        noCocktail = replyRecommendCocktail(message, event, 5)
        print('else')
        if not noCocktail:
            print(': else')
            confirm_template_message = TemplateSendMessage(
                alt_text='你想表達的是。。。？',
                template=ConfirmTemplate(
                    text='您輸入的是調酒成分嗎？',
                    actions=[
                        MessageAction(
                            label='是的',
                            text='是的，含有【' + message + '】成分的調酒有哪些？'
                        ),
                        MessageAction(
                            label='不是',
                            text='不是的:'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, confirm_template_message)
# 先前已判斷 確定做推薦        
def replyRecommendCocktail(message, event, amount):
    recommend_cocktailList = []
    # cocktail name in DB
    if cocktailDB.checkCocktailinDB(message):
        recommend_cocktailList = getRecommend(message, amount)
        cocktailList_template = []
        for i, cocktail in enumerate(recommend_cocktailList):
            print('234')
            name = cocktail['name']
            image = cocktail['image']
            ingredient = cocktail['ingredients']
            garnish = cocktail['garnish']
            preparation = cocktail['preparation']
            if image == '':
                print('null')
                image = default_image[random.randint(0,8)]
            
            item = CarouselColumn(
                thumbnail_image_url=image,
                title=(str(i+1))+')'+name,
                text='成分: '+ingredient[0:52],
                actions=[
                    PostbackAction(
                        label='更多資訊',
                        data="看更多-->"+name
                    ),
                    MessageAction(
                        label='喜歡',
                        text='這是資料1'
                    ),
                    MessageAction(
                        label='不喜歡',
                        text='這是資料2'
                    )
                ]
            )
            cocktailList_template.append(item)
        Carousel_template = TemplateSendMessage(
            alt_text='您可能會喜歡的四個調酒~',
            template=CarouselTemplate( 
                columns=cocktailList_template
            )
        )   
        line_bot_api.reply_message(event.reply_token, [Carousel_template])
        return True
    # not in DB, so input: ingredients
    else:
        recommend_cocktailList = getRecommend(message, amount)
        print(recommend_cocktailList)
        if len(recommend_cocktailList) == 0:
            return False
        else:
            print('yes')
            cocktailList_template = []
            for i, cocktail in enumerate(recommend_cocktailList):
                print('234')
                name = cocktail['name']
                image = cocktail['image']
                ingredient = cocktail['ingredients']
                garnish = cocktail['garnish']
                preparation = cocktail['preparation']
                if image == '':
                    print('null')
                    image = default_image[random.randint(0,8)]
                
                item = CarouselColumn(
                    thumbnail_image_url=image,
                    title=(str(i+1))+')'+name,
                    text='成分: '+ingredient[0:52],
                    actions=[
                        PostbackAction(
                            label='更多資訊',
                            data="看更多-->"+name
                        ),
                        MessageAction(
                            label='喜歡',
                            text='這是資料1'
                        ),
                        MessageAction(
                            label='不喜歡',
                            text='這是資料2'
                        )
                    ]
                )
                cocktailList_template.append(item)
            Carousel_template = TemplateSendMessage(
                alt_text='您可能會喜歡的四個調酒~',
                template=CarouselTemplate( 
                    columns=cocktailList_template
                )
            )   
            line_bot_api.reply_message(event.reply_token, [Carousel_template])
            return True
        
        
def getRecommend(user_input, amount):
    # num = random.randint(7,14)
    # profile = [27,60,80,1563,1012,861,457,950]
    # rec_list = Recommend(profile, num, False, False, True);
    # print(rec_list)
    #return rec_list
    
    # -- CocktailAnalysis [ theCocktailDB ] --
    recommend_cocktailList = cocktailDB.doCocktailAnalyDB(user_input, amount)
    return recommend_cocktailList
        
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    

    #testing
