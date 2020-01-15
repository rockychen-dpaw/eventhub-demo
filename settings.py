import os
from dotenv import load_dotenv

from eventhub_utils import env

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dot_env = os.path.join(BASE_DIR, ".env")
if os.path.exists(dot_env) :
    load_dotenv(dotenv_path=dot_env)

DEBUG = env("DEBUG",False)
PORT = env("PORT",8080)
