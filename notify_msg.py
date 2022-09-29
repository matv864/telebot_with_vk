from vk_file import vk_notify

def notify(receive, username, id_, text):
    msg_vk = f"пользователь под ником {username} \n"
    msg_vk += f"с id - {id_} \n"
    msg_vk += "отправил вам сообщение \n"
    msg_vk += f'"{text}"\n'
    msg_vk += "это сообщение отправил вам этот бот\n"
    msg_vk += "https://t.me/matv864_bot\n"
    return vk_notify(msg_vk, receive)
