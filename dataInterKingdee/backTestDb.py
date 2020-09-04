# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
from datetime import datetime
from busiProcess import BusiProcess
from interMssql import MSSQL

class BackTestDb(BusiProcess):
    """
    自建测试数据库作为业务后端，直连数据库：
    菜品资料：导入
    销售单据：导入
    """

    def __init__(self, sett, endType):
        """
        实例化
        :param sett:
        :param endType:
        """
        super().__init__(sett, endType)
        self.interType = "db"
        self.interBase = "in"
        self.interItems = {"item", "saleBill"}
        self.db = MSSQL(self.interConn["host"], self.interConn["user"], self.interConn["password"], self.interConn["database"])

    def interInit(self):
        """
        初始化
        :return:
        """
        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("后端初始化失败：{name}数据库[{db}]连接失败".format(name=self.interName, db=self.interConn["database"]))

        # 创建菜品表
        lsSql = r"select 1 from sysobjects where xtype = 'U' and id = OBJECT_ID('newFood')"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            # 创建目标菜品表
            lsSql = r"create table newFood ( " \
                    r"  foodid      varchar(20) not null, " \
                    r"  foodname    varchar(60) not null, " \
                    r"  classid     varchar(20) not null, " \
                    r"  price       numeric(10,2) not null, " \
                    r"  primary key ( foodid ) ) "
            cur.execute(lsSql)

        # 创建单据主表
        lsSql = r"select 1 from sysobjects where xtype = 'U' and id = OBJECT_ID('billMaster')"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            # 创建目标单据主表
            lsSql = r"create table billMaster ( " \
                    r"  billId      varchar(50) not null, " \
                    r"  branchId    varchar(20) not null, " \
                    r"  busiDate    char(10)    not null, " \
                    r"  tableId     varchar(20) not null, " \
                    r"  periodId    varchar(20) not null, " \
                    r"  shiftId     varchar(20) null, " \
                    r"  guestNum    int         null, " \
                    r"  createTime  datetime    null, " \
                    r"  settleTime  datetime    null, " \
                    r"  foodAmt     numeric(9,2)    not null, " \
                    r"  serviceFee  numeric(9,2)    not null, " \
                    r"  minfillFee  numeric(9,2)    not null, " \
                    r"  disAmt      numeric(9,2)    not null, " \
                    r"  roundAmt    numeric(9,2)    not null, " \
                    r"  oughtPay    numeric(9,2)    not null, " \
                    r"  paid        numeric(9,2)    not null, " \
                    r"  status      varchar(20)     not null, " \
                    r"  primary key ( billId ) ) "
            cur.execute(lsSql)

        # 创建单据菜品表
        lsSql = r"select 1 from sysobjects where xtype = 'U' and id = OBJECT_ID('billItem')"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            # 创建目标单据商品表
            lsSql = r"create table billItem ( " \
                    r"  billId      varchar(50) not null, " \
                    r"  branchId    varchar(20) not null, " \
                    r"  busiDate    char(10)    not null, " \
                    r"  batchNum    int         not null, " \
                    r"  orderNum    int         not null, " \
                    r"  ItemId      varchar(20) not null, " \
                    r"  ItemName    varchar(80) not null, " \
                    r"  unit        varchar(20) not null, " \
                    r"  prcOld      numeric(9,2)    not null, " \
                    r"  prc         numeric(9,2)    not null, " \
                    r"  qty         numeric(9,2)    not null, " \
                    r"  amtExt      numeric(9,2)    not null, " \
                    r"  amtDis      numeric(9,2)    not null, " \
                    r"  serviceFee  numeric(9,2)    not null, " \
                    r"  amt         numeric(9,2)    not null, " \
                    r"  suitFlag    varchar(20)     not null, " \
                    r"  itemFlag    varchar(20)     not null, " \
                    r"  made        varchar(255)    not null, " \
                    r"  primary key ( billId, batchNum, orderNum ) ) "
            cur.execute(lsSql)

        # 创建单据支付表
        lsSql = r"select 1 from sysobjects where xtype = 'U' and id = OBJECT_ID('billPay')"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            # 创建目标单据支付表
            lsSql = r"create table billPay ( " \
                    r"  billId      varchar(50) not null, " \
                    r"  branchId    varchar(20) not null, " \
                    r"  busiDate    char(10)    not null, " \
                    r"  batchNum    int         not null, " \
                    r"  payId       varchar(20) not null, " \
                    r"  payName     varchar(80) not null, " \
                    r"  payType     varchar(80) not null, " \
                    r"  unit        varchar(20) not null, " \
                    r"  payOrigi    numeric(9,2)    not null, " \
                    r"  exchRate    numeric(9,5)    not null, " \
                    r"  payAmt      numeric(9,2)    not null, " \
                    r"  primary key ( billId, batchNum ) ) "
            cur.execute(lsSql)

        # 提交事务，关闭连接
        conn.commit()
        conn.close()

    def putBaseData(self, putData):
        """
        基础数据导入
        :param putData:
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "item": {                    # 表体代码
                    "item":[]                # 菜品表
                }
            }
        }

        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("基础数据写入失败：{name}数据库[{db}]连接失败".format(name=self.interName, db=self.interConn["database"]))

        for i in putData["entities"]["item"]["item"]:
            lsSql = r"insert into newFood ( foodId, foodName, classId, price ) " \
                    r"values ( '{foodid}', '{foodname}', '{classid}', {price} ) " \
                    r"".format(foodid=i[0], foodname=i[1], classid=i[2], price=i[3])
            cur.execute(lsSql)
            rtnData["entities"]["item"]["item"].append((i[0], i[1], "", ""))

        # 提交事务，关闭连接
        conn.commit()
        conn.close()

        return rtnData

    def putBusiData(self, branch, putData):
        """
        销售单据导入
        :param branch: 门店
        :param putData: 传入的销售单据
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "saleBill": {               # 表体代码
                    "saleBill":[]           # 销售单
                }
            }
        }

        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("业务数据写入失败：{name}数据库[{db}]连接失败".format(name=self.interName, db=self.interConn["database"]))

        # 插入主单
        # business, newbillid, BillTime, SettleTime, FoodAmt, ServiceFee, MinPayFill, DisAmt, RoundAmt, OughtAmt, PayAmt, statuss
        for i in putData["entities"]["saleBill"]["bill"]:
            lsSql = r"insert into billMaster ( billId, branchId, busiDate, tableId, periodId, shiftId, guestNum, " \
                    r"createTime, settleTime, foodAmt, serviceFee, minfillFee, disAmt, roundAmt, oughtPay, paid, status ) " \
                    r"values ('{billId}', '{branchId}', '{busiDate}', '{tableId}', '{periodId}', '{shiftId}', {guestNum}, " \
                    r"'{createTime}', '{settleTime}', {foodAmt}, {serviceFee}, {minfillFee}, {disAmt}, {roundAmt}, {oughtPay}, {paid}, '{status}' ) " \
                    r"".format(
                billId=i[0].rstrip(),
                branchId=i[1],
                busiDate=datetime.strftime(i[2], "%Y-%m-%d"),
                tableId=self.sett.tableNo,
                periodId=self.sett.periodNo,
                shiftId=self.sett.shiftNo,
                guestNum=1,
                createTime=datetime.strftime(i[3], "%Y-%m-%d %H:%M:%S"),
                settleTime=datetime.strftime(i[4], "%Y-%m-%d %H:%M:%S"),
                foodAmt=i[5],
                serviceFee=i[6],
                minfillFee=i[7],
                disAmt=i[8],
                roundAmt=i[9],
                oughtPay=i[10],
                paid=i[11],
                status=i[12]
            )
            cur.execute(lsSql)
            rtnData["entities"]["saleBill"]["saleBill"].append((i[0].rstrip(), "", i[1], datetime.strftime(i[2], "%Y-%m-%d")))

        # 插入项目表
        # newbillid, business, foodbill, foodid, foodname, unit, prcOld, Prc, qty, extPrc, disAmt, serviceFees, amt, SuitFlag, RetSendFlag, made
        for i in putData["entities"]["saleBill"]["item"]:
            lsSql = r"insert into billItem ( billId, branchId, busiDate, batchNum, orderNum, itemId, itemName, " \
                    r"unit, prcOld, prc, qty, amtExt, amtDis, serviceFee, amt, suitFlag, itemFlag, made ) " \
                    r"values ( '{billId}', '{branchId}', '{busiDate}', {batchNum}, {orderNum}, '{itemId}', '{itemName}', " \
                    r"'{unit}', {prcOld}, {prc}, {qty}, {amtExt}, {amtDis}, {serviceFee}, {amt}, '{suitFlag}', '{itemFlag}', '{made}' ) " \
                    r"".format(
                billId=i[0].rstrip(),
                branchId=i[1],
                busiDate=datetime.strftime(i[2], "%Y-%m-%d"),
                batchNum=int(i[3][0:2]),
                orderNum=int(i[3][2:]),
                itemId=i[4].rstrip(),
                itemName=i[5].rstrip(),
                unit=i[6].rstrip(),
                prcOld=i[7],
                prc=i[8],
                qty=i[9],
                amtExt=i[10],
                amtDis=i[11],
                serviceFee=i[12],
                amt=i[13],
                suitFlag=i[14],
                itemFlag=i[15],
                made=i[16]
            )
            cur.execute(lsSql)

        # 插入支付表
        # newbillid, business, billNum, PayId, PayName, PayType, unit, OldAmt, ExchRate, PayAmt
        for i in putData["entities"]["saleBill"]["pay"]:
            lsSql = r"insert into billPay ( billId, branchId, busiDate, batchNum, payId, payName, payType, unit, payOrigi, exchRate, payAmt ) " \
                    r"values ( '{billId}', '{branchId}', '{busiDate}', {batchNum}, '{payId}', '{payName}', '{payType}', '{unit}', {payOrigi}, {exchRate}, {payAmt} ) " \
                    r"".format(
                billId=i[0].rstrip(),
                branchId=i[1],
                busiDate=datetime.strftime(i[2], "%Y-%m-%d"),
                batchNum=int(i[3]),
                payId=i[4].rstrip(),
                payName=i[5].rstrip(),
                payType=i[6].rstrip(),
                unit=i[7].rstrip(),
                payOrigi=i[8],
                exchRate=i[9],
                payAmt=i[10]
            )
            cur.execute(lsSql)

        # 提交事务，关闭连接
        conn.commit()
        conn.close()

        return rtnData
