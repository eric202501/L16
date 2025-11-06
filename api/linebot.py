from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError


from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselColumn,
                            CarouselTemplate, MessageAction, URIAction, ImageCarouselColumn, ImageCarouselTemplate,
                            ImageSendMessage, ButtonsTemplate, ConfirmTemplate)
import os


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text.lower() == "test":
        reply_message = "第32行的reply_message=改成自己想傳送的訊息"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_message))

    elif event.message.text.lower() == "button":
        try:
            buttons_template = TemplateSendMessage(
                alt_text='buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                    title='Brown Cafe',
                    text='Enjoy your coffee',
                    actions=[
                        MessageAction(
                            label='咖啡有什麼好處',
                            text='讓人有精神'),
                        URIAction(
                            label='伯朗咖啡',
                            uri='https://www.mrbrown.com.tw/')
                    ]
                )
            )

            # 嘗試回覆樣板訊息
            line_bot_api.reply_message(event.reply_token, buttons_template)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(e)))
    else:
        reply_message = event.message.text
    
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run()