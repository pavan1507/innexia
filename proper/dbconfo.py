import os

class Config(object):  
   
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "PATRICIA_ROBOT")
    # Leave this defualt
    SESSION_NAME = os.environ.get("SESSION_NAME", "JV_CaptchaBot")
    # get it from https://cloud.mongodb.com 
    API_TOKEN = os.environ.get("API_TOKEN", None)
    # Sudo users(goto @JVToolsBot and send /id to get your id)
   
