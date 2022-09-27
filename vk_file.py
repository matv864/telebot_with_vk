import vk_api
from credentials import vk_token
import random

# with open("config_example.txt", "r") as F:
#   token = F.readline()



def vk_notify(msg, receive):
    req = {"user_id": receive, 
           "random_id": round(random.random() * 100),
           "message": msg}
    session = vk_api.VkApi(token=vk_token)
    something = session.method("messages.send", req)
    return something
