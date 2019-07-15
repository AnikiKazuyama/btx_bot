import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BTX_HOOK = os.getenv("BTX_HOOK")
BTX_DOMAIN = os.getenv("BTX_DOMAIN")
BTX_CLIENT_ID = os.getenv("BTX_CLIENT_ID")
BTX_SECRET = os.getenv("BTX_SECRET")