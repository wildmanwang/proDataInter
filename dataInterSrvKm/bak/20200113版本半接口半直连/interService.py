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
from flask import Flask, request
from interConfig import Settings
from interData import InterData
from myTools import MyJSONEncoder

sett = Settings()
data = InterData(sett)
server = Flask(__name__)

@server.route('/hello', methods=['get', 'post'])
def home():
    return "这里是云蝶餐饮数据服务接口"

@server.route('/test', methods=['post'])
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
    print(request.form)
    print(request.args)
    print(request.values)
    print(request.form.to_dict())
    for i in request.form.to_dict():
        print(json.loads(i, encoding="utf-8")["dataType"])
    rtnData["entities"]["test"].append(("001", "张三", "女"))
    rtnData["entities"]["test"].append(("002", "李四", "女"))
    rtnData["entities"]["test"].append(("003", "王五", "男"))

    return json.dumps(rtnData, ensure_ascii=False)

@server.route('/login', methods=['post'])
def login():
    """
    登录
    :return:
    """
    para = request.get_data()
    para = json.loads(para, encoding="utf-8")
    rtn = data.userLogin(para)

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/basicData', methods=['get'])
def basicDataGet():
    """
    获取基础资料
    :return:
    """
    sType = request.args.get("dataType").strip()
    rtn = data.basicDataGet(sType)

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/basicDataFoodPic', methods=['get'])
def basicDataFoodPic():
    """
    获取菜品图片
    :return:
    """
    foodID = request.args.get("foodID").strip()
    rtn = data.basicDataFoodPic(foodID)

    return rtn

@server.route('/tableStatus', methods=['get'])
def busiTableStatus():
    """
    获取桌台状态
    :return:
    """
    tableNo = request.args.get("tableNo").strip()
    rtn = data.busiTableStatus(tableNo)

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/busiData/billOpen', methods=['post'])
def busiBillOpen():
    """
    开台
    :return:
    """
    para = request.get_data()
    para = json.loads(para, encoding="utf-8")
    if not sett.bLogin:
        rtn = data.userLogin({})
        if rtn["result"]:
            sett.bLogin = True
    if sett.bLogin:
       rtn = data.busiBillOpen(para)

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/busiData/billPut', methods=['post'])
def busiBillPut():
    """
    提交单据
    :return:
    """
    para = request.get_data()
    para = json.loads(para, encoding="utf-8")
    if not sett.bLogin:
        rtn = data.userLogin({})
        if rtn["result"]:
            sett.bLogin = True
    if sett.bLogin:
        rtn = data.busiBillPut(para)

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/busiData/billGet', methods=['get'])
def busiBillGet():
    """
    查询单据
    :return:
    """
    billID = request.args.get("billID").strip()
    rtn = data.busiBillGet(billID)

    return json.dumps(rtn, cls=MyJSONEncoder, ensure_ascii=False)

@server.route('/busiData/settleCode', methods=['get'])
def busiSettleCode():
    """
    查询桌台结帐二维码
    :return:
    """
    tableID = request.args.get("tableID").strip()
    rtn = data.busiSettleCode(tableID)

    return rtn

if __name__ == '__main__':
    server.run(host=sett.webHost, port=sett.webPort, debug=True)
