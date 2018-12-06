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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Reply(event)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = str(e)))

def KeyWord(text):
    KeyWordDict = {"你好":"你好你好你好~","早安":"早安阿","幹":"不要罵髒話!"}
    for k in KeyWordDict.keys():
        if text.find(k) != -1:
            return [True,KeyWordDict[k]]
        return[False]

def Reply(event):
    Ktemp = KeyWord(event.message.text)
    if Ktemp[0]:
        line_bot_api.reply_Message(event.reply_token,TextSendMessage(text=Ktemp[1]))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = event.message.text))



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)