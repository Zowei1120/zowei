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

'''def KeyWord(text):
    KeyWordDict = {"你好":"你好~~",
                   "若薇":"大美女",
                   "早安":"早安安"}
    for k in KeyWordDict.keys():
        if text.find(k) != -1:
            return [True,KeyWordDict[k]]
    return [False]
'''

def Button(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
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
    line_bot_api.reply_message(event.reply_token, message)

'''def Reply(event):
    Ktemp = KeyWord(event.message.text)
    if Ktemp[0]:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = Ktemp[1]))
    else:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = event.message.text))
            '''

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Button(event)
        #Reply(event)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))

#處理Postback
@handler.add(PostbackEvent)
def handle_postback(event):
	command = event.postback.data.split(',')
	if command[0]=="若薇好可愛":
		line_bot_api.reply_message(event.reply_token,
			TextSendMessage(text="是不是~~~"))
		line_bot_api.push_message(event.source.user_id,
			TextSendMessage(text=event.source.user_id))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
