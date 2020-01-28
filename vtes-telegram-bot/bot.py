import logging
import os
from uuid import uuid4
from telegram import InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_query(update, context):
    query = update.inline_query.query

    results = [
        InlineQueryResultPhoto(id=uuid4(),
                               title="Art's Traumatic Essence",
                               thumb_url="https://vtes.dirtydevelopers.org/img/100100.jpg",
                               photo_url="https://vtes.dirtydevelopers.org/img/100100.jpg"),
        InlineQueryResultPhoto(id=uuid4(),
                               title="Ankla Hotep",
                               thumb_url="https://vtes.dirtydevelopers.org/img/200100.jpg",
                               photo_url="https://vtes.dirtydevelopers.org/img/200100.jpg"),
    ]

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

