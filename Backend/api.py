import functools

from flask import (
    Blueprint, flash, redirect, request, Response, jsonify
)
from werkzeug.exceptions import MethodNotAllowed

bp = Blueprint('api', __name__, url_prefix='/api')

from Bot.Btx_bot import btx_bot
from Common.Btx import bx24

from Backend.constants.urls import REDIRECT_TO_BOT
import settings

# Общие функции

def get_profile_func():
    response = bx24.call_method('user.current')
    if (response.get('error') == 'NO_AUTH_FOUND'):
        raise MethodNotAllowed

    profile_data = response.get('result')

    return profile_data

@bp.route("/login")
def get_code():
    code = request.args.get('code', '')
    chat_id = request.args.get('state', '')
    
    bx24.request_tokens(code)

    btx_bot.sucess_login(chat_id, get_profile_func())
    return redirect(REDIRECT_TO_BOT)

@bp.route("/profile")
def get_profile():
    return jsonify(get_profile_func())

@bp.route("/task", methods=["POST"])
def add_task():
    profile = get_profile_func()

    id = profile.get('ID')
    try:
        title = request.get_json(force=True).get("title")
        response = bx24.call_method('tasks.task.add', {'fields':{'TITLE': title,'RESPONSIBLE_ID': id}})
        return jsonify(response)
    except Exception: 
        return Response(status=400)

@bp.errorhandler(MethodNotAllowed)
def handle_bad_request(e):
    return Response(status=405)