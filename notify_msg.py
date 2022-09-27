from vk_file import vk_notify

def notify(receive, username, id_, text):
    msg_vk = f"пользователь под ником {username} \n"
    msg_vk += f"с id - {id_} \n"
    msg_vk += "отправил вам сообщение \n"
    msg_vk += f'"{text}"'
    vk_notify(msg_vk, receive)
