# -*- coding:utf-8 -*-
"""
flask框架实现数据接口服务
数据返回格式：
rtnData = {
    "result":True,                  # 逻辑控制 True/False
    "dataString":"",               # 字符串
    "dataNumber":1,                # 数字
    "info":"",                      # 信息
    "entities": {                   # 表体集
        "bill":[],                   # 销售单
        "billItem":[],               # 销售单
        "billPay":[]                 # 销售单
    }
}
"""
__author__ = "Cliff.wang"
import json
from flask import Flask, request, jsonify
import config
from ormOper import OrmOper

sett = config.DevelopmentConfig()
orm = OrmOper(sett)
app = Flask(__name__)
app.config.from_object(sett)

@app.route('/hello', methods=['get', 'post'])
def home():
    return "这里是石将军数据服务接口"

@app.route('/orm_test', methods=['get', 'post'])
def orm_test():
    sType = "category"
    para = {"id": 46, "name": "哈哈哈", "order_num": 22, "status": 1, "remark": "2222"}
    rtn = orm.basicDataModify(sType, para)

    return rtn["info"]

@app.route('/test', methods=['post'])
def test():
    """
    :return:
    """
    rtnData = {
        "result": True,     # 逻辑控制 True/False
        "dataString": "",   # 字符串
        "dataNumber": 1,    # 数字
        "info": "",         # 信息
        "entities": {       # 表体集
            "test": []  # 销售单
        }
    }
    print(request.get_data())
    # print(request.form) 
    # print(request.args)
    # print(request.values)
    # print(request.form.to_dict())
    for i in request.form.to_dict():
        print(json.loads(i, encoding="utf-8")["dataType"])
    rtnData["entities"]["test"].append(("001", "张三", "女"))
    rtnData["entities"]["test"].append(("002", "李四", "女"))
    rtnData["entities"]["test"].append(("003", "王五", "男"))

    return jsonify(rtnData)

@app.route( '/user/login', methods=['post'])
def user_login():
    """
    登录
    """
    print("**request.url:{con}".format(con=request.url))
    print("**request.form:{con}".format(con=request.form))
    rtn = orm.user_login("0001", "123456")
    rtnFront = {
        "code": 20000,
        "data": rtn["entities"]
    }

    return jsonify(rtnFront)

@app.route( '/user/info', methods=['get'])
def user_info():
    """
    登录
    """
    sToken = request.args.get("token").strip()
    rtn = orm.user_info(sToken)
    rtnFront = {
        "code": 20000,
        "data": rtn["entities"]
    }

    return jsonify(rtnFront)

@app.route( '/user/logout', methods=['post'])
def user_logout():
    """
    登出
    """
    rtn = orm.user_logout()
    rtnFront = {
        "code": 20000,
        "data": rtn["entities"]
    }

    return jsonify(rtnFront)

@app.route('/basicDataList', methods=['get'])
def basicDataList():
    """
    获取基础资料
    :return:
    """
    sType = request.args.get("dataType").strip()
    sQuery = request.args.get("query").strip()
    sPage = request.args.get("page").strip()
    rtn = orm.basicDataList(sType, sQuery, sPage)
    rtnFront = {
        "code": 20000,
        "data": {
            "total": rtn["dataNumber"],
            "items": rtn["entities"][sType]
        }
    }

    return jsonify(rtnFront)

@app.route('/basicDataDelete', methods=['post'])
def basicDataDelete():
    """
    删除基础资料
    """
    sPara = request.get_data()
    para = json.loads(sPara)
    sType = para["dataType"]
    iID = para["id"]
    rtn = orm.basicDataDelete(sType, iID)
    rtnFront = {
        "code": 20000,
        "data": rtn
    }

    return jsonify(rtnFront)

@app.route('/basicDataNew', methods=['post'])
def basicDataNew():
    """
    新增基础资料
    """
    sPara = request.get_data()
    para = json.loads(sPara)
    sType = para["dataType"]
    para = para["data"]
    rtn = orm.basicDataNew(sType, para)
    rtnFront = {
        "code": 20000,
        "data": rtn
    }

    return jsonify(rtnFront)

@app.route('/basicDataModify', methods=['post'])
def basicDataModify():
    """
    修改基础资料
    """
    sPara = request.get_data()
    para = json.loads(sPara)
    sType = para["dataType"]
    para = para["data"]
    rtn = orm.basicDataModify(sType, para)
    rtnFront = {
        "code": 20000,
        "data": rtn
    }

    return jsonify(rtnFront)

if __name__ == '__main__':
    app.run(host=app.config["WEB_SERVER_HOST"], port=app.config["WEB_SERVER_PORT"], debug=True)
