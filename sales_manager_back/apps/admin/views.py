from apps.admin import admin, control
from apps import sett
from flask import request, jsonify, current_app
import json

ctl = control.ctl_admin(sett)


@admin.route("/", methods=["get", "post"])
def hello():
    return "hello:blueprint for admin"


@admin.route('/login', methods=['post'])
def user_login():
    """
    登录
    """
    sPara = request.get_data()
    para = json.loads(sPara)
    rtn = ctl.user_login(para["username"], para["password"])
    if rtn["result"]:
        rtnFront = {
            "code": 20000,
            "data": rtn["dataObject"],
            "message": "登录成功"
        }
    else:
        rtnFront = {
            "code": 60006,
            "message": rtn["info"]
        }

    return jsonify(rtnFront)


@admin.route('/userinfo', methods=['get'])
def user_info():
    """
    登录
    """
    print(request.args)
    sToken = request.args.get("token").strip()
    rtn = ctl.user_info(sToken)
    if rtn["result"]:
        rtnFront = {
            "code": 20000,
            "data": rtn["dataObject"]
        }
    else:
        rtnFront = {
            "code": 50006,
            "message": rtn["info"]
        }

    return jsonify(rtnFront)


@admin.route('/logout', methods=['post'])
def user_logout():
    """
    登出
    """
    rtn = ctl.user_logout()
    if rtn["result"]:
        rtnFront = {
            "code": 20000,
            "data": rtn["dataObject"]
        }
    else:
        rtnFront = {
            "code": 50006,
            "message": rtn["info"]
        }

    return jsonify(rtnFront)
