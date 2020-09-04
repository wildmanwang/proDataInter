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
        if self.sett.clientCode == "YDHDY":
            from billBoli600 import BillBoli600
            self.interClient = BillBoli600(sett)
            self._initData()

    def _initData(self):
        """
        数据初始化
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        #初始化基站状态
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            rtnData["info"] = "基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
        else:
            lsSql = "select 1 from sys_t_system where sys_var_id = 'dcb_stationList'"
            cur.execute(lsSql)
            rsData = cur.fetchall()
            if len(rsData) == 0:
                lsSql = "insert into sys_t_system ( sys_var_id, sys_var_type, sys_var_name, sys_var_value, display_flag, change_flag, sys_var_remark ) values ('dcb_stationList', '接口', 'dcb点菜接口', '', 0, 1, '')"
                cur.execute(lsSql)
            lsSql = "update sys_t_system set sys_var_value = '[1,2,3,4,5,6,7,8]' where sys_var_id = 'dcb_stationList'"
            cur.execute(lsSql)
            conn.commit()
            conn.close()

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
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {
                "order": {}
            }
        }

        if self.sett.terminal == "boli6.00":
            rtnData = self.interClient.userLogin(data)
        else:
            rtnData["info"] = "无效的客户端类型[{code}].".format(code=self.sett.clientCode)

        return rtnData

    def basicDataRefresh(self):
        """
        刷新基础数据
        :return:
        """
        if self.sett.serverCode == 0:
            return self.interClient.basicDataRefresh()
        elif self.sett.serverCode == 1:
            return {"result": True, "info": ""}
        else:
            return {"result": False, "info": "无效的服务端代码"}

    def _basicDataGet0(self, sType):
        """
        获取基础资料
        :param sType:
        dishCategory        菜品类别
            dishCategory        菜品类别
        dishInfo            菜品信息
            dishItem            菜品
            dishSize            例牌
            sizeItem            例牌详情
        dishSuit            套餐
            FoodSuitItem        套餐项
            FoodSuitExchange    套餐替换项
        dishPrice           价格
        dishReasonReturn    退菜原因
        madeInfo
            MadeCls        做法类别
            Made            做法
            FoodMade        菜品做法
            MadeClsFoodCls  做法类别和菜品小类关系
        deskInfo
            HallFloor       桌台区域
            DeskFlie        桌台
        operator            操作员
        waiter              服务员
        soldOut             沽清信息
        :return:
        """
        if sType == 'soldOut':
            para = {
                "terminal": "",
                "factory": ""
            }
            rtnData = self.interClient.basicDataSoldout(para)
        else:
            rtnData = self.interClient.basicDataGet(sType)

        return rtnData

    def _basicDataGet1(self, sType):
        """
        获取基础资料
        :param sType:
        dishCategory        菜品类别
            dishCategory        菜品类别
        dishInfo            菜品信息
            dishItem            菜品
            dishSize            例牌
            sizeItem            例牌详情
        dishSuit            套餐
            FoodSuitItem        套餐项
            FoodSuitExchange    套餐替换项
        dishPrice           价格
        dishReasonReturn    退菜原因
        madeInfo
            MadeCls        做法类别
            Made            做法
            FoodMade        菜品做法
            MadeClsFoodCls  做法类别和菜品小类关系
        deskInfo
            HallFloor       桌台区域
            DeskFlie        桌台
        operator            操作员
        waiter              服务员
        soldOut             沽清信息
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }
        ldItem = {}
        ldKey = {}
        if sType == 'dishCategory':
            ldItem["dishCategory"] = r"select cLitCls_C, cLitCls_N from c_t_food_litCls order by nNum"
            ldKey["dishCategory"] = ["cLitCls_C", "cLitCls_N"]
        elif sType == 'dishInfo':
            ldItem["dishItem"] = r"select cFood_C, cFood_N, cLitCls_C, sNameFast, sUnit, bSuitFood, eSuitType, bMultiUnit, bTimePrc, nPrc, nPrcRoom, nPrcRoom2, nPrcRoom3, isnull(nPrcRoom4, 0), nPrcVip1, nPrcVip2, nPrcVip3, nFee from c_t_food where bUse = 1 and bSaleClose = 0 and isnull(bInHandpro, 0) = 1 order by isnull(nNum, 9999) asc, cFood_C asc"
            ldKey["dishItem"] = ["cFood_C", "cFood_N", "cLitCls_C", "sNameFast", "sUnit", "bSuitFood", "eSuitType", "bMultiUnit", "bTimePrc", "nPrc", "nPrcRoom", "nPrcRoom2", "nPrcRoom3", "nPrcRoom4", "nPrcVip1", "nPrcVip2", "nPrcVip3", "nFee"]
            ldItem["dishSize"] = r"select cFood_C, cFoodSize, nPrc, nPrcRoom, nPrcRoom2, nPrcRoom3, nPrcRoom4, nPrcVIP1, nPrcVIP2, nPrcVIP3 from c_t_food_size order by cFood_C, cFoodSize"
            ldKey["dishSize"] = ["cFood_C", "cFoodSize", "nPrc", "nPrcRoom", "nPrcRoom2", "nPrcRoom3", "nPrcRoom4", "nPrcVIP1", "nPrcVIP2", "nPrcVIP3"]
        elif sType == "dishSuit":
            ldItem["FoodSuitItem"] = r"select cSuit_C, cFood_C, cFood_N, nPrc, nQty, sSelectType, sortid, sunit from c_t_food_suit order by cSuit_C, sortid"
            ldKey["FoodSuitItem"] = ["cSuit_C", "cFood_C", "cFood_N", "nPrc", "nQty", "sSelectType", "sortid", "sunit"]
            ldItem["FoodSuitExchange"] = r"select cSuit_C, cFood_C, cFood_N, cExchange_C, cExchange_N, nPrice, sunit from c_t_food_suitexchange order by cSuit_C, cFood_C, cSuitNo"
            ldKey["FoodSuitExchange"] = ["cSuit_C", "cFood_C", "cFood_N", "cExchange_C", "cExchange_N", "nPrice", "sunit"]
        elif sType == "dishPrice":
            rtnData["info"] = "暂不提供菜品特价"
        elif sType == "dishReasonReturn":
            ldItem["dishReasonReturn"] = r"select cDict_C, cDict_N, cDictRemark from sa_t_dict where cType = '退品原因' and cDict_C > '00' order by cDict_C"
            ldKey["dishReasonReturn"] = ["cDict_C", "cDict_N", "cDictRemark"]
        elif sType == "madeInfo":
            ldItem["MadeCls"] = r"select cMadeCls_C, cMadeCls_N, bBillRemark from f_t_madecls order by cMadeCls_C"
            ldKey["MadeCls"] = ["cMadeCls_C", "cMadeCls_N", "bBillRemark"]
            ldItem["Made"] = r"select cMade_C, cMade_N, nExtPrice, cMadeCls, bNumPrc from f_t_made order by iSortID"
            ldKey["Made"] = ["cMade_C", "cMade_N", "nExtPrice", "cMadeCls", "bNumPrc"]
            ldItem["FoodMade"] = r"select cFood_C, cMade_C from c_t_food_madeCls order by cFood_C, cMade_C"
            ldKey["FoodMade"] = ["cFood_C", "cMade_C"]
            ldItem["MadeClsFoodCls"] = r"select cMadeCls_C, cCls_C from f_t_madecls_cls order by cMadeCls_C, cCls_C"
            ldKey["MadeClsFoodCls"] = ["cMadeCls_C", "cCls_C"]
        elif sType == "deskInfo":
            ldItem["HallFloor"] = r"select cFloor_C, cFloor_N, bRoomPrice from f_t_floor order by cFloor_C"
            ldKey["HallFloor"] = ["cFloor_C", "cFloor_N", "bRoomPrice"]
            ldItem["DeskFlie"] = r"select cTable_C, cTable_N, cFloor_C, bEnabled, iSeatNum from f_t_table order by iSort"
            ldKey["DeskFlie"] = ["cTable_C", "cTable_N", "cFloor_C", "bEnabled", "iSeatNum"]
        elif sType == "operator":
            ldItem["operator"] = r"select oper_id, oper_name, log_pw from sa_t_operator_info where log_pos = 1 and oper_status = 1 order by oper_id"
            ldKey["operator"] = ["oper_id", "oper_name", "log_pw"]
        elif sType == "waiter":
            ldItem["waiter"] = r"select cEmp_C, cEmp_N from f_t_employee where bServiceFlag = 1 order by cEmp_C"
            ldKey["waiter"] = ["cEmp_C", "cEmp_N"]
        elif sType == "soldOut":
            ldItem["soldOut"] = r"select cFood_C, cFood_N, nStock from d_t_item_stock where sClearType = '数量沽清' order by cFood_C"
            ldKey["soldOut"] = ["cFood_C", "cFood_N", "nStock"]
        else:
            rtnData["info"] = "非法的数据类型参数:{sType}".format(sType=sType)
        if len(rtnData["info"]) == 0:
            try:
                conn = self.db.GetConnect()
                cur = conn.cursor()
                if not cur:
                    rtnData["info"] = "基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
                else:
                    for lsItem in ldItem:
                        lsSql = ldItem[lsItem]
                        cur.execute(lsSql)
                        rsData = cur.fetchall()
                        rsData = [[(col.rstrip() if isinstance(col, str) else col) for col in line] for line in rsData]
                        rtnData["entities"][lsItem] = []
                        for line in rsData:
                            rtnData["entities"][lsItem].append(dict(zip(ldKey[lsItem], line)))
                    rtnData["result"] = True
            except Exception as e:
                rtnData["info"] = str(e)
            finally:
                conn.close()

        return rtnData

    def basicDataGet(self, sType):
        if self.sett.serverCode == 0:
            return self._basicDataGet0(sType)
        elif self.sett.serverCode == 1:
            return self._basicDataGet1(sType)
        else:
            return {"result": False, "info": "无效的服务端代码"}

    def basicDataFoodPic(self, sFood):
        """
        获取菜品图片
        :return:图片
        """
        rtnData = {
            "result": False,
            "info": ""
        }
        if self.sett.serverCode == 0:
            rtnData["info"] = "当前版本不支持获取菜品图片"
        else:
            try:
                sPic = ""
                conn = self.db.GetConnect()
                cur = conn.cursor()
                if not cur:
                    rtnData["info"] = "基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
                else:
                    lsSql = r"select isnull(sPicName, '') from c_t_food where cFood_C = '{food}'".format(food=sFood)
                    cur.execute(lsSql)
                    rsData = cur.fetchall()
                    if len(rsData) > 0:
                        sPic = rsData[0][0].strip()
                        if len(sPic) > 0:
                            rtnData["result"] = True
                        else:
                            rtnData["info"] = "菜品{food}没有设置图片".format(food=sFood)
                    else:
                        rtnData["info"] = "查无此菜品{food}".format(food=sFood)
            except Exception as e:
                rtnData["info"] = str(e)
            finally:
                conn.close()

        if rtnData["result"]:
            file = os.path.join(self.sett.foodPicPath, sPic)
            if not os.path.exists(file):
                return json.dumps({"result": False, "info": "查无此二维码"}, cls=MyJSONEncoder, ensure_ascii=False)
            with open(file, "rb") as f:
                image = f.read()
            from flask import Response
            return Response(image, mimetype="image/jpeg")
        else:
            return json.dumps(rtnData, cls=MyJSONEncoder, ensure_ascii=False)

    def _busiTableStatus0(self, sTable):
        """
        查询空闲桌台
        :param sTable:
        :return:
        """
        sTable = sTable.strip()
        para = {
            "terminal": "",
            "factory": ""
        }
        if len(sTable) > 0:
            para["table"] = sTable
            return self.interClient.busiTableStatusSingle(para)
        else:
            return self.interClient.busiTableStatusAll(para)

    def _busiTableStatus1(self, sTable):
        """
        获取桌台状态
        :param sTable:
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {
                "tableStatus":[]
            }
        }
        if len(sTable) > 0:
            lsSql = "select cTable_C, eStatus, cBill_C, nOughtAmt from d_t_food_Bill0 where eStatus <> '结账' and cTable_C = '{table}' order by cTable_C".format(table=sTable)
        else:
            lsSql = "select cTable_C, eStatus, cBill_C, nOughtAmt from d_t_food_Bill0 where eStatus <> '结账' order by cTable_C"
        try:
            conn = self.db.GetConnect()
            cur = conn.cursor()
            if not cur:
                rtnData["info"] = "基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
            else:
                cur.execute(lsSql)
                rsData = cur.fetchall()
                for line in rsData:
                    rtnData["entities"]["tableStatus"].append(dict(zip(["cTable_C", "eStatus", "cBill_C", "nOughtAmt"], line)))
                rtnData["result"] = True
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            conn.close()

        return rtnData

    def busiTableStatus(self, sTable):
        """
        查询桌台状态
        :param sTable:
        :return:
        """
        if self.sett.serverCode == 0:
            rtnData =  self._busiTableStatus0(sTable)
            rtnData["entities"]["tableStatus"] = []
            if rtnData["result"] and len(rtnData["info"]) > 0:
                rsData = []
                ls_orig = rtnData["info"].split("\n")
                for item in ls_orig:
                    li_pos = item.find("：")
                    if li_pos >= 0:
                        item = item[li_pos+1:]
                        ls_sub = item.split("、")
                        rsData.extend(ls_sub)
                    elif len(item) > 0:
                        rtnData["info"] = item
                rsData = [[sTable, "空闲", "", 0.00] for sTable in rsData]
                for line in rsData:
                    rtnData["entities"]["tableStatus"].append(dict(zip(["cTable_C", "eStatus", "cBill_C", "nOughtAmt"], line)))
            if len(sTable) > 0:
                rtnData["entities"]["tableStatus"] = [rec for rec in rtnData["entities"]["tableStatus"] if rec["cTable_C"] == sTable]
            return rtnData
        elif self.sett.serverCode == 1:
            return self._busiTableStatus1(sTable)
        else:
            return {"result": False, "info": "无效的服务端代码"}

    def busiBillOpen(self, data):
        """
        开台
        :param data:{
            "terminal":"01",                # 开台终端号
            "table":"",                   # 桌台号
            "waiter":"",                  # 服务员号
            "guestNum":0                  # 客人数量
        }
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {
                "order": {}
            }
        }

        if self.sett.terminal == "boli6.00":
            rtnData = self.interClient.billOpen(data)
        else:
            rtnData["info"] = "无效的客户端类型[{code}].".format(code=self.sett.clientCode)

        return rtnData

    def busiBillPut(self, data):
        """
        下单
        :param data:
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {
                "order": {},
                "dishes": []
            }
        }

        if self.sett.terminal == "boli6.00":
            rtnData = self.interClient.billPut(data)
        else:
            rtnData["info"] = "无效的客户端类型[{code}].".format(code=self.sett.clientCode)

        return rtnData

    def _busiBillGet0(self, sTable):
        """
        账单查询
        :param sTable:
        :return:
        """
        para = {
            "terminal": "",
            "table": sTable,
            "factory": ""
        }
        return self.interClient.billGet(para)

    def _busiBillGet1(self, sBill):
        """
        获取单据
        :param sBill:
        :return:
        """
        rtnData = {
            "result":True,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {
                "order": [],
                "dishes": [],
                "mades": []
            }
        }

        if sBill.upper() == "ALL":
            lsSqlBill = "select cBill_C, cTable_C, iGuestNum, stbremark, dtBillTime, eStatus, dtSettleTime from d_t_food_Bill0 order by cBill_C"
            lsSqlItem = "select cBill_C, cFoodBill, cFood_C, cFood_N, cLitCls_C, nPrcBill, nQty, eRetSendFlag, eSuitFlag, cSuitBill from d_t_food_bills0 order by cBill_C, cFoodBill"
            lsSqlMade = "select cBill_C, madeID, cFoodBill, cFood_C, cMade_C, cMade_n, nExtQty, nExtPrice, nExtAmt, bNumPrc from d_t_food_Billsmade0 order by cBill_C, cFoodBill, madeID"
        else:
            lsSqlBill = "select cBill_C, cTable_C, iGuestNum, stbremark, dtBillTime, eStatus, dtSettleTime from d_t_food_Bill0 where cBill_C = '{billID}'".format(billID=sBill)
            lsSqlItem = "select cBill_C, cFoodBill, cFood_C, cFood_N, cLitCls_C, nPrcBill, nQty, eRetSendFlag, eSuitFlag, cSuitBill from d_t_food_bills0 where cBill_C = '{billID}' order by cFoodBill".format(billID=sBill)
            lsSqlMade = "select cBill_C, madeID, cFoodBill, cFood_C, cMade_C, cMade_n, nExtQty, nExtPrice, nExtAmt, bNumPrc from d_t_food_Billsmade0 where cBill_C = '{billID}' order by cFoodBill, madeID".format(billID=sBill)
        lsKeyBill = ["cBill_C", "cTable_C", "iGuestNum", "stbremark", "dtBillTime", "eStatus", "dtSettleTime"]
        lsKeyItem = ["cBill_C", "cFoodBill", "cFood_C", "cFood_N", "cLitCls_C", "nPrcBill", "nQty", "eRetSendFlag", "eSuitFlag", "cSuitBill"]
        lsKeyMade = ["cBill_C", "madeID", "cFoodBill", "cFood_C", "cMade_C", "cMade_n", "nExtQty", "nExtPrice", "nExtAmt", "bNumPrc"]

        try:
            conn = self.db.GetConnect()
            cur = conn.cursor()
            if not cur:
                rtnData["info"] = "基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb)
            else:
                cur.execute(lsSqlBill)
                rsData = cur.fetchall()
                for line in rsData:
                    rtnData["entities"]["order"].append(dict(zip(lsKeyBill, line)))
                cur.execute(lsSqlItem)
                rsData = cur.fetchall()
                for line in rsData:
                    rtnData["entities"]["dishes"].append(dict(zip(lsKeyItem, line)))
                cur.execute(lsSqlMade)
                rsData = cur.fetchall()
                for line in rsData:
                    rtnData["entities"]["mades"].append(dict(zip(lsKeyMade, line)))
                rtnData["result"] = True
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            conn.close()

        return rtnData

    def busiSettleCode(self, sTable):
        """
        获取结帐二维码
        :param sTable:
        :return:
        """
        file = os.path.join(self.sett.tableQRPath, "{tableID}.jpg".format(tableID=sTable))
        if not os.path.exists(file):
            return json.dumps({"result": False, "info": "查无此二维码"}, cls=MyJSONEncoder, ensure_ascii=False)
        with open(file, "rb") as f:
            image = f.read()
        from flask import Response
        return Response(image, mimetype="image/jpeg")

if __name__ == "__main__":
    b = InterData(a)
    c = b.basicDataGet("dishCategory")
    if c["result"]:
        print(c["entities"]["dishCategory"])
    else:
        print("Some wrong is happen.")
