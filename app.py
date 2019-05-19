from flask import Flask
from flask import render_template
from flask import request
from flask_cors import CORS
import json
from UserControl import login, register, find, editInfo, changePassword
from PaperControl import purchase, download
from ResourceControl import comment, findComment
from ScholarControl import editScholarInfo, authenticate, manageResource
from SearchControl import searchPaper
from CollectionControl import subscribe, manageCollection, collectPaper
import pymongo
import time

myclient = pymongo.MongoClient('mongodb://106.14.150.33:27017')
mydb = myclient["test"]
logcol = mydb['requestLog']


app = Flask(__name__)
CORS(app, supports_credentials=True)

PORT = 5015


def write_log(data, ans):
    log = {'time': time.time(), 'data': data, 'ans': ans}
    logcol.insert_one(log)


def error(e):
    dic = {
        "code": 0,
        "msg": e,
        "data": {
        }
    }
    return dic


@app.route("/")
def show_web():
    return render_template('main.html')


@app.route("/api/user/login", methods=['POST'])
def user_login():
    data = json.loads(request.data)
    try:
        code = 100
        userID = login(username=data['username'], password=data['password'])
        if not userID or userID == 0:
            code = 111
        if userID == -100:
            code = 112
        elif userID == -200:
            code = 113
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "userID": userID,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/user/register", methods=['POST'])
def user_register():
    data = json.loads(request.data)
    try:
        code = 100
        userID = register(username=data['username'], password=data['password'], email=data['email'])
        if userID == 0:
            code = 104
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "userID": userID,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/user/find", methods=['POST'])
def user_find():
    data = json.loads(request.data)
    try:
        code = 100
        user = find(userID=data['userID'])
        if not user:
            code = 105
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "user": user,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/user/edit_info", methods=['POST'])
def user_edit_info():
    data = json.loads(request.data)
    try:
        code = 100
        flag = editInfo(userID=data['userID'], introduction=data['introduction'], organization=data['organization'])
        if not flag:
            code = 106
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/user/change_pwd", methods=['POST'])
def user_change_pwd():
    data = json.loads(request.data)
    try:
        code = 100
        flag = changePassword(userID=data['userID'], oldPassword=data['oldPassword'], newPassword='oldPassword')
        if not flag:
            code = 107
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/paper/purchase", methods=['POST'])
def paper_purchase():
    data = json.loads(request.data)
    try:
        code = 100
        flag = purchase(userID=data['userID'], paperID=data['paperID'])
        if not flag:
            code = 201
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/user/downloads", methods=['POST'])
def user_downloads():
    data = json.loads(request.data)
    try:
        code = 100
        url = download(paperID=data['paperID'])
        if not url:
            code = 202
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "url": url,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/resource/comment", methods=['POST'])
def resource_comment():
    data = json.loads(request.data)
    try:
        code = 100
        flag = comment(userID=data['userID'], resourceID=data['resourceID'], content=data['content'])
        if not flag:
            code = 301
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/resource/get_comment", methods=['POST'])
def resource_get_comment():
    data = json.loads(request.data)
    try:
        code = 100
        result = findComment(resourceID=data['resourceID'])
        if not result:
            code = 302
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "result": result,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/scholar/edit", methods=['POST'])
def scholar_edit():
    data = json.loads(request.data)
    try:
        code = 100
        flag = editScholarInfo(scholarID=data['scholarID'], name=data['name'], organization=data['organization'], resourceField=data['resourceField'])
        if not flag:
            code = 401
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception as e:
        ans = error(e)

    return json.dumps(ans)


@app.route("/api/scholar/auth", methods=['POST'])
def scholar_auth():
    data = json.loads(request.data)
    try:
        code = 100
        flag = authenticate(userID=data['userID'], email=data['email'])
        if not flag:
            code = 402
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


'''
@app.route("/api/scholar/manage", methods=['POST'])
def scholar_manage():
    data = json.loads(request.data)
    try:
        code = 100
        flag = manageResource(resourceID=data['resourceID'], cmd=data['cmd'], newPrice=data['newPrice'])
        if not flag:
            code = 403
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)
'''


@app.route("/api/search/paper", methods=['POST'])
def search_paper():
    data = json.loads(request.data)
    try:
        code = 100
        result = searchPaper(data['keyword'])
        if not data:
            code = 501
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "result": result
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/collection/subscribe", methods=['POST'])
def collection_subscribe():
    data = json.loads(request.data)
    try:
        code = 100
        flag = subscribe(userID=data['userID'], scholarID=data['scholarID'], cmd=data['cmd'])
        if not flag:
            code = 601
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/collection/paper", methods=['POST'])
def collection_paper():
    data = json.loads(request.data)
    try:
        code = 100
        flag = collectPaper(userID=data['userID'], paperListID=data['paperListID'], cmd=data['cmd'], paperID=data['paperID'])
        if not flag:
            code = 602
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)


@app.route("/api/collection/manage", methods=['POST'])
def collection_manage():
    data = json.loads(request.data)
    try:
        code = 100
        flag = manageCollection(userID=data['userID'], paperListID=data['paperListID'], cmd=data['cmd'], name=data['name'])
        if not flag:
            code = 603
        ans = {
            "code": code,
            "msg": "OK",
            "data": {
                "flag": flag,
            }
        }
    except Exception as e:
        ans = error(e)

    write_log(data, ans)

    return json.dumps(ans)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
