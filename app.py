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
from UserControl import login, register, find, editInfo, changePassword
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


@app.route("/api/user/find", methods=['POST'])
def user_find():
    data = request.form
    try:
        code = 100
        user = find(userID=data['userID'])
        if not user:
            code = 105
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "user": user,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/user/edit_info", methods=['POST'])
def user_edit_info():
    data = request.form
    try:
        code = 100
        flag = editInfo(userID=data['userID'], introduction=data['introduction'], organization=data['organization'])
        if not flag:
            code = 106
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/user/change_pwd", methods=['POST'])
def user_change_pwd():
    data = request.form
    try:
        code = 100
        flag = changePassword(userID=data['userID'], oldPassword=data['oldPassword'], newPassword='oldPassword')
        if not flag:
            code = 107
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/paper/purchase", methods=['POST'])
def paper_purchase():
    data = request.form
    try:
        code = 100
        flag = purchase(userID=data['userID'], paperID=data['paperID'])
        if not flag:
            code = 201
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/user/download", methods=['POST'])
def user_download():
    data = request.form
    try:
        code = 100
        url = download(paperID=data['paperID'])
        if not url:
            code = 202
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "url": url,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/resource/comment", methods=['POST'])
def resource_comment():
    data = request.form
    try:
        code = 100
        flag = comment(userID=data['userID'], resourceID=data['resourceID'], content=data['content'])
        if not flag:
            code = 301
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/scholar/edit", methods=['POST'])
def scholar_edit():
    data = request.form
    try:
        code = 100
        flag = editScholarInfo(scholarID=data['scholarID'], name=data['name'], organization=data['organization'], resourceField=data['resourceField'])
        if not flag:
            code = 401
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/scholar/auth", methods=['POST'])
def scholar_auth():
    data = request.form
    try:
        code = 100
        flag = authenticate(userID=data['userID'], email=data['email'])
        if not flag:
            code = 402
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/scholar/manage", methods=['POST'])
def scholar_manage():
    data = request.form
    try:
        code = 100
        flag = manageResource(resourceID=data['resourceID'], cmd=data['cmd'], newPrice=data['newPrice'])
        if not flag:
            code = 403
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/search/search", methods=['POST'])
def search_search():
    data = request.form
    try:
        code = 100
        list = search(category=data['category'], keyword=data['keyword'])
        if not list:
            code = 501
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "list": list,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/collection/subscribe", methods=['POST'])
def collection_subscribe():
    data = request.form
    try:
        code = 100
        flag = subscribe(userID=data['userID'], scholarID=data['scholarID'], cmd=data['cmd'])
        if not flag:
            code = 601
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/collection/paper", methods=['POST'])
def collection_paper():
    data = request.form
    try:
        code = 100
        flag = collectPaper(userID=data['userID'], paperListID=data['paperListID'], cmd=data['cmd'], paperID=data['paperID'])
        if not flag:
            code = 602
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)


@app.route("/api/collection/manage", methods=['POST'])
def collection_manage():
    data = request.form
    try:
        code = 100
        flag = manageCollection(userID=data['userID'], paperListID=data['paperListID'], cmd=data['cmd'], name=data['name'])
        if not flag:
            code = 603
        ans = {
            "code": code,  # 状态码
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception:
        ans = error()

    return json.dumps(ans)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
