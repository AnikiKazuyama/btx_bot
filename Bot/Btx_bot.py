import logging

import telegram
from telegram.ext import Updater, Filters
from telegram.ext import Handler
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)

import requests
import json

from Common.Btx import bx24
from Bot.errors import error_handling

from Bot.decorators import send_typing_action
from Bot.keyboards import link_keyboard

import emoji

import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class BtxBot():
    START_WITHOUT_AUTH_MESSAGE = emoji.emojize('Для работы со мной, вам необходимо авторизироваться в битрикс24 :point_down:', use_aliases=True)

    def __init__(self, *args, **kwargs):
        self.updater = Updater(token=settings.BOT_TOKEN)
        self.dp = self.updater.dispatcher

        start_handler = CommandHandler('start', self.handle_start)
        login_handler = CommandHandler('login', self.login)
        profile_handler = CommandHandler('profile', self.get_profile_info)
        add_task_hadnler = CommandHandler('add_task', self.add_task, pass_args=True)
        meow_handler = CommandHandler('meow', self.handle_meow)
        unknown_handler = (MessageHandler(Filters.command, self.unknown))
    
        self.dp.add_handler(start_handler)
        self.dp.add_handler(login_handler)
        self.dp.add_handler(profile_handler)
        self.dp.add_handler(add_task_hadnler)
        self.dp.add_handler(meow_handler)
        self.dp.add_handler(unknown_handler)

        self.dp.add_error_handler(error_handling)

    def handle_start(self, bot, update):
        url = bx24.resolve_authorize_endpoint(**{"state": update.message.chat_id})
        keyboard = link_keyboard(url)

        update.message.reply_text(self.START_WITHOUT_AUTH_MESSAGE, reply_markup=keyboard)

    def login(self, bot, update):
        url = bx24.resolve_authorize_endpoint(**{"state": update.message.chat_id})
        keyboard = link_keyboard(url)

        update.message.reply_text('Войти', reply_markup=keyboard)

    def sucess_login(self, chat_id, profile):
        fullname = f"{profile.get('NAME') or ''} {profile.get('LAST_NAME') or ''}"
        self.updater.bot.send_message(chat_id, text=f'Вы успешно залогинились как {fullname}')
    
    @send_typing_action
    def add_task(self, bot, update, args):
        action_response = requests.post(f'{settings.API_URL}/task', data=json.dumps({'title': args[0:]}))
        
        if (action_response.status_code == 200):
            update.message.reply_text(f"Задача успешно добавлена")
            
        if (action_response.status_code == 405):
            keyboard = link_keyboard(url)
            update.message.reply_text(
                emoji.emojize('Вы не авторизованы, пожалуйста авторизируйтесь :point_down:', use_aliases=True),
                reply_markup=keyboard
            )
    
    @send_typing_action
    def get_profile_info(self, bot, update):
        user_info = requests.get(f'{settings.API_URL}/profile').json()
        update.message.reply_text(f"Вас зовут {user_info.get('NAME')}")

    @send_typing_action
    def handle_meow(self, bot, update):
        response = requests.get(settings.CAT_API).json()

        try:
            cat = response[0]
            update.message.reply_photo(photo=cat.get('url'))
        except:
            update.message.reply_text(text=emoji.emojize('Котейка потерялся по дороге к тебе :cry:', use_aliases=True))
    
    @send_typing_action
    def unknown(self, bot, update):
        update.message.reply_text("Моя тебя не понимать")

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

btx_bot = BtxBot()

if (__name__ == "__main__"):
    btx_bot.run()
