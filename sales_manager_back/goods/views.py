from goods import goods, control
from backApp import sett
from flask import request, jsonify
import json

ctl = control.ctl_goods(sett)


@goods.route("/", methods=["get", "post"])
def hello():
    return "hello:blueprint for goods"


@goods.route('/basicDataList', methods=['get'])
def basicDataList():
    """
    获取基础资料
    :return:
    """
    sType = request.args.get("dataType").strip()
    sQuery = request.args.get("query").strip()
    sPage = request.args.get("page").strip()
    rtn = ctl.basicDataList(sType, sQuery, sPage)
    rtnFront = {
        "code": 20000,
        "data": {
            "total": rtn["dataNumber"],
            "items": rtn["entities"][sType]
        }
    }

    return jsonify(rtnFront)


@goods.route('/basicDataDelete', methods=['post'])
def basicDataDelete():
    """
    删除基础资料
    """
    sPara = request.get_data()
    para = json.loads(sPara)
    sType = para["dataType"]
    iID = para["id"]
    rtn = ctl.basicDataDelete(sType, iID)
    rtnFront = {
        "code": 20000,
        "data": rtn
    }

    return jsonify(rtnFront)


@goods.route('/basicDataNew', methods=['post'])
def basicDataNew():
    """
    新增基础资料
    """
    sPara = request.get_data()
    para = json.loads(sPara)
    sType = para["dataType"]
    para = para["data"]
    rtn = ctl.basicDataNew(sType, para)
    rtnFront = {
        "code": 20000,
        "data": rtn
    }

    return jsonify(rtnFront)


@goods.route('/basicDataModify', methods=['post'])
def basicDataModify():
    """
    修改基础资料
    """
    sPara = request.get_data()
    para = json.loads(sPara)
    sType = para["dataType"]
    para = para["data"]
    rtn = ctl.basicDataModify(sType, para)
    rtnFront = {
        "code": 20000,
        "data": rtn
    }

    return jsonify(rtnFront)
