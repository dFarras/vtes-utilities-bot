import logging
import os
import requests

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class Message:
    text: str = ""
    preview: bool = False

    def __init__(self, text, preview=False):
        self.text = text
        self.preview = preview


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hola\! Soy VTES ALLY, tu guía en el sombrío y oscuro mundo de los vampiros \U0001F9DB\u200D\u2640\uFE0F",
        parse_mode='MarkdownV2'
    )


async def vtes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="\U0001F9DB\u200D\u2640\uFE0F*¿Qué es VTES?*\U0001F9DB\u200D\u2642\uFE0F \n"
             "  \- Es un juego de cartas ambientado en el mundo de tinieblas de Vampiro La Mascarada\n"
             "  \- Sin embargo, *no es un TCG*, y *no existen los sobres* ni la obligación de comprar cartas \(se aceptan proxies\)\n"
             "  \- En los torneos es el organizador quien permite o no los proxies, la inmensa mayoría *si los permiten*\n\n"
             "[Nociones básicas](https://www.youtube.com/watch?v=velKoYv3LXM)",
        parse_mode='MarkdownV2'
    )


async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    urls = [
        "[Reglas](https://www.blackchantry.com/utilities/rulebook/)",
        "[Generador de mazos y libreria de mazos y cartas](https://vtesdecks.com/)",
        "[Generador de proxies](https://bloodlibrary.info/)"
    ]
    for u in urls:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=u,
            parse_mode='MarkdownV2'
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


async def places(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages: list[Message] = [
        Message("*Este es el sitio principal donde jugamos* \n[La Guarida](https://maps.app.goo.gl/fJwDA4GjuADvv5AZA)"),
        Message("Estos son otros lugares donde también se organizan partidas \n[Bar Capote]("
                "https://maps.app.goo.gl/xqMDLUYURoWemcio7) \n[Kingdom Wargames]("
                "https://maps.app.goo.gl/Vb5rikSvvvVEhrGy9)", True),
    ]
    for m in messages:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=m.text,
            parse_mode='MarkdownV2',
            disable_web_page_preview=m.preview
        )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Si tienes alguna duda que yo no pueda resolver, puedes escribir a @Yogurmeyer o "
             "vteslaguarida@gmail\.com que estará encantado de ayudarte en todo \U0001F601",
        parse_mode='MarkdownV2'
    )


async def event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="\U0001F9DB\u200D\u2640\uFE0F¡¡Noche de los primogénitos\!\!\U0001F9DB\u200D\u2642\uFE0F \n\nQueremos "
             "anunciar que el día *22 de Octubre a las 17:00* organizamos un evento en *La"
             "Guarida* para las personas que quieran *probar VTES y aprender a jugar* \n\nNo será necesario que "
             "traigáis mazos, nosotros pondremos los nuestros\. Si alguien quiere traer el suyo que tenga en cuenta "
             "que para este día sólo se permiten mazos preconstruidos básicos, para que todos los jugadores tengan "
             "las mismas oportunidades de aprender y pasarlo bien \n\nEn cada una de las mesas habrá un integrante "
             "del Círculo Interior para explicar el juego y resolver dudas según avanza la partida \n\nSi queréis "
             "apuntaros, escribid un mensaje a @Yogurmeyer \(apuntaros si estáis seguros, ya que para jugar hay que "
             "formar mesas de 4 o 5 jugadores y hay que reservar mesas\) \n\n¡¡¡Os esperamos en La Guarida\!\!\!",
        parse_mode='MarkdownV2'
    )


if __name__ == '__main__':
    load_dotenv()
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('vtes', vtes))
    application.add_handler(CommandHandler('enlaces', links))
    application.add_handler(CommandHandler('consultar_carta', get_card, has_args=True))
    application.add_handler(CommandHandler('lugares', places, ))
    application.add_handler(CommandHandler('contacto', contact, ))
    application.add_handler(CommandHandler('evento_destacado', event, ))

    application.run_polling()
