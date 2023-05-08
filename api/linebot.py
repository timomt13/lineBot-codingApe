from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselColumn,
                            CarouselTemplate, MessageAction, URIAction, ImageCarouselColumn, ImageCarouselTemplate,
                            ImageSendMessage)
import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)


# domain root
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


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    image_carousel_columns = [
        ImageCarouselColumn(
            image_url='https://jimmy2130.github.io/WestGolf/images/GaryLuCrop.jpg',
            action=MessageAction(label='Button 1', text='Button 1 pressed')
        ),
        ImageCarouselColumn(
            image_url='https://jimmy2130.github.io/WestGolf/images/VincentLu.jpg',
            action=MessageAction(label='Button 2', text='Button 2 pressed')
        ),
        ImageCarouselColumn(
            image_url='https://jimmy2130.github.io/WestGolf/images/KaiChan.jpg',
            action=MessageAction(label='Button 3', text='Button 3 pressed')
        )
    ]

    image_fee = ImageSendMessage(
                    original_content_url='https://i.imgur.com/KDwuzWN_d.webp?maxwidth=760&fidelity=grand',
                    preview_image_url='https://i.imgur.com/KDwuzWN_d.webp?maxwidth=760&fidelity=grand')
    
    image_teachers = ImageSendMessage(
                original_content_url='https://i.imgur.com/aZSEbsk_d.webp?maxwidth=760&fidelity=grand',
                preview_image_url='https://i.imgur.com/aZSEbsk_d.webp?maxwidth=760&fidelity=grand')
    
    businessHours = '西鈞高爾夫推廣中心\n\
網址：https://jimmy2130.github.io/WestGolf/index.html\n\n\
石牌門市\n\
電話：2828-7313\n\n\
地址：台北市北投區承德路七段223之2號\n\
營業時間：\n\
週一至週五 08:00-22:00\n\
週六、週日 08:00-19:00\n\n\
碧潭門市\n\
電話：2212-6041\n\n\
地址：新北市新店區溪洲路121號\n\
Line ID：@298yqvcd (要加@)\n\
營業時間：\n\
週一至週五 09:30-22:00\n\
週六、週日 08:00-19:00'

    reservation = '感謝您的訊息\n\
課程預約方式：\n\n\
若指定教練，請留下\n\
1、指定教練的姓名，2、自己的聯絡電話，3、預約上課的日期、時段。\n\
小編會聯繫教練，快速地回覆您的訊息。\n\n\
若不指定教練，請留下\n\
1、自己的聯絡電話，2、預約上課的日期、時段。\n\
小編會盡速為您安排'

    text_businessHours = TextSendMessage(text=businessHours)
    text_reservation = TextSendMessage(text=reservation)
    image_carousel_template = ImageCarouselTemplate(columns=image_carousel_columns)
    template_message = TemplateSendMessage(
        alt_text='Image Carousel template',
        template=image_carousel_template
        )

    if event.message.text == '教練介紹':
        line_bot_api.reply_message(event.reply_token, image_teachers)
    if event.message.text == '費用介紹':
        line_bot_api.reply_message(event.reply_token, image_fee)
    if event.message.text == '門市資訊':
        line_bot_api.reply_message(event.reply_token, text_businessHours)
    if event.message.text == '課程預約':
        line_bot_api.reply_message(event.reply_token, text_reservation)


if __name__ == "__main__":
    app.run()
