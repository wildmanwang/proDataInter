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
        rtn = self.initDb()
        print(rtn)

    def initDb(self):
        """
        数据库初始化
        """
        rtnData = {
            "result": False,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 0,  # 数字
            "info": "",  # 信息
            "entities": {}
        }

        ibConnected = False
        try:
            # 创建手机号码记录表：自等列、单据号、手机号码、是否已处理
            conn = self.db.GetConnect()
            ibConnected = True
            cur = conn.cursor()
            if not cur:
                raise Exception("初始化失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb))
            lsSql = r"select 1 from sysobjects where id=object_id('tmpPhone')"
            cur.execute(lsSql)
            rsData = cur.fetchall()
            if len(rsData) == 0:
                lsSql = r"CREATE TABLE tmpPhone(" \
                        r"    sID int IDENTITY(1,1) NOT NULL," \
                        r"    sBill varbinary(50) NOT NULL," \
                        r"    sPhone varbinary(50) NOT NULL," \
                        r"    primary key ( sID ) )"
                cur.execute(lsSql)
                conn.commit()
                rtnData["result"] = True
                rtnData["info"] = "建表完成"
            else:
                rtnData["info"] = "已存在临时表"
        except Exception as e:
            rtnData["info"] += str(e)
            print(str(e))
        finally:
            if(ibConnected):
                conn.close()

        return rtnData

    def handleScore(self):
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        return rtnData

    def queryToken(self):
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }
        lsSql = r"select isnull(sys_var_value, '') from sys_t_system where sys_var_id = 'kmmicro_token'"
        ibConnected = False
        try:
            conn = self.db.GetConnect()
            ibConnected = True
            cur = conn.cursor()
            if not cur:
                rtnData["info"] = "查询access token失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
            else:
                cur.execute(lsSql)
                rsData = cur.fetchall()
                if len(rsData) == 0:
                    rtnData["info"] = "查询access token失败：参数没有初始化"
                else:
                    rtnData["dataString"] = rsData[0][0]
                    rtnData["result"] = True
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            if (ibConnected):
                conn.close()

        return rtnData

    def queryBillList(self, iStatus=2):
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }
        if iStatus == 0:
            lsSql = r"select cBill_C, cTable_C, cTable_N, iGuestNum, nOughtAmt, bSettle, isnull(OpenId, '') from d_t_food_bill0 bill left join kmmicro_t_vip_salesend micro on bill.cBill_C = micro.orderid where bSettle = 0"
        elif iStatus == 1:
            lsSql = r"select cBill_C, cTable_C, cTable_N, iGuestNum, nOughtAmt, bSettle, isnull(OpenId, '') from d_t_food_bill0 bill left join kmmicro_t_vip_salesend micro on bill.cBill_C = micro.orderid where bSettle = 1"
        else:
            lsSql = r"select cBill_C, cTable_C, cTable_N, iGuestNum, nOughtAmt, bSettle, isnull(OpenId, '') from d_t_food_bill0 bill left join kmmicro_t_vip_salesend micro on bill.cBill_C = micro.orderid"
        llKey = ["cBill_C", "cTable_C", "cTable_N", "iGuestNum", "nOughtAmt", "status", "openID"]
        ibConnected = False
        try:
            conn = self.db.GetConnect()
            ibConnected = True
            cur = conn.cursor()
            if not cur:
                rtnData["info"] = "基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
            else:
                cur.execute(lsSql)
                rsData = cur.fetchall()
                rsData = [[(col.rstrip() if isinstance(col, str) else col) for col in line] for line in rsData]
                rtnData["entities"]["orderBill"] = []
                for line in rsData:
                    rtnData["entities"]["orderBill"].append(dict(zip(llKey, line)))
                rtnData["result"] = True
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            if(ibConnected):
                conn.close()

        return rtnData

    def callSoundTaking(self, sBill):
        rtnData = {
            "result": False,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 0,  # 数字
            "info": "",  # 信息
            "entities": {}
        }
        ibConnected = False
        try:
            conn = self.db.GetConnect()
            ibConnected = True
            cur = conn.cursor()
            if not cur:
                rtnData["info"] = "查询access token失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
            else:
                lsSql = r"select convert(char(10), dBusiness, 121), bankcard_no from d_t_food_bill0 where cBill_C = '{sBill}'".format(sBill=sBill)
                cur.execute(lsSql)
                rsData = cur.fetchall()
                if len(rsData) == 0:
                    raise Exception('单据号[{sBill}]无效.'.format(sBill=sBill))
                else:
                    sBusiness = rsData[0][0]
                    sNumber = rsData[0][1]
                lsSql = r"insert into sa_t_voice_queue ( voice_type , voice_value , dbusiness , bill_no , oper_id , oper_date , oper_computer , call_flag , call_time ) " \
                        r"values ( '取餐' , '{snumber}' , '{dBusiness}' , '{sBill}' , '0000' , getdate ( ) , '{computer}' , 0 , null ) " \
                        r"".format(snumber=sNumber, dBusiness=sBusiness, sBill=sBill, computer=self.sett.callComputer)
                cur.execute(lsSql)
                conn.commit()
                rtnData["result"] = True
                rtnData["info"] = "请求呼叫成功."

        except Exception as e:
            rtnData["info"] = str(e)
            print(str(e))
        finally:
            if(ibConnected):
                conn.close()

        return rtnData

    def callWXTaking(self, sBill):
        rtnData = {
            "result": False,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 0,  # 数字
            "info": "",  # 信息
            "entities": {}
        }

        ibConnected = False
        try:
            if len(sBill) == 0:
                raise Exception("请传入订单号")
            conn = self.db.GetConnect()
            ibConnected = True
            cur = conn.cursor()
            if not cur:
                raise Exception("查询km服务地址失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb))
            if self.sett.kmHttpSrv == "" or self.sett.kmHttpPort == "":
                lsSql = r"select isnull(sys_var_value, '') from sys_t_system where sys_var_id = 'kmmicro_ip'"
                cur.execute(lsSql)
                rsData = cur.fetchall()
                if len(rsData) == 0:
                    raise Exception("科脉通讯助手没有正确配置.")
                self.sett.kmHttpSrv = rsData[0][0]
                lsSql = r"select isnull(sys_var_value, '') from sys_t_system where sys_var_id = 'kmmicro_port'"
                cur.execute(lsSql)
                rsData = cur.fetchall()
                if len(rsData) == 0:
                    raise Exception("科脉通讯助手没有正确配置.")
                self.sett.kmHttpPort = rsData[0][0]
                if self.sett.kmHttpSrv == "" or self.sett.kmHttpPort == "":
                    raise Exception("微信通讯助手参数无效.")
            lsSql = r"select ISNULL(orderid, '') from d_t_food_bill0 where cBill_C = '{bill}'".format(bill=sBill)
            cur.execute(lsSql)
            rsData = cur.fetchall()
            if len(rsData) == 0:
                raise Exception("查无此订单[{bill}]".format(bill=sBill))
            lsOrderID = rsData[0][0]
            lsRequest = "http://{srvPath}:{srvPort}/microservices/UpdateOrderGainMealFlag/{bill}".format(srvPath=self.sett.kmHttpSrv, srvPort=self.sett.kmHttpPort, bill=lsOrderID)
            import urllib
            rtnData["info"] = "微信通讯助手响应超时."
            response = urllib.request.urlopen(lsRequest)
            rtnData["info"] = ""
            lsResponse = response.read().decode("gbk")
            if len(lsResponse) == 0:
                rtnData["info"] = "未知的错误"
            else:
                if lsResponse[0] == "1":
                    rtnData["result"] = True
                rtnData["info"] = lsResponse[2:]
        except Exception as e:
            rtnData["info"] += str(e)
        finally:
            if(ibConnected):
                conn.close()

        return rtnData

    def setVipPhone(self, sBill, sPhone):
        rtnData = {
            "result": False,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 0,  # 数字
            "info": "",  # 信息
            "entities": {}
        }

        ibConnected = False
        try:
            if len(sBill) == 0:
                raise Exception("请传入订单号")
            if len(sPhone) == 0:
                raise Exception("请传入手机号")
            conn = self.db.GetConnect()
            ibConnected = True
            cur = conn.cursor()
            if not cur:
                raise Exception("设置会员手机号失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb))
            lsSql = r"select 1 from d_t_food_bill0 where cBill_C = '{bill}'".format(bill=sBill)
            cur.execute(lsSql)
            rsData = cur.fetchall()
            if len(rsData) == 0:
                raise Exception("查无此订单[{bill}]".format(bill=sBill))
            # 存入新表：门店、营业日期、单据号、手机号、积分标志
            lsSql = r"insert into tmpPhone ( sBill, sPhone ) values ( '{sBill}', '{sPhone}' )".format(
                sBill = sBill,
                sPhone = sPhone
            )
            cur.execute(lsSql)
            conn.commit()
            rtnData["result"] = True
            rtnData["info"] = "会员手机号码提交成功"
        except Exception as e:
            rtnData["info"] += str(e)
        finally:
            if(ibConnected):
                conn.close()

        return rtnData

    def queryMealNumber(self):
        rtnData = {
            "result": False,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 0,  # 数字
            "info": "",  # 信息
            "entities": {}
        }

        ibConnected = False
        try:
            conn = self.db.GetConnect()
            ibConnected = True
            cur = conn.cursor()
            if not cur:
                raise Exception("查询取餐号失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb))
            lsSql = r"select bill.cBill_C, bill.cTable_N, iGuestNum, nOughtAmt, num.cgetfood_num from d_t_food_bill0 bill, d_t_foodbill num where bill.cBill_C = num.cbill_c"
            cur.execute(lsSql)
            rsData = cur.fetchall()
            llKey = ["cBill_C", "cTable_N", "iGuestNum", "nOughtAmt", "cgetfood_num"]
            rsData = [[(col.rstrip() if isinstance(col, str) else col) for col in line] for line in rsData]
            rtnData["entities"]["orderBill"] = []
            for line in rsData:
                rtnData["entities"]["orderBill"].append(dict(zip(llKey, line)))
            rtnData["result"] = True
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            if(ibConnected):
                conn.close()

        return rtnData

if __name__ == "__main__":
    b = InterData(a)
    c = b.basicDataGet("dishCategory")
    if c["result"]:
        print(c["entities"]["dishCategory"])
    else:
        print("Some wrong is happen.")
