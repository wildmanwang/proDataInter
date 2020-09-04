# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
from busiProcess import BusiProcess
from interMssql import MSSQL

class FrontKemaiTtysDb(BusiProcess):
    """
    Kemai《天天饮食V8》作为营业前端，直连数据库：
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

        lsSql = r"select	branch_no, branch_name " \
                r"from	bi_t_branch_info " \
                r"where	Property in (4,5) "
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
            lsSql = r"select food.cFood_C, food.cFood_N, cls.cBigCls_C, food.cLitCls_C, food.sUnit, food.nPrc from c_t_food food, c_t_food_litCls cls where food.cLitCls_C = cls.cLitCls_C"
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
            lsSql = r"select    cBill_C, " \
                    r"          cBranch_C, " \
                    r"          dBusiness, " \
                    r"          dtBillTime, " \
                    r"          dtSettleTime, " \
                    r"          nFoodAmt, " \
                    r"          nServiceFee, " \
                    r"          nMinPay, " \
                    r"          nDisAmt, " \
                    r"          nRoundAmt, " \
                    r"          nOughtAmt, " \
                    r"          nPayAmt, " \
                    r"          eStatus, " \
                    r"          remark " \
                    r"from      d_t_food_bill " \
                    r"where     cBranch_C = '{branchno}' " \
                    r"and       dBusiness >= '{sOld}' " \
                    r"and       dBusiness <= '{sDate}' " \
                    r"".format(branchno=branch, sOld=sFrom, sDate=sTo)
            cur.execute(lsSql)
            rsBill = cur.fetchall()
            rtnData["entities"][item] = {}
            rtnData["entities"][item]["bill"] = rsBill

            lsSql = r"select    bills.cBill_C, " \
                    r"          bill.cBranch_C, " \
                    r"          bills.dBusiness, " \
                    r"          bills.cFoodBill, " \
                    r"          bills.cFood_C, " \
                    r"          bills.cFood_N, " \
                    r"          bills.sUnit, " \
                    r"          bills.nPrcOld, " \
                    r"          bills.nPrc, " \
                    r"          bills.nQty, " \
                    r"          bills.nExtPrc, " \
                    r"          bills.nDisAmt, " \
                    r"          bills.nServiceFees, " \
                    r"          bills.nAmt, " \
                    r"          bills.eSuitFlag, " \
                    r"          bills.eRetSendFlag, " \
                    r"          bills.sMade " \
                    r"from      d_t_food_bills bills, d_t_food_bill bill " \
                    r"where     bills.cBill_C = bill.cBill_C " \
                    r"and       bill.cBranch_C = '{branchno}' " \
                    r"and       bills.dBusiness >= '{sOld}' " \
                    r"and       bills.dBusiness <= '{sDate}' " \
                    r"order by  bills.cFoodBill asc " \
                    r"".format(branchno=branch, sOld=sFrom, sDate=sTo)
            cur.execute(lsSql)
            rsItem = cur.fetchall()
            rtnData["entities"][item]["item"] = rsItem

            lsSql = r"select    pay.cBill_C, " \
                    r"          bill.cBranch_C, " \
                    r"          pay.dBusiness, " \
                    r"          pay.cBillNum, " \
                    r"          pay.cPay_C, " \
                    r"          pay.cPay_N, " \
                    r"          pay.ePayType, " \
                    r"          pay.sUnit, " \
                    r"          pay.nOldAmt, " \
                    r"          pay.nExchRate, " \
                    r"          pay.nPayAmt " \
                    r"from      d_t_bill_pay pay, d_t_food_bill bill " \
                    r"where     pay.cBill_C = bill.cBill_C " \
                    r"and       bill.cBranch_C = '{branchno}' " \
                    r"and       pay.dBusiness >= '{sOld}' " \
                    r"and       pay.dBusiness <= '{sDate}' " \
                    r"order by  pay.cBillNum asc " \
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
