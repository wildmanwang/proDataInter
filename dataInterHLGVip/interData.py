# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from interMssql import MSSQL
import datetime
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
            sDate = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
            lsSql = r"insert into Vip ( Id, VipClsId, CardFlag, OriginalId, FlowId, Status, BeginDate, EndDate, BranchId, SendDate, Name, Sex, Mobile, Birthday, Deposit, Dues, TotalConsTimes, TotalConsAmt, TotalIntegral, Integral, RechargingAmt, Balance, EncryptBalance, IntegralFlag, OperId, OperDate, SendMan, CardSendFlag, BackFlag, CardMakeFlag, IsSync ) " \
                    r"values ( '{vipId}', '{VipClsId}', 'O', '{vipId}', '{FlowId}', '0', '{BeginDate}', '{EndDate}', '{branchno}', '{sDate}', '{vipName}', '男', '{Mobile}', '1990-01-01 00:00:00.000', 0.00, 0.00, 0, 0.00, 0.00, 0.00, 0.00, 0.00, 'CJ;=D538CL;=', '1', '0000', '{sDate}', '0000', '1', '1', '1', '1' )" \
                    r"".format(
                vipId=data["Id"],
                VipClsId=self.sett.vipClass,
                Mobile=data["Phone"],
                FlowId=data["cardNo"],
                vipName=data["custName"],
                BeginDate=data["validBegTime"],
                EndDate=data["validEndTime"],
                branchno=self.sett.branchNo,
                sDate=sDate
            )
            cur.execute(lsSql)
            conn.commit()
            rtnData["status"] = 1
            rtnData["message"] = "ok"
        except Exception as e:
            rtnData["message"] = str(e)
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
            lsSql = r"update Vip set OriginalId='{OriginalId}' where Id='{vipId}'".format(
                vipId=data["Id"],
                OriginalId=data["Qrcode"]
            )
            cur.execute(lsSql)
            conn.commit()
            rtnData["status"] = "1"
            rtnData["message"] = "ok"
        except Exception as e:
            rtnData["message"] = str(e)
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
                lsSql = r"select '欢乐谷出口小商店消费', CardCost, operDate, ActualPayamt from VipCostList " \
                        r"where CardId = '{cardId}' and convert(char(10), OperDate, 120) between '{startDate}' and '{endDate}' " \
                        r"and CardWay in ('充值','消费','退单','预扣','预扣还款','设定金额','挂账付款')".format(
                    cardId=data["Id"],
                    startDate=data["startDate"],
                    endDate=data["endDate"]
                )
                ldCol = ["title", "price", "date", "sale"]
                cur.execute(lsSql)
                rsTmp = cur.fetchall()
                rtnData["data"] = [dict(zip(ldCol, line)) for line in rsTmp]
                conn.commit()
                rtnData["status"] = "1"
                rtnData["message"] = "ok"
        except Exception as e:
            rtnData["message"] = str(e)
        finally:
            if (ibConnected):
                conn.close()

        return rtnData

if __name__ == "__main__":
    pass
