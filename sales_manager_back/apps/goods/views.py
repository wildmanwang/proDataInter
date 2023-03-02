from apps.goods import goods, control
from apps import sett
from flask import request, jsonify
import json
from flask_login import login_required

ctl = control.ctl_goods(sett)


@goods.route("/", methods=["get", "post"])
def hello():
    return "hello:blueprint for goods"


@goods.route('/basicDataList', methods=['get'])
@login_required
def basicDataList():
    """
    获取基础资料
    :return:
    """
    sType = request.args.get("dataType").strip()
    sQuery = request.args.get("query").strip()
    sPage = request.args.get("page").strip()
    rtn = ctl.basicDataList(sType, sQuery, sPage)
    if rtn["result"]:
        rtnFront = {
            "code": 20000,
            "data": {
                "total": rtn["dataNumber"],
                "items": rtn["entities"][sType]
            }
        }
    else:
        rtnFront = {
            "code": 50006,
            "message": rtn["info"]
        }

    return jsonify(rtnFront)


@goods.route('/basicDataDelete', methods=['post'])
@login_required
def basicDataDelete():
    """
    删除基础资料
    """
    sPara = request.get_data()
    para = json.loads(sPara)
    sType = para["dataType"]
    iID = para["id"]
    rtn = ctl.basicDataDelete(sType, iID)
    if rtn["result"]:
        rtnFront = {
            "code": 20000,
            "data": rtn
        }
    else:
        rtnFront = {
            "code": 50006,
            "message": rtn["info"]
        }

    return jsonify(rtnFront)


@goods.route('/basicDataNew', methods=['post'])
@login_required
def basicDataNew():
    """
    新增基础资料
    """
    sPara = request.get_data()
    para = json.loads(sPara)
    sType = para["dataType"]
    para = para["data"]
    rtn = ctl.basicDataNew(sType, para)
    if rtn["result"]:
        rtnFront = {
            "code": 20000,
            "data": rtn
        }
    else:
        rtnFront = {
            "code": 50006,
            "message": rtn["info"]
        }

    return jsonify(rtnFront)


@goods.route('/basicDataModify', methods=['post'])
@login_required
def basicDataModify():
    """
    修改基础资料
    """
    sPara = request.get_data()
    para = json.loads(sPara)
    sType = para["dataType"]
    para = para["data"]
    rtn = ctl.basicDataModify(sType, para)
    if rtn["result"]:
        rtnFront = {
            "code": 20000,
            "data": rtn
        }
    else:
        rtnFront = {
            "code": 50006,
            "message": rtn["info"]
        }

    return jsonify(rtnFront)
