import vk_api
from credentials import vk_token
import random


def vk_notify(msg, receive):
       req = {"user_id": receive, 
              "random_id": round(random.random() * 100),
              "message": msg}
       session = vk_api.VkApi(token=vk_token)
       try:
              something = session.method("messages.send", req)
              return something
       except:
              return 0
