
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent, 
    StickerSendMessage, ImageSendMessage, LocationSendMessage,FlexSendMessage,
    TemplateSendMessage,ImageCarouselTemplate,ImageCarouselColumn,PostbackAction,
    PostbackEvent,QuickReply,QuickReplyButton,ConfirmTemplate,MessageAction,ButtonsTemplate
)

# Channel access token
line_bot_api = LineBotApi('lzozWfpuVLXc+8HXi2P0Fx8mKEHwzL/qNByk9e18l1iNH/gKdPGzz9CeBReDtT5pn1ykwoheynpAhlyatxi8ZTbGkBWBKzeKQgnfMdDkO4SZrqM7r4IQBuK04XDjyBW+MYr6eWixavkESb6/mwKKlwdB04t89/1O/w1cDnyilFU=')
#Channel secret
handler = WebhookHandler('1768601e8a345509555bc9999ca777ba')