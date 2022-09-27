from credentials import bot_token
import telebot
from telebot import types
import json
from notify_msg import notify


hello_message = """вас приветствует транспортёр сообщений
выберите способ отправки сообщения"""

text_for_vk_id = """vk_id"""
text_for_vk_username = """vk_username"""

user_text = ""


with open('new_data.json', 'r') as fp:
        # Чтение файла 'data.json' и преобразование
        # данных JSON в объект Python 
        main_obj = json.load(fp)

bot = telebot.TeleBot(bot_token)

#print(type(main_obj))

for key, it in main_obj.items():
    bot.send_message(it, "я знаю твой айпишник")




@bot.message_handler(content_types = ["text"])
def command_help(message):
    list_of_buttons = types.InlineKeyboardMarkup()
    msg = types.InlineKeyboardButton(text=text_for_vk_id, callback_data="vk_id")
    list_of_buttons.add(msg)
    msg = types.InlineKeyboardButton(text=text_for_vk_username, callback_data="vk_username")
    list_of_buttons.add(msg)



    main_obj[message.from_user.username] = message.from_user.id
    with open("new_data.json", "w") as F:
        json.dump(main_obj, F)


    

    bot.send_message(message.chat.id, "||choose1||", reply_markup=list_of_buttons, timeout=20)
    #bot.send_message(message.chat.username, "||choose2||", reply_markup=list_of_buttons, timeout=20)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "vk_id":
        with open("new_text.txt", "w") as F:
            F.write(str(call))
        sent = bot.send_message(call.from_user.id, "введите сообщение")
        bot.register_next_step_handler(sent, for_user_text)
        msg = "сообщение отправлено"
    elif call.data == "vk_username":
        msg = "данная функция в разработке"
        bot.send_message(call.message.chat.id, msg)

    
def for_user_text(message):
    global user_text
    user_text = message.text
    sent = bot.send_message(message.chat.id, "введите vk_id")
    bot.register_next_step_handler(sent, for_id_receiver)

def for_id_receiver(message):
    vk_receive = message.text.strip()
    if vk_receive.isdigit():
        notify(int(vk_receive), message.from_user.username, str(message.from_user.id), user_text)
        bot.send_message(message.chat.id, "сообщение отправлено")
    else:
        bot.send_message(message.chat.id, "введите действительный vk_id")


#bot.polling(interval=5)
bot.infinity_polling()
