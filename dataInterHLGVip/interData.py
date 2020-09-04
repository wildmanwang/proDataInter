# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from interMssql import MSSQL
import os
from myTools import MyJSONEncoder
import json


class InterData():
    def __init__(self, sett):
        self.sett = sett
        self.db = MSSQL(self.sett.serverHost, self.sett.serverUser, self.sett.serverPwd, self.sett.serverDb)

    def setVIPInfo(self, data):
        """
        推送会员注册
        """
        rtnData = {
            "status": 0,
            "message": ""
        }

        ibConnected = False
        try:
            conn = self.db.GetConnect()
            ibConnected = True
            cur = conn.cursor()
            if not cur:
                raise Exception("同步会员信息失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb))
            # 存入新表：门店、营业日期、单据号、手机号、积分标志
            lsSql = r"select 1"
            cur.execute(lsSql)
            conn.commit()
            rtnData["status"] = 1
            rtnData["message"] = "ok"
        except Exception as e:
            rtnData["message"] += str(e)
        finally:
            if(ibConnected):
                conn.close()

        return rtnData

    def setVIPCode(self, data):
        """
        推送会员二维码
        """
        rtnData = {
            "status": 0,
            "message": ""
        }

        ibConnected = False
        try:
            conn = self.db.GetConnect()
            ibConnected = True
            cur = conn.cursor()
            if not cur:
                raise Exception("同步会员动态二维码失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb))
            # 存入新表：门店、营业日期、单据号、手机号、积分标志
            lsSql = r"select 1"
            cur.execute(lsSql)
            conn.commit()
            rtnData["status"] = True
            rtnData["message"] = "ok"
        except Exception as e:
            rtnData["message"] += str(e)
        finally:
            if(ibConnected):
                conn.close()

        return rtnData

    def queryBills(self, data):
        """
        查询会员消费记录
        {
            "title":"欢乐谷出口小商店消费",
            "price":100.00,
            "date":"2020-08-01 12:15:12",
            "sale":10.01
        }
        """
        rtnData = {
            "status": 0,
            "message": "",
            "data": []
        }
        ibConnected = False
        try:
            conn = self.db.GetConnect()
            ibConnected = True
            cur = conn.cursor()
            if not cur:
                rtnData["message"] = "查询会员消费失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
            else:
                lsSql = r"select 1"
                cur.execute(lsSql)
                conn.commit()
                rtnData["status"] = True
                rtnData["message"] = "查询会员消费成功"
        except Exception as e:
            rtnData["message"] = str(e)
        finally:
            if (ibConnected):
                conn.close()

        return rtnData

if __name__ == "__main__":
    pass
