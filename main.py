from credentials import bot_token
import telebot
from telebot import types
import json
from notify_msg import notify


def checking(call):
    return (call.data in ["vk_id", "my_contacts"])


hello_message = """вас приветствует транспортёр сообщений
здесь вы можете отправлять сообщения людям в вк от лица нашего бота
вы можете ооткрыть свои контакты или отправить сообщение по vk_id"""

text_for_vk_id = """vk_id"""
vk_contacts = """мои контакты"""

user_text = ""


with open('new_data.json', 'r') as F:
        username_and_id = json.load(F)

with open('contacts.json', 'r') as F:
        contacts_dict = json.load(F)

bot = telebot.TeleBot(bot_token)

# for key, it in main_obj.items():
#     bot.send_message(it, "я знаю твой айпишник")




@bot.message_handler(content_types = ["text"])
def command_help(message):
    list_of_buttons = types.InlineKeyboardMarkup()
    msg = types.InlineKeyboardButton(text=text_for_vk_id, callback_data="vk_id")
    list_of_buttons.add(msg)
    msg = types.InlineKeyboardButton(text=vk_contacts, callback_data="my_contacts")
    list_of_buttons.add(msg)



    username_and_id[message.from_user.username] = message.from_user.id
    with open("new_data.json", "w") as F:
        json.dump(username_and_id, F, indent="\t")

    if contacts_dict.get(str(message.chat.id), False) == False:
        contacts_dict[str(message.chat.id)] = []
        with open("contacts.json", "w") as F:
            json.dump(contacts_dict, F, indent="\t")



    

    bot.send_message(message.chat.id, hello_message, reply_markup=list_of_buttons)
    #bot.send_message(message.chat.username, "||choose2||", reply_markup=list_of_buttons, timeout=20)

@bot.callback_query_handler(func=checking)
def callback_worker(call):
    if call.data == "vk_id":
        with open("new_text.txt", "w") as F:
            F.write(str(call))
        sent = bot.send_message(call.from_user.id, "введите сообщение")
        bot.register_next_step_handler(sent, for_user_text)
    elif call.data == "my_contacts":
        list_of_buttons = types.InlineKeyboardMarkup()
        temp = contacts_dict.get(str(call.from_user.id))
        if temp:
            for i in temp:
                msg = types.InlineKeyboardButton(text=str(i), callback_data=str(i))
                list_of_buttons.add(msg)
        msg = types.InlineKeyboardButton(text="добавить контакт", callback_data="add_contact")
        list_of_buttons.add(msg)
        bot.send_message(call.from_user.id, "ваши контакты", reply_markup=list_of_buttons)

@bot.callback_query_handler(func=lambda call: True)
def for_choose_from_contacts(call):
    #bot.send_message(call.from_user.id, "good")
    if call.data == "add_contact":
        sent = bot.send_message(call.from_user.id, "введите номер контакта")
        bot.register_next_step_handler(sent, add_contact_from_user)
    elif call.data:
        pass

def add_contact_from_user(message):
    contacts_dict[str(message.from_user.id)].append(message.text)
    with open("contacts.json", "w") as F:
        json.dump(contacts_dict, F, indent="\t")
    bot.send_message(message.chat.id, "контакт добавлен")
    
def for_user_text(message):
    global user_text
    user_text = message.text
    sent = bot.send_message(message.chat.id, "введите vk_id")
    bot.register_next_step_handler(sent, for_id_receiver)

def for_id_receiver(message):
    vk_receive = message.text.strip()
    if vk_receive.isdigit():
        repl = notify(int(vk_receive), message.from_user.username, str(message.from_user.id), user_text)
        if repl:
            bot.send_message(message.chat.id, "сообщение отправлено")
        else:
            bot.send_message(message.chat.id, "сообщение не отправлено")
    else:
        bot.send_message(message.chat.id, "введите действительный vk_id")

def for_contacts_receiver(message):
    pass


#bot.polling(interval=5)
bot.infinity_polling()
