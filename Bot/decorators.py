from functools import wraps
from telegram.chataction import ChatAction

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(instance, bot, update,  *args, **kwargs):
            bot.send_chat_action(chat_id=update.message.chat_id, action=action)
            return func(instance, bot, update,  *args, **kwargs)
        return command_func
    
    return decorator

send_typing_action = send_action(ChatAction.TYPING)