# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
from superBillDCB import SuperBillDCB
from interMssql import MSSQL
import time, json

class BillBoli600(SuperBillDCB):

    def __init__(self, sett):
        super().__init__(sett)
        self.station = [1,2,3,4,5,6,7,8]        # 可用基站
        self.db = MSSQL(self.sett.serverHost, self.sett.serverUser, self.sett.serverPwd, self.sett.serverDb)

    def _getStation(self):
        """
        获取基站号
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        try:
            conn = self.db.GetConnect()
            cur = conn.cursor()
            if not cur:
                rtnData["info"] = "基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
            else:
                lsSql = "select sys_var_value from sys_t_system where sys_var_id = 'dcb_stationList'"
                cur.execute(lsSql)
                rsData = cur.fetchall()
                if len(rsData) > 0:
                    staStr = rsData[0][0]
                else:
                    staStr = "[]"
                staList = json.loads(staStr)
                if len(staList) == 0:
                    rtnData["info"] = "基站繁忙，请稍后再试"
                else:
                    rtnData["dataNumber"] = staList.pop(0)
                    lsSql = "update sys_t_system set sys_var_value = '{value}' where sys_var_id = 'dcb_stationList'".format(value=json.dumps(staList))
                    cur.execute(lsSql)
                    conn.commit()
                    rtnData["result"] = True
        except Exception as e:
            rtnData["dataNumber"] = 0
            rtnData["info"] = str(e)
        finally:
            conn.close()

        return rtnData

    def _putStation(self, station):
        """
        释放基站号
        :param station:
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        try:
            conn = self.db.GetConnect()
            cur = conn.cursor()
            if not cur:
                rtnData["info"] = "基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
            else:
                lsSql = "select sys_var_value from sys_t_system where sys_var_id = 'dcb_stationList'"
                cur.execute(lsSql)
                rsData = cur.fetchall()
                if len(rsData) > 0:
                    staStr = rsData[0][0]
                    staList = json.loads(staStr)
                    staList.append(station)
                    staList = list(set(staList))
                    staList.sort()
                    lsSql = "update sys_t_system set sys_var_value = '{value}' where sys_var_id = 'dcb_stationList'".format(value=json.dumps(staList))
                    cur.execute(lsSql)
                    conn.commit()
                    rtnData["result"] = True
                else:
                    rtnData["info"] = "获取基站参数失败"
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            conn.close()

        return rtnData

    def userLogin(self, data):
        """
        登录
        :param data:{
            "terminal":"",                # 开台终端号（3位）
            "factory":"",                 # 出厂号（10位）
            "user":"",                    # 工号（4位）
            "password":""                 # 密码（8位）
        }
        :return:
        """
        rtnData = {
            "result":True,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        # 获取基站
        rtnData = self._getStation()
        if rtnData["result"]:
            iStation = rtnData["dataNumber"]

        try:
            # 参数检查
            if len(self.sett.softNumber) > 0:
                data["terminal"] = self.sett.softNumber
            elif "terminal" not in data:
                raise Exception("请传入参数：点菜宝编号")
            sTerminal = (data["terminal"] + chr(32) * 3)[:3]
            if len(self.sett.serialNumber) > 0:
                data["factory"] = self.sett.serialNumber
            elif "factory" not in data:
                raise Exception("请传入参数：点菜宝序列号")
            sFactory = ("0" * 10 + data["factory"])[-10:]
            if len(self.sett.loginUser) > 0:
                data["user"] = self.sett.loginUser
                data["password"] = self.sett.loginPassword
            elif "user" not in data:
                raise Exception("请传入参数：用户及密码")
            sUser = (data["user"] + chr(32) * 5)[:4]
            sPassword = (data["password"] + chr(32) * 8)[:8]

            # 生成开台请求数据
            sCon = []
            sCon.append("DL  " + chr(32) + sTerminal)
            sCon.append(sFactory + chr(32) + sUser + chr(32) + sPassword)
            # sCon.append(sUser + chr(32) + sPassword)

            # 开台请求写入文件，并通知餐饮服务
            if rtnData["result"]:
                rtnData = self._writeBusiData(iStation, sCon)

            # 获取执行结果
            if rtnData["result"]:
                rtnData = self._readRtnData(iStation, "登录", sCon, 0, "", 1)
        except Exception as e:
            rtnData["result"] = False
            rtnData["info"] = str(e)
        finally:
            # 释放基站
            if "iStation" in locals():
                self._putStation(iStation)
            # 返回执行结果
            return rtnData

    def billOpen(self, data):
        """
        开台
        :param data:{
            "terminal":"",                # 开台终端号（3位）
            "table":"",                   # 桌台号（4位）
            "waiter":"",                  # 服务员号（5位）
            "guestNum":0,                 # 客人数量（2位）
            "factory":""                 # 出厂号（后7/10位）
        }
        :return:
        """
        rtnData = {
            "result":True,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        # 获取基站
        rtnData = self._getStation()
        if rtnData["result"]:
            iStation = rtnData["dataNumber"]

        try:
            # 参数检查
            if len(self.sett.softNumber) > 0:
                data["terminal"] = self.sett.softNumber
            elif "terminal" not in data:
                raise Exception("请传入参数：点菜宝编号")
            sTerminal = (data["terminal"] + chr(32) * 3)[:3]
            if "table" in data:
                sTable = (data["table"] + chr(32) * 4)[:4]
            else:
                rtnData["result"] = False
                rtnData["info"] = "请传入桌台号"
            if "waiter" in data:
                sWaiter = (data["waiter"] + chr(32) * 5)[:5]
            else:
                sWaiter = chr(32) * 5
            if "guestNum" in data:
                sGuestNum = ("0" + str(int(data["guestNum"])))[-2:]
            else:
                sGuestNum = "01"
            if len(self.sett.serialNumber) > 0:
                data["factory"] = self.sett.serialNumber
            elif "factory" not in data:
                raise Exception("请传入参数：点菜宝序列号")
            sFactory = ("0" * 10 + data["factory"])

            # 生成开台请求数据
            if rtnData["result"]:
                sCon = []
                sCon.append("KT  " + chr(32) + sTerminal)
                sCon.append(sTable + chr(32) + sGuestNum + chr(32) + sWaiter + chr(32) + sFactory[-7:] + chr(
                    32) + time.strftime("%H:%M:%S"))

            # 开台请求，并获取反馈
            if rtnData["result"]:
                rtnData = self._writeBusiData(iStation, sCon)

            # 获取执行结果
            if rtnData["result"]:
                rtnData = self._readRtnData(iStation, "开台", sCon, 1, "开台成功", 1)
        except Exception as e:
            rtnData["result"] = False
            rtnData["info"] = str(e)
        finally:
            # 释放基站
            if "iStation" in locals():
                self._putStation(iStation)
            # 返回执行结果
            return rtnData

    def billPut(self, data):
        """
        点菜
        :param data:{
            "terminal":"",                # 开台终端号（3位）
            "table":"",                   # 桌台号+账单流水号（4+3=7位）
            "factory":"",                 # 出厂号（4+4+2=10位）
            "remark":"",                  # 整单备注（12位）
            "item":[{
                "food":"",                  # 菜品号（5位）
                "qty":1,                    # 数量（4位）
                "made":"",                  # 做法（12位）
                "suit":"",                  # 套餐号（2位）
                "waitUp":0                  # 等叫标志（1位）
            }]
        }
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        # 获取基站
        rtnData = self._getStation()
        if rtnData["result"]:
            iStation = rtnData["dataNumber"]

        try:
            # 参数检查
            if len(self.sett.softNumber) > 0:
                data["terminal"] = self.sett.softNumber
            elif "terminal" not in data:
                raise Exception("请传入参数：点菜宝编号")
            sTerminal = (data["terminal"] + chr(32) * 3)[:3]
            if "table" in data:
                sTable = (data["table"] + chr(32) * 7)[:7]
            else:
                rtnData["result"] = False
                rtnData["info"] = "请传入桌台号"
            if len(self.sett.serialNumber) > 0:
                data["factory"] = self.sett.serialNumber
            elif "factory" not in data:
                raise Exception("请传入参数：点菜宝序列号")
            sFactory = ("0" * 10 + data["factory"])
            if "remark" in data:
                sRemark = (data["remark"] + chr(32) * 12)[:12]
            else:
                sRemark = chr(32) * 12
            sFlow = time.strftime("%H:%M:%S")

            # 生成开台请求数据
            if rtnData["result"]:
                sCon = []
                sCon.append("DC  " + chr(32) + sTerminal)
                sCon.append(sTable + chr(32) + sFactory[:4] + chr(32) + chr(32) * 6 + sRemark + chr(32) + chr(
                    32) * 4 + sFlow + chr(32) + sFactory[4:8] + chr(32) + sFactory[8:10])
                for line in data["item"]:
                    sFood = (line["food"] + chr(32) * 5)[:5]
                    sQty = (chr(32) * 4 + str(line["qty"]))[-4:]
                    if "made" in line:
                        sMade = (line["made"] + chr(32) * 12)[:12]
                    else:
                        sMade = chr(32) * 12
                    if "suit" in line:
                        suit = (line["suit"] + chr(32) * 2)[:2]
                    else:
                        suit = chr(32) * 2
                    if "waitUp" in line:
                        waitUp = (str(line["waitUp"]) + "0")[-1:]
                    else:
                        waitUp = "0"
                    sCon.append(
                        sTable + chr(32) + sFood + chr(32) + sQty + chr(32) + sMade + chr(32) + suit + chr(32) + waitUp)

            # 开台请求写入文件，并通知餐饮服务
            if rtnData["result"]:
                rtnData = self._writeBusiData(iStation, sCon)

            # 获取执行结果
            if rtnData["result"]:
                rtnData = self._readRtnData(iStation, "点菜", sCon, 1, "点菜成功", 1)
        except Exception as e:
            rtnData["result"] = False
            rtnData["info"] = str(e)
        finally:
            # 释放基站
            if "iStation" in locals():
                self._putStation(iStation)
            # 返回执行结果
            return rtnData
