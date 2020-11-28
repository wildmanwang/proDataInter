# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
from busiProcess import BusiProcess
from interMssql import MSSQL
import datetime

class FrontHongshang(BusiProcess):
    """
    鸿商作为营业前端，直连数据库：
    """

    def __init__(self, sett):
        """
        实例化
        :param sett:
        """
        super().__init__(sett)
        self.interName = "鸿商系统"
        self.db = MSSQL(self.interConn["host"], self.interConn["user"], self.interConn["password"], self.interConn["database"])

    def _getOrderNewNo(self, cursor):
        """
        获取新单据号
        """
        rtnData = {
            "result": True,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 1,  # 数字
            "info": "",  # 信息
            "entities": {}  # 表体集
        }
        iYear = datetime.datetime.strftime(datetime.datetime.today(), "%y")
        sYear = str(iYear).rjust(2, "0")
        lsSql = "select max(RIGHT(orderid, 8)) from orderselfapp where orderid like \'00{year}%\'".format(year=sYear)
        cursor.execute(lsSql)
        ds = cursor.fetchall()
        if ds[0][0]:
            iNum = int(ds[0][0])
        else:
            iNum = 0
        iNum += 1

        rtnData["dataString"] = "00" + sYear + str(iNum).rjust(8, "0")

        return rtnData

    def getItems(self, itemNo):
        """
        获取商品列表
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

        itemNo = "00021509"         # 购物袋小
        itemNo = "00036967"         # 一毛钱的糖果

        lsSql = r"select	comid '第三方商品id', " \
                r"comname '商品名称',  " \
                r"'' '商品商标',  " \
                r"'' '商品主图',  " \
                r"'' '商品图片列表',  " \
                r"'' '图文详情', " \
                r"remark '商品描述', " \
                r"-1 '库存', " \
                r"0 '虚拟销量', " \
                r"0 '限量销售', " \
                r"0 '单次限量销售', " \
                r"'' '扩展参数', " \
                r"0 '成本', " \
                r"0 '基本邮费', " \
                r"1 '邮费计算方式', " \
                r"unit '单位', " \
                r"saleprice '销售价', " \
                r"saleprice '原价', " \
                r"1 '上门自提', " \
                r"0 '自提延时时间', " \
                r"'' '自提开始时间', " \
                r"'' '自提结束时间', " \
                r"0 '排序', " \
                r"'2020-01-01' '开始可用时间', " \
                r"'2222-01-01' '结束可用时间' " \
                r"from plu " \
                r"where lowsalesum >= 0.0 " \
                r"and status in ('A','B','C','') "
        if itemNo:
            lsSql += r" and comid = '{itemNo}'".format(itemNo=itemNo)
        colName = ["out_goods_id", "goods_name", "logo", "master_picture", "pictures", "description", "comment", "stock", "virtual_sales", "limited_sale", "limited_single", "extra", "cost", "postage", "postage_type", "unit", "price", "original_price", "pickup", "pickup_delay_time", "pickup_start_time", "pickup_end_time", "sort", "start_time", "end_time"]
        cur.execute(lsSql)
        rsItems = cur.fetchall()
        rsItems = [[(col.rstrip() if isinstance(col, str) else col) for col in line] for line in rsItems]
        rtnData["entities"]["item"] = []
        for line in rsItems:
            rtnData["entities"]["item"].append(dict(zip(colName, line)))

        # 关闭连接
        conn.close()

        return rtnData

    def putOrders(self, dsOrder):
        """
        写入订单
        :param dsOrder: 新增订单列表
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {
                "order": []
            }                  # 表体集
        }

        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("业务数据获取失败：{name}数据库[{db}]连接失败".format(name=self.interName, db=self.interConn["database"]))

        for bill in dsOrder["entities"]["order"]:
            try:
                lsSql = r"select count(*) from orderselfapp where outtradeno='{outtradeno}'".format(outtradeno=bill["order_id"])
                cur.execute(lsSql)
                rsData = cur.fetchall()
                if rsData[0][0]:
                    continue
                rtnTmp = self._getOrderNewNo(cur)
                if rtnTmp["result"]:
                    sBill = rtnTmp["dataString"]
                else:
                    raise Exception(rtnTmp["info"])
                lsSql = r"insert into orderselfapp (orderid, deptid, deptname, vipid, status, totalfee, disfee, discountfee, payfee, codeid, createtime, paytime, payedfee, outtradeno, paytype)" \
                        r"values ({orderid}, {deptid}, {deptname}, {vipid}, {status}, {totalfee}, {disfee}, {discountfee}, {payfee}, {codeid}, {createtime}, {paytime}, {payedfee}, {outtradeno}, {paytype})" \
                        r"".format(
                    orderid="'"+sBill+"'",
                    deptid="'"+self.sett.defaultOrgNo+"'",
                    deptname="'"+self.sett.defaultOrgName+"'",
                    vipid=("'"+bill["member_id"][:20]+"'") if bill["member_id"] else "NULL",
                    status="'CHECKING'",
                    totalfee=bill["amount"] / 100,
                    disfee=0.00 / 100,
                    discountfee=0.00 / 100,
                    payfee=bill["amount"] / 100,
                    codeid="NULL",
                    createtime=("'"+bill["create_time"]+"'") if bill["create_time"] else "NULL",
                    paytime=("'"+bill["create_time"]+"'") if bill["create_time"] else "NULL",
                    payedfee=bill["amount"] / 100,
                    outtradeno="'"+bill["order_id"]+"'",
                    paytype="'微信支付'" if bill["pay_type"] == "wechat_miniprogram" else "NULL"
                )
                cur.execute(lsSql)
                iNum = 0
                for item in bill["goodses"]:
                    iNum += 1
                    dPrice = round(item["amount"] / item["quantity"] / 100, 2)
                    dAmt = round(item["amount"] / 100, 2)
                    lsSql = r"insert into ordercomselfapp (orderid, deptid, no, comid, barcode, comname, saleprice, quantity, totalfee, weight, vendorid)" \
                            r"values ({orderid}, {deptid}, {no}, {comid}, {barcode}, {comname}, {saleprice}, {quantity}, {totalfee}, {weight}, {vendorid})" \
                            r"".format(
                        orderid="'"+sBill+"'",
                        deptid="'"+self.sett.defaultOrgNo+"'",
                        no=iNum,
                        comid="'"+item["related"]+"'",
                        barcode="''",
                        comname="'"+item["goods_name"]+"'",
                        saleprice=dPrice,
                        quantity=item["quantity"],
                        totalfee=dAmt,
                        weight="'0'",
                        vendorid="'2999'"
                    )
                    cur.execute(lsSql)
                conn.commit()
                rtnData["entities"]["order"].append({
                    "type": "order",
                    "code": bill["order_id"],
                    "related": sBill,
                    "name": "",
                    "time": bill["create_time"]
                })
            except Exception as e:
                conn.rollback()

        # 关闭连接
        conn.close()

        return rtnData
