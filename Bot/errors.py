def error_handling():
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
    try:
        raise error
    except MethodNotAllowed:
        bot.send_message(update.message.chat_id, text='Вы не авторизованы, пожалуйста авторизируйтесь')
    except BadRequest:
        # handle malformed requests - read more below!
        pass
    except TimedOut:
        # handle slow connection problems
        pass
    except NetworkError:
        bot.send_message(update.message.chat_id, text='С соединением что-то не так, попробуйте еще раз')
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        pass
    except TelegramError:
        # handle all other telegram related errors
        pass