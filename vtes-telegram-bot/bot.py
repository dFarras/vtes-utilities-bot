import logging
import os
from uuid import uuid4
from telegram import InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def get_cards(query):
    rs = requests.get("https://api.bloodlibrary.info/api/search", params={'name': query})
    if rs.status_code != 200:
        raise Exception(f"[${rs.status_code}]$ {rs.text}")

    return rs.json()


def build_query_result(card):
    return InlineQueryResultPhoto(id=uuid4(),
                                  title=card['name'],
                                  thumb_url=card['image'],
                                  photo_url=card['image'])


def handle_query(update, context):
    query = update.inline_query.query

    if not query or len(query) < 3:
        return

    cards = get_cards(query)

    results = [build_query_result(c) for c in cards[:14]]

    return update.inline_query.answer(results)


def handle_error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    bot_token = os.getenv("TELEGRAM_TOKEN", None)
    if not bot_token:
        raise Exception("Invalid Telegram bo token.")

    updater = Updater(bot_token, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(InlineQueryHandler(handle_query))
    dispatcher.add_error_handler(handle_error)

    updater.start_polling()
    updater.idle()
