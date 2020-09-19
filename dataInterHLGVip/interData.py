# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from interMssql import MSSQL
import datetime, time
import os
from myTools import MyJSONEncoder
import json


class InterData():
    def __init__(self, sett):
        self.sett = sett
        self.db = MSSQL(self.sett.serverHost, self.sett.serverUser, self.sett.serverPwd, self.sett.serverDb)


    def securityVerify(self, headers, parab):
        import hashlib
        rtnData = {
            "status": 0,
            "message": ""
        }
        try:
            # 安全校验
            paras = {}
            if "appid" in headers:
                paras["appid"] = headers["appid"]
            else:
                raise Exception("请提供请求appid")
            if "timestamp" in headers:
                paras["timestamp"] = headers["timestamp"]
            else:
                raise Exception("请提供请求时间戳timestamp")
            if "sign" in headers:
                sSign1 = headers["sign"]
            else:
                raise Exception("请提供验证签名sign")
            if paras["appid"] == "inter_km_HLGVip":
                sSecret = "km200915"
            else:
                raise Exception("appid错误")
            iTimestamp = int(time.time())
            if abs(iTimestamp - int(paras["timestamp"])) > 5 * 60:
                raise Exception("请求时间与服务器时间不一致")
            # 生成签名
            paras.update(parab)
            lPara = sorted(paras.items(), key=lambda x:x[0])
            sSource = sSecret
            for gitem in lPara:
                sSource += str(gitem[0]) + str(gitem[1])
            sSource += sSecret
            sSign2 = hashlib.md5(sSource.encode(encoding='UTF-8')).hexdigest()
            if sSign2 != sSign1:
                self.sett.logger.error("时间：{timestr}，参数字符串：{paras}，签名：{sign}".format(
                    timestr=datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),
                    paras=sSource,
                    sign=sSign2)
                )
                raise Exception("签名验证失败")
            rtnData["status"] = 1
        except Exception as e:
            self.sett.logger.error(str(e))
            rtnData["message"] = str(e)
        return rtnData


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
            lsSql = r"select count(*) from Vip where Id='{vipId}'".format(vipId=data["Id"])
            cur.execute(lsSql)
            rsTmp = cur.fetchall()
            if rsTmp[0][0] == 0:
                data["validEndTime"] = "2099-08-01 23:59:59"        # 有效期由线上生成二维码时判断，线上不会把有效期更新推送到线下
                if len(data["cardNo"]) == 18:
                    if data["cardNo"][6:14].isdigit():
                        sBirthday = data["cardNo"][6:10] + "-" + data["cardNo"][10:12] + "-" + data["cardNo"][12:14] + " 00:00:00.000"
                    else:
                        sBirthday = '1990-01-01 00:00:00.000'
                else:
                    sBirthday = '1990-01-01 00:00:00.000'
                lsSql = r"insert into Vip ( Id, VipClsId, CardFlag, OriginalId, IdentityCardId, Status, BeginDate, EndDate, BranchId, SendDate, Name, Sex, Mobile, Email, Birthday, Deposit, Dues, TotalConsTimes, TotalConsAmt, TotalIntegral, Integral, RechargingAmt, Balance, EncryptBalance, IntegralFlag, OperId, OperDate, SendMan, CardSendFlag, BackFlag, CardMakeFlag, IsSync ) " \
                        r"values ( '{vipId}', '{VipClsId}', 'O', '{vipId}', '{IdentityCardId}', '0', '{BeginDate}', '{EndDate}', '{branchno}', '{sDate}', '{vipName}', '男', '{Mobile}', '{Mobile}', '{Birthday}', 0.00, 0.00, 0, 0.00, 0.00, 0.00, 0.00, 0.00, 'CJ;=D538CL;=', '1', '0000', '{sDate}', '0000', '1', '1', '1', '1' )" \
                        r"".format(
                    vipId=data["Id"],
                    VipClsId=self.sett.vipClass,
                    Mobile=data["Phone"],
                    Birthday=sBirthday,
                    IdentityCardId=data["cardNo"],
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
            lsSql = r"update Vip set Mobile='{Qrcode}' where Id='{vipId}'".format(
                vipId=data["Id"],
                Qrcode=data["Qrcode"]
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
                lsSql = r"select '{title}', CardCost, operDate, ActualPayamt from VipCostList " \
                        r"where CardId = '{cardId}' and convert(char(10), OperDate, 120) between '{startDate}' and '{endDate}' " \
                        r"and CardWay in ('充值','消费','退单','预扣','预扣还款','设定金额','挂账付款')".format(
                    title=self.sett.rptTitle,
                    cardId=data["Id"],
                    startDate=data["startDate"],
                    endDate=data["endDate"]
                )
                lsSql = r"select '{title}', master.FoodAmt, master.SettleTime, master.FoodAmt - master.PayAmt from foodbill master, FoodBillEntity detail " \
                        r"where master.NewBillId = detail.NewBillId and master.VipId = '{cardId}' " \
                        r"and CONVERT(char(10), master.Business, 120) between '{startDate}' and '{endDate}'".format(
                    title=self.sett.rptTitle,
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
