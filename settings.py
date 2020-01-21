import os
from dotenv import load_dotenv

from eventhub_utils import env

import bottle 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(BASE_DIR,"static")

dot_env = os.path.join(BASE_DIR, ".env")
if os.path.exists(dot_env) :
    load_dotenv(dotenv_path=dot_env)

DEBUG = env("DEBUG",False)
HOST = env("HOST",'0.0.0.0')
PORT = env("PORT",8080)


app = bottle.Bottle()
