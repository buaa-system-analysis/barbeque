from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_cors import CORS
import sys
import json
import os.path
from UserControl import login, register, findUser, editInfo, changePassword
from PaperControl import purchase, download
from ResourceControl import comment
from ScholarControl import editScholarInfo, authenticate, manageResource
from SearchControl import search
from CollectionControl import subscribe, manageCollection, collectPaper


app = Flask(__name__)
CORS(app, supports_credentials=True)

PORT = 5015


def error():
    dic = {
        "code": 0,  # 状态码
        "msg": "ERROR",
        "data": {
        }
    }
    return dic


@app.route("/")
def show_web():
    return render_template('main.html')


@app.route("/api/user/login", methods=['POST'])
def user_login():
    data = request.form
    try:
        code = 100
        userID = login(username=data['username'], password=data['password'])
        if not userID or userID == 0:  # 其他错误
            code = 111
        if userID == -100:  # 未找到用户名
            code = 112
        elif userID == -200:  # 密码错误
            code = 113
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "userID": userID,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/user/register", methods=['POST'])
def user_register():
    data = request.form
    try:
        code = 100
        userID = register(username=data['username'], password=data['password'], email=data['email'])
        if userID == 0:  # 注册失败
            code = 104
        if userID == -100:  # 未找到用户名
            code = 102
        elif userID == -200:  # 密码错误
            code = 103
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "userID": userID,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
