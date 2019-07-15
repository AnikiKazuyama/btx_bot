from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def link_keyboard(url):
    keyboard = [[InlineKeyboardButton(text="Войти", url=url)]]
    return InlineKeyboardMarkup(keyboard)
