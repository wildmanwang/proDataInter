# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
from superBillDCB import SuperBillDCB
from interMssql import MSSQL
import time, json
from os import path

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

    def basicDataRefresh(self):
        """
        获取基础资料：请求刷新，才会生成基础资料的文件
        :return:
        """
        rtnData = {
            "result": True,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 0,  # 数字
            "info": "",  # 信息
            "entities": {}
        }
        try:
            # 获取基础数据请求写入文件，并通知餐饮服务
            if rtnData["result"]:
                rtnData = self._socketRequest(11)

            # 获取执行结果
            if rtnData["result"]:
                if rtnData["dataNumber"] == 11:
                    # 读取数据
                    rtnData["info"] = "数据刷新成功"
                else:
                    rtnData["result"] = False
                    rtnData["info"] = "数据返回标志异常"
        except Exception as e:
            rtnData["result"] = False
            rtnData["info"] = str(e)
        finally:
            # 返回执行结果
            return rtnData

    def basicDataGet(self, sType):
        """
        读取基础资料文件
        :param sType:
        :return:
        """
        rtnData = {
            "result": True,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 0,  # 数字
            "info": "",  # 信息
            "entities": {}
        }
        # 文件名
        sType = sType.strip()
        ldItem = {}
        ldKey = {}
        if sType == "dishCategory":
            ldItem["dishCategory"] = "菜品类别表.TXT"
            ldKey["dishCategory"] = ["cLitCls_C", "cLitCls_N"]
        elif sType == "dishInfo":
            ldItem["dishItem"] = "菜品表.TXT"
            ldKey["dishItem"] = ["cFood_C", "cFood_N", "cLitCls_C", "sNameFast", "sUnit", "bSuitFood", "eSuitType", "bMultiUnit", "bTimePrc", "nPrc", "nPrcRoom", "nPrcRoom2", "nPrcRoom3", "nPrcRoom4", "nPrcVip1", "nPrcVip2", "nPrcVip3", "nFee"]
            ldItem["dishSize"] = ""
            ldKey["dishSize"] = ["cFood_C", "cFoodSize", "nPrc", "nPrcRoom", "nPrcRoom2", "nPrcRoom3", "nPrcRoom4", "nPrcVIP1", "nPrcVIP2", "nPrcVIP3"]
        elif sType == "dishSuit":
            ldItem["FoodSuitItem"] = "菜品套餐内容表.TXT"
            ldKey["FoodSuitItem"] = ["cSuit_C", "cFood_C", "cFood_N", "nPrc", "nQty", "sSelectType", "sortid", "sunit"]
            ldItem["FoodSuitExchange"] = "菜品套餐内容表.TXT"
            ldKey["FoodSuitExchange"] = ["cSuit_C", "cFood_C", "cFood_N", "cExchange_C", "cExchange_N", "nPrice", "sunit"]
        elif sType == "dishPrice":
            rtnData["result"] = False
            rtnData["info"] = "暂不提供菜品特价"
        elif sType == "dishReasonReturn":
            ldItem["dishReasonReturn"] = "退菜理由表.TXT"
            ldKey["dishReasonReturn"] = ["cDict_C", "cDict_N", "cDictRemark"]
        elif sType == "madeInfo":
            ldItem["MadeCls"] = ""
            ldKey["MadeCls"] = ["cMadeCls_C", "cMadeCls_N", "bBillRemark"]
            ldItem["Made"] = "客户要求表.TXT"
            ldKey["Made"] = ["cMade_C", "cMade_N", "nExtPrice", "cMadeCls", "bNumPrc"]
            ldItem["FoodMade"] = ""
            ldKey["FoodMade"] = ["cFood_C", "cMade_C"]
            ldItem["MadeClsFoodCls"] = ""
            ldKey["MadeClsFoodCls"] = ["cMadeCls_C", "cCls_C"]
        elif sType == "deskInfo":
            ldItem["HallFloor"] = ""
            ldKey["HallFloor"] = ["cFloor_C", "cFloor_N", "bRoomPrice"]
            ldItem["DeskFlie"] = "包房名称表.TXT"
            ldKey["DeskFlie"] = ["cTable_C", "cTable_N", "cFloor_C", "bEnabled", "iSeatNum"]
        elif sType == "operator":
            ldItem["operator"] = ""
            ldKey["operator"] = ["oper_id", "oper_name", "log_pw"]
        elif sType == "waiter":
            ldItem["waiter"] = ""
            ldKey["waiter"] = ["cEmp_C", "cEmp_N"]
        elif sType == "soldOut":
            # 估清有单独的接口
            ldItem["soldOut"] = ""
            ldKey["soldOut"] = ["cFood_C", "cFood_N", "nStock"]
        else:
            rtnData["result"] = False
            rtnData["info"] = "非法的数据类型参数:{sType}".format(sType=sType)

        # 读文件
        data = {}
        if rtnData["result"]:
            for item in ldItem:
                if len(ldItem[item]) > 0:
                    data[item] = []
                    filename = path.join(self.sett.dataPath, ldItem[item])
                    with open(filename, "r", encoding="ANSI") as f:
                        for line in f.readlines():
                            rec = []
                            line = line.rstrip().encode("GBK")
                            if len(line) > 0:
                                if item == "dishCategory":
                                    rec.append(line[:2].decode("GBK").strip())               # 编码
                                    rec.append(line[2:].decode("GBK").strip())               # 名称
                                elif item == "dishItem":
                                    rec.append(line[:5].decode("GBK").strip())               # 编码
                                    rec.append(line[7:27].decode("GBK").strip())             # 名称
                                    rec.append(line[5:7].decode("GBK").strip())              # 类别
                                    rec.append(line[90:100].decode("GBK").strip())           # 助记码
                                    rec.append(line[36:40].decode("GBK").strip())            # 单位
                                    rec.append(0)                              # 是否套餐
                                    rec.append("")                             # 套餐类型
                                    rec.append(0)                              # 是否多单位
                                    rec.append(0)                              # 是否时价
                                    rec.append(float(line[27:36].decode("GBK").strip()))     # 单价
                                    rec.append(float(line[27:36].decode("GBK").strip()))     # 包房价1
                                    rec.append(float(line[27:36].decode("GBK").strip()))     # 包房价2
                                    rec.append(1)                               # 包房是否启用 >0：启用 0：不启用
                                    rec.append(0)                               # 限售数量 >0：数量 0：不限售
                                    rec.append(float(line[27:36].decode("GBK").strip()))     # 会员价1
                                    rec.append(float(line[27:36].decode("GBK").strip()))     # 会员价2
                                    rec.append(float(line[27:36].decode("GBK").strip()))     # 会员价3
                                    rec.append(0)                              # 服务费
                                elif item == "FoodSuitItem":
                                    if line[29:30] == "1":
                                        rec.append(line[:2].decode("GBK").strip())                # 套餐号
                                        rec.append(line[2:7].decode("GBK").strip())               # 菜品编号
                                        rec.append(line[30:32].decode("GBK").strip())             # 菜品名称，用分组号代替
                                        rec.append(float(line[16:25].decode("GBK").strip()))      # 价格
                                        rec.append(float(line[7:16].decode("GBK").strip()))       # 数量
                                        rec.append("必选项")                       # 选择类型
                                        rec.append(1)                               # 排序号
                                        rec.append(line[25:29].decode("GBK").strip())             # 单位
                                elif item == "FoodSuitExchange":
                                    if "FoodSuitItem" in data:
                                        if line[29:30] == "0":
                                            defaultFood = ""
                                            for findsuit in data["FoodSuitItem"]:
                                                if findsuit[2] == line[30:32].decode("GBK").strip():
                                                    defaultFood = findsuit[1]
                                                    break
                                            rec.append(line[:2].decode("GBK").strip())                # 套餐号
                                            rec.append(line[2:7].decode("GBK").strip())               # 菜品编号
                                            rec.append(line[30:32].decode("GBK").strip())             # 菜品名称，用分组号代替
                                            rec.append(defaultFood)                     # 替换菜品编号
                                            rec.append("")                              # 替换菜品名称
                                            rec.append(float(line[16:25].decode("GBK").strip()))      # 价格
                                            rec.append(line[25:29].decode("GBK").strip())             # 单位
                                elif item == "dishReasonReturn":
                                    rec.append(line[:2].decode("GBK").strip())                # 编码
                                    rec.append(line[2:22].decode("GBK").strip())              # 名称
                                    rec.append("")                              # 备注
                                elif item == "Made":
                                    rec.append(line[:3].decode("GBK").strip())                # 编码
                                    rec.append(line[3:19].decode("GBK").strip())              # 名称
                                    rec.append(0)                               # 加价
                                    rec.append("")                              # 类别
                                    rec.append(0)                               # 是否计数
                                elif item == "DeskFlie":
                                    rec.append(line[:4].decode("GBK").strip())                # 编码
                                    rec.append(line[4:14].decode("GBK").strip())              # 名称
                                    rec.append("")                              # 楼层
                                    rec.append(1)                               # 是否有效
                                    rec.append(1)                               # 座位数
                            data[item].append(rec)
                    if sType == "dishInfo":
                        with open(path.join(self.sett.dataPath, "菜品套餐表.TXT"), "r", encoding="ANSI") as f:
                            for line in f.readlines():
                                rec = []
                                line = line.rstrip().encode("GBK")
                                if len(line) > 0:
                                    rec.append(line[:2].decode("GBK").strip())                # 编码
                                    rec.append(line[2:].decode("GBK").strip())                # 名称
                                    rec.append("")                              # 类别
                                    rec.append("")                              # 助记码
                                    rec.append("")                              # 单位
                                    rec.append(1)                               # 是否套餐
                                    rec.append("可变价")                       # 价格类型
                                    rec.append(0)                               # 是否多单位
                                    rec.append(0)                               # 是否时价
                                    rec.append(-1)                              # 单价（需要由套餐子项累加）
                                    rec.append(-1)                              # 包房价1
                                    rec.append(-1)                              # 包房价2
                                    rec.append(1)                               # 包房是否启用 >0：启用 0：不启用
                                    rec.append(0)                               # 限售数量 >0：数量 0：不限售
                                    rec.append(-1)                              # 会员价1
                                    rec.append(-1)                              # 会员价2
                                    rec.append(-1)                              # 会员价3
                                    rec.append(0)                               # 服务费
                                data[item].append(rec)

        # 数据格式调整
        for item in data:
            rtnData["entities"][item] = []
            for line in data[item]:
                rtnData["entities"][item].append(dict(zip(ldKey[item], line)))

        # 返回数据
        return rtnData

    def basicDataSoldout(self, data):
        """
        获取估清数据
        :param data:{
            "terminal":"",                # 开台终端号（3位）
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
            if len(self.sett.serialNumber) > 0:
                data["factory"] = self.sett.serialNumber
            elif "factory" not in data:
                raise Exception("请传入参数：点菜宝序列号")
            sFactory = ("0" * 10 + data["factory"])

            # 生成沽清列表请求数据
            if rtnData["result"]:
                sCon = []
                sCon.append("GQLB" + chr(32) + sTerminal)
                sCon.append(sFactory[-7:])

            # 获取估清列表请求，并获取反馈
            if rtnData["result"]:
                rtnData = self._writeBusiData(iStation, sCon)

            # 获取执行结果
            if rtnData["result"]:
                rtnData = self._readRtnData(iStation, "估清列表", sCon, 1, "", 1)
        except Exception as e:
            rtnData["result"] = False
            rtnData["info"] = str(e)
        finally:
            # 释放基站
            if "iStation" in locals():
                self._putStation(iStation)
            # 返回执行结果
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

    def busiTableStatusAll(self, data):
        """
        查询空闲桌台
        :param data:{
            "terminal":"",                # 开台终端号（3位）
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
            if len(self.sett.serialNumber) > 0:
                data["factory"] = self.sett.serialNumber
            elif "factory" not in data:
                raise Exception("请传入参数：点菜宝序列号")
            sFactory = ("0" * 10 + data["factory"])

            # 生成开台请求数据
            if rtnData["result"]:
                sCon = []
                sCon.append("KXHZ" + chr(32) + sTerminal)
                sCon.append(sFactory[-7:])

            # 获取估清列表请求，并获取反馈
            if rtnData["result"]:
                rtnData = self._writeBusiData(iStation, sCon)

            # 获取执行结果
            if rtnData["result"]:
                rtnData = self._readRtnData(iStation, "空闲桌台汇总", sCon, 1, "", 1)
        except Exception as e:
            rtnData["result"] = False
            rtnData["info"] = str(e)
        finally:
            # 释放基站
            if "iStation" in locals():
                self._putStation(iStation)
            # 返回执行结果
            return rtnData

    def busiTableStatusSingle(self, data):
        """
        查询空闲桌台
        :param data:{
            "terminal":"",                # 开台终端号（3位）
            "table":"",                   # 桌台号（4位）
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
                raise Exception("请传入桌台号")
            if len(self.sett.serialNumber) > 0:
                data["factory"] = self.sett.serialNumber
            elif "factory" not in data:
                raise Exception("请传入参数：点菜宝序列号")
            sFactory = ("0" * 10 + data["factory"])

            # 生成开台请求数据
            if rtnData["result"]:
                sCon = []
                sCon.append("KXHZ" + chr(32) + sTerminal)
                sCon.append(sTable + chr(32) + sFactory[-7:])

            # 获取估清列表请求，并获取反馈
            if rtnData["result"]:
                rtnData = self._writeBusiData(iStation, sCon)

            # 获取执行结果
            if rtnData["result"]:
                rtnData = self._readRtnData(iStation, "查桌台状态", sCon, 1, "", 1)
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
                sCon.append(sTable + chr(32) + sGuestNum + chr(32) + sWaiter + chr(32) + sFactory[-7:] + chr(32) + time.strftime("%H:%M:%S"))

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

    def billGet(self, data):
        """
        账单查询
        :param data:{
            "terminal":"",                # 开台终端号（3位）
            "table":"",                   # 桌台号（4位）
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
            if "table" not in data:
                raise Exception("请传入桌台号")
            sTable = (data["table"] + chr(32) * 4)[:4]
            if len(self.sett.serialNumber) > 0:
                data["factory"] = self.sett.serialNumber
            elif "factory" not in data:
                raise Exception("请传入参数：点菜宝序列号")
            sFactory = ("0" * 10 + data["factory"])

            # 生成账单查询请求数据
            if rtnData["result"]:
                sCon = []
                sCon.append("ZDCX" + chr(32) + sTerminal)
                sCon.append(chr(32) * 3 + sTable + chr(32) + sFactory[-7:])

            # 获取账单查询请求，并获取反馈
            if rtnData["result"]:
                rtnData = self._writeBusiData(iStation, sCon)

            # 获取执行结果
            if rtnData["result"]:
                rtnData = self._readRtnData(iStation, "账单查询", sCon, 1, "", 1)
        except Exception as e:
            rtnData["result"] = False
            rtnData["info"] = str(e)
        finally:
            # 释放基站
            if "iStation" in locals():
                self._putStation(iStation)
            # 返回执行结果
            return rtnData
