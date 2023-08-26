from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,StickerSendMessage,FollowEvent,UnfollowEvent,
)
from linebot.models import *

app = Flask(__name__)


line_bot_api = LineBotApi('lzozWfpuVLXc+8HXi2P0Fx8mKEHwzL/qNByk9e18l1iNH/gKdPGzz9CeBReDtT5pn1ykwoheynpAhlyatxi8ZTbGkBWBKzeKQgnfMdDkO4SZrqM7r4IQBuK04XDjyBW+MYr6eWixavkESb6/mwKKlwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1768601e8a345509555bc9999ca777ba')


app = Flask(__name__)


def about_us_event(event):
    emoji = [
            {
                "index": 0,
                "productId": "5ac21184040ab15980c9b43a",
                "emojiId": "225"
            },
            {
                "index": 17,
                "productId": "5ac21184040ab15980c9b43a",
                "emojiId": "225"
            }
        ]

    text_message = TextSendMessage(text='''$ Master RenderP $
Hello! 您好，歡迎您成為 Master RenderP 的好友！

我是Master 支付小幫手 

-這裡有商城，還可以購物喔~
-直接點選下方【圖中】選單功能

-期待您的光臨！''', emojis=emoji)

    sticker_message = StickerSendMessage(
        package_id='8522',
        sticker_id='16581271'
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message])
    
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
	
#處裡訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = line_bot_api
    message_text = str(event.message.text).lower()

    ### 使用說明、選單 ###
    if message_text == '@使用說明':
        about_us_event(event)

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Hi Welcome to LSTORE'))
    
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = '''Hello! 您好，歡迎成為Hi Car的好友

我是Hi Car小幫手'''

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg))


if __name__ == "__main__":
    
    app.run()