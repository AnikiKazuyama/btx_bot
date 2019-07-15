import logging

from telegram.ext import Updater, Filters
from telegram.ext import Handler
from telegram.ext import CommandHandler, MessageHandler

import requests

from decorators import send_typing_action
import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class CatBot():
    def __init__(self, *args, **kwargs):
        self.updater = Updater(token=settings.BOT_TOKEN)
        self.dp = self.updater.dispatcher

        start_handler = CommandHandler('start', self.handle_start)
        meow_handler = CommandHandler('meow', self.handle_meow)
        unknown_handler = (MessageHandler(Filters.command, self.unknown))

        self.dp.add_handler(start_handler)
        self.dp.add_handler(meow_handler)
        self.dp.add_handler(unknown_handler)

        self.dp.add_error_handler(self.error)

    def handle_start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text='Use /meow comand and see what will happened')
    
    def handle_meow(self, bot, update):
        response = requests.get('https://api.thecatapi.com/v1/images/search?limit=1&order=Random').json()

        try:
            cat = response[0]
            bot.send_photo(chat_id=update.message.chat_id, photo=cat.get('url'))
        except:
            bot.sendMessage(chat_id=update.message.chat_id, text='Что-то пошло не так =(')
    
    def unknown(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def run(self):
        self.updater.start_webhook(
            listen='127.0.0.1',
            port=9099,
            url_path=settings.BOT_TOKEN
        )

        self.updater.bot.set_webhook(f"https://8a81688c.ngrok.io/{settings.BOT_TOKEN}")
        self.updater.idle()

if (__name__ == "__main__"):
    cat_bot = CatBot()

    cat_bot.run()
