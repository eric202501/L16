from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselColumn,
                            CarouselTemplate, MessageAction, URIAction, ImageCarouselColumn, ImageCarouselTemplate,
                            ImageSendMessage, ButtonsTemplate, ConfirmTemplate)
import os
import requests
from bs4 import BeautifulSoup
import random

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def random_ptt_boards():
    board_info = []
    response = requests.get('https://www.ptt.cc/bbs/index.html')
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有討論版的名稱和URL
    data = soup.find_all('div', class_='b-ent')

    for board in data:
        board_name = board.find('div', class_='board-name').text
        board_url = 'https://www.ptt.cc' + board.find('a')['href']
        temp = [board_name, board_url]  # 把板名和 URL 整理成清單
        board_info.append(temp)

    return board_info

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text == 'confirm':
        confirm_template = TemplateSendMessage(
            alt_text = 'confirm template',
            template = ConfirmTemplate(
                text = 'drink coffee?',
                actions = [
                    MessageAction(
                        label = 'yes',
                        text = 'yes'),
                    MessageAction(
                        label = 'no',
                        text = 'no')]
                )
            )
        line_bot_api.reply_message(event.reply_token, confirm_template)


    #按鈕樣板
    if event.message.text == 'button':
        buttons_template = TemplateSendMessage(
            alt_text = 'buttons template',
            template = ButtonsTemplate(
                thumbnail_image_url='https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                title = 'Brown Cafe',
                text = 'Enjoy your coffee',
                actions = [
                    MessageAction(
                        label = '咖啡有什麼好處',
                        text = '讓人有精神'),
                    URIAction(
                        label = '伯朗咖啡',
                        uri = 'https://www.mrbrown.com.tw/')]
                )
            )

        line_bot_api.reply_message(event.reply_token, buttons_template)


    #carousel樣板
    if event.message.text == 'carousel':
        carousel_template = TemplateSendMessage(
            alt_text = 'carousel template',
            template = CarouselTemplate(
                columns = [
                    #第一個
                    CarouselColumn(
                        thumbnail_image_url = 'https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        title = 'this is menu1',
                        text = 'menu1',
                        actions = [
                            MessageAction(
                                label = '咖啡有什麼好處',
                                text = '讓人有精神'),
                            URIAction(
                                label = '伯朗咖啡',
                                uri = 'https://www.mrbrown.com.tw/')]),
                    #第二個
                    CarouselColumn(
                        thumbnail_image_url = 'https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        title = 'this is menu2',
                        text = 'menu2',
                        actions = [
                            MessageAction(
                                label = '咖啡有什麼好處',
                                text = '讓人有精神'),
                            URIAction(
                                label = '伯朗咖啡',
                                uri = 'https://www.mrbrown.com.tw/')])
                ])
            )

        line_bot_api.reply_message(event.reply_token, carousel_template)


    #image carousel樣板
    if event.message.text == 'image carousel':
        image_carousel_template = TemplateSendMessage(
            alt_text = 'image carousel template',
            template = ImageCarouselTemplate(
                columns = [
                    #第一張圖
                    ImageCarouselColumn(
                        image_url = 'https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        action = URIAction(
                            label = '伯朗咖啡',
                            uri = 'https://www.mrbrown.com.tw/')),
                    #第二張圖
                    ImageCarouselColumn(
                        image_url = 'https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        action = URIAction(
                            label = '伯朗咖啡',
                            uri = 'https://www.mrbrown.com.tw/'))                       
                ])
            )

        line_bot_api.reply_message(event.reply_token, image_carousel_template)

    
    if event.message.text == 'ptt':
        try:
            board_info = []
            response = requests.get('https://www.ptt.cc/bbs/index.html')
            soup = BeautifulSoup(response.text, 'html.parser')
            data = soup.find_all('div', class_='b-ent')

            for board in data:
                board_name = board.find('div', class_='board-name').text
                board_url = 'https://www.ptt.cc' + board.find('a')['href']
                temp = [board_name, board_url]  # 把板名和 URL 整理成清單
                board_info.append(temp)

            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(soup)[0:1000]+str(len(data))))

        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(e)))


if __name__ == "__main__":
    app.run()