# -*- coding:utf-8 -*-
"""
软件前端的父类
数据操作标准返回值结构：
{
    "result":True/False,            # 逻辑控制
    "dataString":"",                # 字符串
    "dataNumber":0,                 # 数字
    "info":"",                      # 信息
    "entities":{                    # 表体集
        "item":[(                   # 表体代码
                recordNo,           # 记录标识
                recordName          # 记录名称/备注
            )
        ]
    }
}
"""
__author__ = "Cliff.wang"

class BusiProcess():

    def __init__(self, sett):
        """
        实例化
        :param sett: 参数
        :param endType:  接口端型 front:前端 back:后端
        """
        self.sett = sett
        self.interName = "线下端"
        self.interConn = {}
        self.interConn["host"] = self.sett.serverHost
        self.interConn["user"] = self.sett.serverUser
        self.interConn["password"] = self.sett.serverPwd
        self.interConn["database"] = self.sett.serverDb

    def getItems(self, itemNo):
        """
        获取商品列表
        :return:                            # 返回商品数据表
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "item": {                    # 表体代码
                    "Item":[]               # 商品表
                }
            }
        }

        return rtnData

    def putOrders(self, dsOrder):
        """
        写入订单
        :param dsOrder: 新增订单列表
        :return:
        """
        rtnData = {
            "result": True,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 1,  # 数字
            "info": "",  # 信息
            "entities": {}
        }

        return rtnData
