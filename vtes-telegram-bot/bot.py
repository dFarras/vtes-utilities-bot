import io
import logging
from tkinter import Image

from telegram import Update, InlineQueryResultPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hola! Soy VTES ALLY, tu guía en el sombrío mundo de los vampiros"
    )


async def vtes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*¿Qué es VTES?*\n"
             "  \- Es un juego de cartas ambientado en el mundo de tinieblas de Vampiro la Mascarada\n"
             "  \- Sin embargo juego *no es un TCG*, y *no existen los sobres* ni la obligación de comprar cartas \(se acpetan proxies\)\n"
             "  \- En los torneos es el organizador quien permite o no los proxies, la inmensa mayoría *si los permiten*\n\n"
             "[Nociones básicas](https://www.youtube.com/watch?v=velKoYv3LXM)",
        parse_mode='MarkdownV2',
        disable_web_page_preview=True
    )


async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="[Reglas](https://www.blackchantry.com/utilities/rulebook/)\n"
             "[Generador de mazos y libreria de mazos y cartas](https://vtesdecks.com/)\n"
             "[Generador de proxies](https://bloodlibrary.info/)\n",
        parse_mode='MarkdownV2',
        disable_web_page_preview=True
    )


async def get_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card_name = ""
    for arg in context.args:
        if len(card_name) > 0:
            card_name += " "
        card_name += arg
    rs = requests.get("https://api.bloodlibrary.info/api/search", params={'name': card_name})
    if rs.status_code != 200:
        raise Exception(f"[${rs.status_code}]$ {rs.text}")
    cards = rs.json()
    for c in cards[:14]:
        available_sets = list(filter(lambda s: s['image'], c['publish_sets']))
        available_sets.sort(key=lambda s: s['set_id'], reverse=True)
        image = requests.get(available_sets[0]['image'])
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image.content
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token('6520029161:AAEv6MmrWZrX2c4yqUIFqhIZLryseAtqPkM').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('vtes', vtes))
    application.add_handler(CommandHandler('enlaces', links))
    application.add_handler(CommandHandler('consultar_carta', get_card, has_args=True))

    application.run_polling()
