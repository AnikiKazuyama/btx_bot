from flask import Flask, request, Response, redirect, jsonify
from flask_cors import CORS

from Btx_bot import btx_bot
from bitrix24 import Bitrix24

import settings

app = Flask(__name__)
CORS(app)

bx24 = Bitrix24(settings.BTX_DOMAIN, settings.BTX_CLIENT_ID, settings.BTX_SECRET)
        
@app.route("/")
def hello():
    return Response("HI")


@app.route("/login")
def get_code():
    code = request.args.get('code', '')
    chat_id = request.args.get('state', '')
    
    bx24.request_tokens(code)
    btx_bot.get_tokens(chat_id)
    
    return redirect("https://t.me/Bitrix_actions_bot")

def get_profile_func():
    response = bx24.call_method('user.current')

    profile_data = response.get('result')
    return profile_data

@app.route("/profile")
def get_profile():
    return jsonify(get_profile_func())

@app.route("/task", methods=["POST"])
def add_task():
    profile = get_profile_func()

    id = profile.get('ID')
    title = request.get_json(force=True).get("title")
    response = bx24.call_method('tasks.task.add', {'fields':{'TITLE': title,'RESPONSIBLE_ID': id}})

    return jsonify(response)

app.run(host="127.0.0.1", port=1122)

