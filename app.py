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
from models.user import Users
from models.database import db_session, init_db

from models.product import Products

app = Flask(__name__)


line_bot_api = LineBotApi('lzozWfpuVLXc+8HXi2P0Fx8mKEHwzL/qNByk9e18l1iNH/gKdPGzz9CeBReDtT5pn1ykwoheynpAhlyatxi8ZTbGkBWBKzeKQgnfMdDkO4SZrqM7r4IQBuK04XDjyBW+MYr6eWixavkESb6/mwKKlwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1768601e8a345509555bc9999ca777ba')


app = Flask(__name__)

#建立或取得user
def get_or_create_user(user_id):
    #從id=user_id先搜尋有沒有這個user，如果有的話就會直接跳到return
    user = db_session.query(Users).filter_by(id=user_id).first()
    #沒有的話就會透過line_bot_api來取得用戶資訊
    if not user:
        profile = line_bot_api.get_profile(user_id)
        #然後再建立user並且存入到資料庫當中
        user = Users(id=user_id, nick_name=profile.display_name, image_url=profile.picture_url)
        db_session.add(user)
        db_session.commit()

    return user


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

    ########## 使用說明、選單 ##########
    if message_text == '@使用說明':
        about_us_event(event)
    elif message_text =='@我想訂購商品':
        message = Products.list_all()
    if messages:
        line_bot_api.reply_message(
        event.reply_token,
        message)
    
#初始化產品資訊
@app.before_first_request
def init_products():
    # init db
    result = init_db()#先判斷資料庫有沒有建立，如果還沒建立就會進行下面的動作初始化產品
    if result:
        init_data = [Products(name='Lamborghini',
                              product_image_url='https://i.imgur.com/EYhLvum.jpg',
                              price=250,
                              description='nascetur ridiculus mus. Donec quam felis, ultricies'),
                     Products(name='BMW',
                              product_image_url='https://i.imgur.com/Pz56QQ9.png',
                              price=200,
                              description='adipiscing elit. Aenean commodo ligula eget dolor'),
                     Products(name='BENZ',
                              price=200,
                              product_image_url='https://i.imgur.com/t4zauYW.jpg',
                              description='Aenean massa. Cum sociis natoque penatibus')]
        db_session.bulk_save_objects(init_data)#透過這個方法一次儲存list中的產品
        db_session.commit()#最後commit()才會存進資料庫
        #記得要from models.product import Products在app.py

if __name__ == "__main__":
    init_products()
    app.run()


@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = '''Hello! 您好，歡迎成為Hi Car的好友

我是Hi Car小幫手'''

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg))


if __name__ == "__main__":
    init_db()
    app.run()
