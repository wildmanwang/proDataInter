# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
from busiProcess import BusiProcess
from interMssql import MSSQL

class FrontKemaiHcmDb(BusiProcess):
    """
    Kemai《好参谋V11》作为营业前端，直连数据库：
    菜品资料：导出
    销售单据：导出
    """

    def __init__(self, sett, endType):
        """
        实例化
        :param sett:
        :param endType:
        """
        super().__init__(sett, endType)
        self.interType = "db"
        self.interBase = "out"
        self.interItems = {"item", "saleBill", "accBill"}
        self.db = MSSQL(self.interConn["host"], self.interConn["user"], self.interConn["password"], self.interConn["database"])

    def getBranchs(self):
        """
        获取需要对接的门店列表
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {}                  # 表体集
        }

        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.interName, db=self.interConn["database"]))

        lsSql = r"select	Id, Name " \
                r"from	Branch " \
                r"where	Property in (1,7,8) "
        cur.execute(lsSql)
        rsBranchs = cur.fetchall()
        rsBranchs = [(i[0].rstrip(), i[1].rstrip()) for i in rsBranchs]
        rtnData["entities"]["branch"] = {}
        rtnData["entities"]["branch"]["branch"] = rsBranchs

        # 关闭连接
        conn.close()

        return rtnData

    def getBaseData(self, item):
        """
        基础资料导出
        :param item: 数据项
        :return: 基础资料字典
            item:       商品资料
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {}                  # 表体集
        }

        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.interName, db=self.interConn["database"]))

        if item == "item":
            # 同步菜品数据：编码、名称
            lsSql = r"select FoodId, FoodName, bigClsId, litClsId, unitId, salePrice from Food"
            cur.execute(lsSql)
            rsItem = cur.fetchall()
            rtnData["entities"][item] = {}
            rtnData["entities"][item][item] = rsItem

        # 关闭连接
        conn.close()

        return rtnData

    def getBusiData(self, item, branch, sFrom, sTo):
        """
        销售单据导出
        :param item: 数据项
        :param branch: 门店
        :param sFrom: 开始日期
        :param sTo: 截至日期
        :return: 导出的销售单据
            maxDate:    本次同步的最大日期
            bill:       主单表集合
            item:       商品表集合
            pay:        付款表集合
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {}                  # 表体集
        }

        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("业务数据获取失败：{name}数据库[{db}]连接失败".format(name=self.interName, db=self.interConn["database"]))

        if item in {"saleBill", "accBill"}:
            lsSql = r"select    rtrim(newbillId), " \
                    r"          rtrim(branchId), " \
                    r"          business, " \
                    r"          BillTime, " \
                    r"          SettleTime, " \
                    r"          FoodAmt, " \
                    r"          ServiceFee, " \
                    r"          MinPayFill,	" \
                    r"          DisAmt, " \
                    r"          RoundAmt, " \
                    r"          OughtAmt, " \
                    r"          PayAmt, " \
                    r"          statuss, " \
                    r"          Remark " \
                    r"from      foodbill " \
                    r"where     branchid = '{branchno}' " \
                    r"and       business >= '{sOld}' " \
                    r"and       business <= '{sDate}' " \
                    r"".format(branchno=branch, sOld=sFrom, sDate=sTo)
            cur.execute(lsSql)
            rsBill = cur.fetchall()
            rtnData["entities"][item] = {}
            rtnData["entities"][item]["bill"] = rsBill

            lsSql = r"select    rtrim(newbillId), " \
                    r"          rtrim(branchId), " \
                    r"          business, " \
                    r"          foodbill, " \
                    r"          foodid, " \
                    r"          foodname, " \
                    r"          unit, " \
                    r"          isnull(prcOld, Prc), " \
                    r"          Prc, " \
                    r"          qty, " \
                    r"          extPrc, " \
                    r"          disAmt, " \
                    r"          serviceFees, " \
                    r"          amt, " \
                    r"          SuitFlag, " \
                    r"          RetSendFlag, " \
                    r"          made " \
                    r"from      foodbillEntity " \
                    r"where     branchid = '{branchno}' " \
                    r"and       business >= '{sOld}' " \
                    r"and       business <= '{sDate}' " \
                    r"order by  foodbill asc " \
                    r"".format(branchno=branch, sOld=sFrom, sDate=sTo)
            cur.execute(lsSql)
            rsItem = cur.fetchall()
            rtnData["entities"][item]["item"] = rsItem

            lsSql = r"select    rtrim(newbillId), " \
                    r"          rtrim(branchId), " \
                    r"          business, " \
                    r"          billNum, " \
                    r"          PayId, " \
                    r"          PayName, " \
                    r"          PayType, " \
                    r"          unit, " \
                    r"          OldAmt, " \
                    r"          ExchRate, " \
                    r"          PayAmt " \
                    r"from      foodbillpay " \
                    r"where     branchid = '{branchno}' " \
                    r"and       business >= '{sOld}' " \
                    r"and       business <= '{sDate}' " \
                    r"order by  billnum asc " \
                    r"".format(branchno=branch, sOld=sFrom, sDate=sTo)
            cur.execute(lsSql)
            rsPay = cur.fetchall()
            rtnData["entities"][item]["pay"] = rsPay

            maxDate = ""
            for i in rsBill:
                sBillDate = i[2].strftime("%Y-%m-%d")
                if sBillDate > maxDate:
                    maxDate = sBillDate
            rtnData["dataString"] = maxDate

        # 关闭连接
        conn.close()

        return rtnData
