from admin import admin, control
from interService import engine
from flask import request, jsonify
import json

ctl = control.ctl_admin(engine)


@admin.route("/", methods=["get", "post"])
def hello():
    return "hello:blueprint for admin"


@admin.route('/login', methods=['post'])
def user_login():
    """
    登录
    """
    rtn = ctl.user_login("0001", "123456")
    rtnFront = {
        "code": 20000,
        "data": rtn["entities"]
    }

    return jsonify(rtnFront)


@admin.route('/userinfo', methods=['get'])
def user_info():
    """
    登录
    """
    sToken = request.args.get("token").strip()
    rtn = ctl.user_info(sToken)
    rtnFront = {
        "code": 20000,
        "data": rtn["entities"]
    }

    return jsonify(rtnFront)


@admin.route('/logout', methods=['post'])
def user_logout():
    """
    登出
    """
    rtn = ctl.user_logout()
    rtnFront = {
        "code": 20000,
        "data": rtn["entities"]
    }

    return jsonify(rtnFront)
