from functools import wraps
from telegram import ChatAction

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(bot, update, *args, **kwargs):
        bot.sendChatAction(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(bot, update,  *args, **kwargs)

    return command_func
