from telegram_bot_api import Pooling, API, Update, MessageEntityType, get_entities_by_type, MessageBuilder

BOT_NAME = "Test Bot"
api = API(token="5645950598:AAFHHrryA15O4X4lADJeu-IMfHYrxuP_Aes")


def handler(update: Update):
	# this bot support only messages
	if not update.message:
		return
	msg = update.message

	# this bot support only messages, contains "/". /help for example
	commands = get_entities_by_type(msg, MessageEntityType.BOT_COMMAND)

    

	for command in commands:

		if command == "/help":
			api.send_message(msg.chat.id, f'{commands} is a /help message for {BOT_NAME}.')
			return
		if command == "/start":
			user = msg.from_user
			user_name = user.username or user.first_name or user.last_name
			api.send_message(msg.chat.id, f'{commands} /start command processed by {BOT_NAME} for {user_name}.')
			return
    
	repl = MessageBuilder()
	repl.append("he")
	repl.append("llo")

	api.send_message(msg.chat.id,  repl.get())


pooling = Pooling(api, handler, 1).start()