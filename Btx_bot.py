import logging

import telegram
from telegram.ext import Updater, Filters
from telegram.ext import Handler
from telegram.ext import CommandHandler, MessageHandler

import requests

import json

from decorators import send_typing_action
import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class BtxBot():
    START_WITHOUT_AUTH_MESSAGE = """
Для работы со мной, вам необходимо авторизироваться
в битрикс24, для этого перейдите по ссылке <a href=':href'>войти</a>
    """

    def __init__(self, *args, **kwargs):
        self.updater = Updater(token=settings.BOT_TOKEN)
        self.dp = self.updater.dispatcher
        

        start_handler = CommandHandler('start', self.handle_start)
        profile_handler = CommandHandler('профиль', self.get_profile_info)
        add_task_hadnler = CommandHandler('добавить_задачу', self.add_task, pass_args=True)
        unknown_handler = (MessageHandler(Filters.command, self.unknown))
    
        self.dp.add_handler(add_task_hadnler)
        self.dp.add_handler(profile_handler)
        self.dp.add_handler(start_handler)
        self.dp.add_handler(unknown_handler)

        self.dp.add_error_handler(self.error)

    def handle_start(self, bot, update):
        text = self.START_WITHOUT_AUTH_MESSAGE.replace(':href', self.bx24.resolve_authorize_endpoint(**{"state": update.message.chat_id}))
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text=text,
            parse_mode=telegram.ParseMode.HTML
        )

    def get_tokens(self, chat_id):
        self.updater.bot.sendMessage(chat_id, text='Вы успешно залогинились!')
    
    def add_task(self, bot, update, args):
        action_response = requests.post('http://127.0.0.1:1122/task', data=json.dumps({'title': args[0:]}))

    def get_profile_info(self, bot, update):
        user_info = requests.get('http://127.0.0.1:1122/profile').json()
        bot.sendMessage(update.message.chat_id, text=f"Вас зовут {user_info.get('NAME')}")

    def unknown(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Моя тебя не понимать")

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def run(self):
        self.updater.start_webhook(
            listen='127.0.0.1',
            port=9099,
            url_path=settings.BOT_TOKEN
        )

        self.updater.bot.set_webhook(f"https://d80c79ad.ngrok.io/{settings.BOT_TOKEN}")
        self.updater.idle()

btx_bot = BtxBot()

if (__name__ == "__main__"):
    btx_bot.run()
