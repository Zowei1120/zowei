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
line_bot_api = LineBotApi('EYOPugWAkwk+VWuUxPmAp2DRmxusDo/vWrjrxBkTsv7q9N8Zb+44ogpthavRw7jN+gdZL2QxRVnhLqBxpM+L+vuERXaAnx00DY4cda1UMFWlR+YQ/JO1KB7towhVR6zHfIrIkHi9/T0nmb/E4Rv6EQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('77cd391a547b354792a6752b4270fcd2')

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

#----------從這裡開始複製----------

#會員系統
def GetUserlist():
    userlist = {}
    file = open('users','r')
    while True :
        temp = file.readline().strip().split(',')
        if temp[0] == "" : break
        userlist[temp[0]] = temp[1]
    file.close()
    return userlist

#登入系統
def Login(event,userlist):
    i = 0
    for user in userlist.keys():
        if event.source.user_id == user:
            return i
        i+=1
    return -1

#寫入資料
def Update(userlist):
    file = open('users','w')
    for user in userlist.keys():
        file.write(user+','+userlist[user])
    file.close()


#關鍵字系統
def Keyword(event):
    KeyWordDict = {"你好":["text","你好你好"],
                   "早安阿":["text","早安安"],
                   "早安":["text","早安阿"],
                   "哈囉":["text","嗨"],
                   "愛你":["sticker",'2','172']}

    for k in KeyWordDict.keys():
        if event.message.text.find(k) != -1:
            if KeyWordDict[k][0] == "text":
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = KeyWordDict[k][1]))
            elif KeyWordDict[k][0] == "sticker":
                line_bot_api.reply_message(event.reply_token,StickerSendMessage(
                    package_id=KeyWordDict[k][1],
                    sticker_id=KeyWordDict[k][2]))
            return True
    return False

#按鈕版面系統
def Button(event):
    line_bot_api.reply_message(event.reply_token,
        TemplateSendMessage(
            alt_text='特殊訊息，請進入手機查看',
            template=ButtonsTemplate(
                thumbnail_image_url='https://github.com/Zowei1120/zowei/blob/master/%E6%B0%B4%E8%B1%9A.jpg?raw=true',
            title='Menu',
            text='Please select',
            actions=[
                PostbackTemplateAction(
                    label='若薇好可愛',
                    text='我也覺得若薇好可愛',
                    data='若薇好可愛'
                ),
                MessageTemplateAction(
                    label='若薇好棒棒',
                    text='若薇超棒的♥'
                ),
                URITemplateAction(
                    label='我好想認識若薇',
                    uri='https://www.instagram.com/zowei1120/'

                )
                ]
            )
        )
    )

#指令系統，若觸發指令會回傳True
def Command(event):
    tempText = event.message.text.split(",")
    if tempText[0] == "發送" and event.source.user_id == "U10effeaeced164d73397ef798539b586":
        line_bot_api.push_message(tempText[1], TextSendMessage(text=tempText[2]))
        return True
    else:
        return False
    
#新增一個參數
def Reply(event,userlist):
    if not Command(event):
        Ktemp = KeyWord(event)
        if Ktemp[0]:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text = Ktemp[1]))
        else:
            if userlist[event.source.user_id] == '-1':
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text = "你知道台灣最稀有、最浪漫的鳥是哪一種鳥嗎？"))
                userlist[event.source.user_id] = '0'
            else:
                if event.message.text == "黑面琵鷺":
                    line_bot_api.reply_message(event.reply_token,
                        TextSendMessage(text = "你居然知道答案!!!"))
                else:
                    line_bot_api.reply_message(event.reply_token,
                        TextSendMessage(text = "答案是：黑面琵鷺!!!因為每年冬天，他們都會到台灣來\"壁咚\""))
                userlist[event.source.user_id] = '-1'

#回覆函式，指令 > 關鍵字 > 按鈕
def Reply(event):
    if not Command(event):
        if not Keyword(event):
            Button(event)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        userlist = GetUserlist()
        clientindex = Login(event,userlist)
        if clientindex > -1:
            Reply(event,userlist)
            '''
            line_bot_api.push_message("U95418ebc4fffefdd89088d6f9dabd75b", TextSendMessage(text=event.source.user_id + "說:"))
            line_bot_api.push_message("U95418ebc4fffefdd89088d6f9dabd75b", TextSendMessage(text=event.message.text))
            '''
        else:
            userlist[event.source.user_id] = '-1';
            line_bot_api.reply_message(event.reply_token, 
                TextSendMessage(text="註冊成功"))
        Update(userlist)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))
        
#處理Postback
@handler.add(PostbackEvent)
def handle_postback(event):
    command = event.postback.data.split(',')
    if command[0] == "若薇好可愛":
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="是不是~~~"))
        
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id='2',
            sticker_id='34')
    )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
