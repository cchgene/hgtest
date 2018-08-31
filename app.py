from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import random
import requests as r
from bs4 import BeautifulSoup as bs
from datetime import datetime 
import os


# customer module
import mongodb

app = Flask(__name__)

# 必須放上自己的Channel Access Token

channel_access_token =os.environ['Access_Token']
line_bot_api = LineBotApi(channel_access_token)

# 必須放上自己的Channel Secret
channel_secret = os.environ['Secret']
handler = WebhookHandler(channel_secret)

# push給自己
self_uid = os.environ['gene_uid']
line_bot_api.push_message(self_uid, TextSendMessage(text='DD睡醒囉'))

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



@handler.add(FollowEvent)
def handle_follow(event):
    '''
    當使用者加入時觸動
    '''
    # 取得使用者資料
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    
    print(name)
    print(uid)
    
    if mongodb.find_user(uid,'users')<= 0:
        # 整理資料
        dic = {'userid':uid,
               'username':name,
               'creattime':datetime.now(),
               'Note':'user',
               'ready':0}
        
        mongodb.insert_one(dic,'users')





#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得個人資料
    print("----------------必須加入好友才會回覆(個人聊天室、群組聊天室皆可)-------------")
    '''
    當收到使用者訊息的時候
    '''
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    message = event.message.text
    print(name)
    print(uid)
    print(message)
    
    dic = {'userid':uid,
           'username':name,
           'creattime':datetime.now(),
           'message':message}
        
    mongodb.insert_one(dic,'messages')
    
    
    #if mongodb.get_ready(uid,'users') ==1 :
    #    mongodb.update_byid(uid,{'ready':0},'users')
    #    casttext = name+' 對大家說： '+message
    #    remessage = TextSendMessage(text=casttext)
    #    userids = mongodb.get_all_userid('users')
    #    line_bot_api.multicast(userids, remessage)
    #    return 0 
    
    #if message == '群體廣播':
        # 設定使用者下一句話要群廣播
     #   mongodb.update_byid(uid,{'ready':1},'users')
      #  remessage = TextSendMessage(text='請問要廣播什麼呢?')
       # line_bot_api.reply_message(
        #                event.reply_token,
         #               remessage)
        #return 0 
    #print('picture:'+profile.picture_url)
    #print('status_message:'+profile.status_message)
    #print("-------------無須加入好友也會回覆(只限在群組內)--------------------------")
    #profile2 = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
    #print(profile2.display_name)
    #print(profile2.user_id)
    #print(profile2.picture_url)

    # 傳送圖片
    if event.message.text == 'HG':
        message = ImagemapSendMessage(
            base_url='https://i.imgur.com/m1sFvq3.jpg',
            alt_text='HAPPY GO 串聯你的美好生活',
            base_size=BaseSize(height=800, width=600),
            actions=[
                URIImagemapAction(
                    link_uri='https://www.happygocard.com.tw/',
                    area=ImagemapArea(
                        x=0, y=0, width=800, height=600
                    )
)])

    # 傳送影片
    elif event.message.text == 'HG影片':
        message = VideoSendMessage(
            original_content_url='https://video-tpe1-1.xx.fbcdn.net/v/t42.9040-2/40079821_242698919723214_7629329173013594112_n.mp4?_nc_cat=0&efg=eyJ2ZW5jb2RlX3RhZyI6InN2ZV9zZCJ9&oh=605fd4040e31944bae323753de232090&oe=5B8518E5',
            preview_image_url='https://i.imgur.com/m1sFvq3.jpg'
        )
    elif event.message.text == 'HG影片2':
        message = VideoSendMessage(
            original_content_url='https://videos2.sendvid.com/84/e9/v1tdeh6d.mp4?validfrom=1535434749&validto=1535441949&rate=200k&burst=1000k&hash=%2B9pqdo4Ev9T%2BH9qfeEqvAa3tprQ%3D',
            preview_image_url='https://i.imgur.com/m1sFvq3.jpg'
        )
    # 傳送位置
    elif event.message.text == '公司位置':
        message = LocationSendMessage(
            title='公司地點',
            address='板橋',
            latitude=25.013132,
            longitude=121.4670082
        )
        
    #擲骰子
    elif event.message.text == '擲骰子':
        message = TextSendMessage(text=random.choice(['1','2','3','4','5','6']))

    # 傳送貼圖
    elif event.message.text == '抽貼圖':
        #line_picture = random.choice([[random.choice([i for i in range(1,18)] + [21] + [i for i in range(100,140)] + [i for i in range(401,431)]),1],[random.choice([18] + [19] + [20] + [i for i in range(22,48)] + [i for i in range(140,180)] + [i for i in range(501,528)]),2]])
        line_picture = random.choice([[random.choice([i for i in range(1,18)] + [21] + \
                               [i for i in range(100,140)] + [i for i in range(401,431)]),1],\
    [random.choice([18] + [19] + [20] + [i for i in range(22,48)] + \
                   [i for i in range(140,180)] + [i for i in range(501,528)]),2],\
    [random.choice([i for i in range(180,260)]),3],\
    [random.choice([i for i in range(260,308)] + \
                   [i for i in range(601,633)]),4]])
        message = StickerSendMessage(
            package_id=str(line_picture[1]),
            sticker_id=str(line_picture[0]))
        line_bot_api.reply_message(event.reply_token,message)

    elif event.message.text == '卡友好康':
        url = 'https://www.happygocard.com.tw/official/event/calendar/index.html?utm_source=hg&utm_medium=menu&utm_campaign=calendar'
        resp = r.get(url)
        resp.encoding='utf-8'
        soup = bs(resp.text,'html5lib')
        mes_list=[]
        for i in soup.select('ul.bxslider > li > p'):
            mes_list.append(i.text)
        remessage = random.choice(mes_list)
        message = TextSendMessage(text=remessage)
    
    # 傳送確認介面訊息
    elif event.message.text == '我想要評分':
        message = TemplateSendMessage(
            alt_text='今天演講內容滿意嗎？',
            template=ConfirmTemplate(
                text='今天演講內容滿意嗎？',
                actions=[
                    MessageTemplateAction(
                        label='滿意',
                        text='ＧＯＯＤ'
                    ),
                    MessageTemplateAction(
                        label='非常滿意!',
                        text='ＶＥＲＹ　ＧＯＯＤ！'
                    )
                ]
            )
        )

    elif event.message.text == '所有功能':
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/8g83GnI.jpg',
                        title='HAPPY GO',
                        text='串聯生活 放大美好',
                        actions=[
                            URITemplateAction(
                                label='HAPPY GO官方網站',
                                uri='https://www.happygocard.com.tw/#'
                            ),
                            MessageTemplateAction(
                                label='關於HAPPY GO',
                                text='HG影片'
                            ),
                            MessageTemplateAction(
                                label='卡友好康',
                                text='卡友好康'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/F8WHUU6.jpg',
                        title='放鬆自己',
                        text='享受生活',
                        actions=[
                            MessageTemplateAction(
                                label='我想要評分',
                                text='我想要評分'
                            ),
                            MessageTemplateAction(
                                label='放鬆一下',
                                text='抽貼圖'
                            ),
                            MessageTemplateAction(
                                label='比大小',
                                text='擲骰子'
                            )
                        ]
                    )
                ]
            )
        )


    else:
        message = TextSendMessage(text=event.message.text)
        
    line_bot_api.reply_message(event.reply_token,message)

if __name__ == '__main__':
    app.run(debug=True)
