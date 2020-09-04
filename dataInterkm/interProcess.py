# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
from interMssql import MSSQL

class InterProcess:

    def __init__(self, sett):
        self.sett = sett
        self.dbApp = MSSQL(sett.app_host, sett.app_user, sett.app_pwd, sett.app_db )
        self.dbErp = MSSQL(sett.erp_host, sett.erp_user, sett.erp_pwd, sett.erp_db )

    def interInit(self, bRestart):
        """
        初始化接口
        :return:
        """
        # 获取数据库连接
        connErp = self.dbErp.GetConnect()
        curErp = connErp.cursor()
        if not curErp:
            raise Exception("Erp端数据库连接失败")
        connApp = self.dbApp.GetConnect()
        curApp = connApp.cursor()
        if not curApp:
            raise Exception("App端数据库连接失败")

        # 初始化标志
        lsSql = r"select isnull(sys_var_value, '') from sys_t_system where sys_var_id = 'usewx'"
        curErp.execute(lsSql)
        res = curErp.fetchall()
        if len(res) == 0:
            lsSql = r"insert into sys_t_system ( sys_var_id, sys_var_type, sys_var_name, sys_var_value, display_flag ) " \
                    r"values ( 'usewx', '微信接口', '是否启用微信接口', '1', '0' )"
        elif res[0][0] != "1":
            lsSql = r"update sys_t_system set sys_var_value = '1' where sys_var_id = 'usewx'"
        else:
            lsSql = ""
        if len(lsSql) > 0:
            curErp.execute(lsSql)
        lsSql = r"select isnull(sys_var_value, '') from sys_t_system where sys_var_id = 'UseCRM'"
        curErp.execute(lsSql)
        res = curErp.fetchall()
        if len(res) == 0:
            lsSql = r"insert into sys_t_system ( sys_var_id, sys_var_type, sys_var_name, sys_var_value, display_flag ) " \
                    r"values ( 'UseCRM', '前台参数', '是否CRM服务', '1', '1' )"
        elif res[0][0] != "1":
            lsSql = r"update sys_t_system set sys_var_value = '1' where sys_var_id = 'UseCRM'"
        else:
            lsSql = ""
        if len(lsSql) > 0:
            curErp.execute(lsSql)

        # 数据同步日期
        bInit = False
        lsSql = r"select isnull(sys_var_value, '') from sys_t_system where sys_var_id = 'dInterBase'"
        curErp.execute(lsSql)
        res = curErp.fetchall()
        if len(res) == 0:
            lsSql = r"insert into sys_t_system ( sys_var_id, sys_var_type, sys_var_name, sys_var_value ) values ( 'dInterBase', '系统信息', '外部点餐对接日期', '' )"
            curErp.execute(lsSql)
            lsInterBase = "1900-01-01"
            bInit = True
        else:
            lsInterBase = res[0][0]
            if not lsInterBase or lsInterBase.strip() == "":
                lsInterBase = "1900-01-01"

        # 获取当前营业日期
        lsSql = r"select isnull(sys_var_value, '') from sys_t_system where sys_var_id = 'dBusiness'"
        curErp.execute(lsSql)
        res = curErp.fetchall()
        if len(res) == 0:
            raise Exception("当前营业日期无效")
        self.sBusiness = res[0][0]

        # 建立临时表
        lsSql = r"select 1 from sysobjects where id=object_id('interTmp')"
        curApp.execute(lsSql)
        res = curApp.fetchall()
        if len(res) == 0:
            lsSql = r"create table interTmp ( " \
                    r"  Dine_ID         varchar(50) not null, " \
                    r"  busiDate        varchar(10) not null, " \
                    r"  app_billno      varchar(50) not null, " \
                    r"  primary key ( Dine_ID, busiDate, app_billno ) ) "
            curApp.execute(lsSql)
        if bInit:
            lsSql = r"insert into interTmp ( Dine_ID, busiDate, app_billno ) " \
                    r"select DINE_ID, convert(char(10), BEGINDate, 120), salesid from Dine_sales " \
                    r"where Dine_ID = '{Dine_ID}'".format(Dine_ID=self.sett.Dine_ID)
            curApp.execute(lsSql)
        lsSql = r"select 1 from sysobjects where id=object_id('interTmp0')"
        curApp.execute(lsSql)
        res = curApp.fetchall()
        if len(res) == 0:
            lsSql = r"create table interTmp0 ( " \
                    r"  Dine_ID         varchar(50) not null, " \
                    r"  busiDate        varchar(10) not null, " \
                    r"  app_billno      varchar(50) not null, " \
                    r"  primary key ( Dine_ID, busiDate, app_billno ) ) "
            curApp.execute(lsSql)
        if bInit:
            lsSql = r"insert into interTmp0 ( Dine_ID, busiDate, app_billno ) " \
                    r"select DINE_ID, convert(char(10), BEGINDate, 120), salesid from Dine_sales " \
                    r"where DINE_ID = '{Dine_ID}' " \
                    r"and convert(char(10), BEGINDate, 120) = '{sDate}'".format(Dine_ID=self.sett.Dine_ID, sDate=lsInterBase)
            curApp.execute(lsSql)

        # 初始化单据
        if self.sBusiness != lsInterBase:
            lsSql = r"delete from interTmp0 where Dine_ID = '{Dine_ID}' ".format(Dine_ID=self.sett.Dine_ID)
            curApp.execute(lsSql)
            lsSql = r"insert into interTmp0 ( Dine_ID, busiDate, app_billno ) " \
                    r"select Dine_ID, busiDate, app_billno from interTmp " \
                    r"where Dine_ID = '{Dine_ID}' " \
                    r"and busiDate = '{sDate}' ".format(Dine_ID=self.sett.Dine_ID, sDate=self.sBusiness)
            curApp.execute(lsSql)

            lsSql = r"update sys_t_system set sys_var_value = '{sDate}' where sys_var_id = 'dInterBase'".format(sDate=self.sBusiness)
            curErp.execute(lsSql)

        # 初始化菜品等资料
        if self.sBusiness != lsInterBase or bRestart:
            self.interToApp()

        # 提交事务，关闭连接
        connErp.commit()
        connErp.close()
        connApp.commit()
        connApp.close()

    def interToApp(self):
        """
        向App写入菜品等资料，提交事务
        :return:
        """
        # 获取数据库连接
        connErp = self.dbErp.GetConnect()
        curErp = connErp.cursor()
        if not curErp:
            raise Exception("Erp端数据库连接失败")
        connApp = self.dbApp.GetConnect()
        curApp = connApp.cursor()
        if not curApp:
            raise Exception("App端数据库连接失败")

        # 查询Erp数据
        lsSql = r"select    bigcls.cBigCls_C, " \
                r"          litcls.cLitCls_C, " \
                r"          litcls.cLitCls_N " \
                r"from      c_t_food_bigCls bigcls, " \
                r"          c_t_food_litCls litcls " \
                r"where     bigcls.cBigCls_C = litcls.cBigCls_C "
        curErp.execute(lsSql)
        resCls = curErp.fetchall()
        lsSql = r"select    food.cFood_C, " \
                r"          food.sNameFast, " \
                r"          food.cFood_N, " \
                r"          food.sUnit, " \
                r"          food.nPrc, " \
                r"          bigcls.cBigCls_C, " \
                r"          litcls.cLitCls_C " \
                r"from      c_t_food food, " \
                r"          c_t_food_litCls litcls, " \
                r"          c_t_food_bigCls bigcls " \
                r"where     food.cLitCls_C = litcls.cLitCls_C " \
                r"and       litcls.cBigCls_C = bigcls.cBigCls_C " \
                r"and       food.bUse = 1 "
        curErp.execute(lsSql)
        resItem = curErp.fetchall()

        if len(resCls) > 0 and len(resItem) > 0:
            # 类别数据同步
            lsSql = r"delete from Dine_ClassSub where Dine_ID = '{Dine_ID}'".format(Dine_ID=self.sett.Dine_ID)
            curApp.execute(lsSql)
            for i in resCls:
                lsSql = r"insert into Dine_ClassSub ( CLASSID, Dine_ID, CLASSNAME ) values ( '{cBig_C}_{cLit_C}', '{Dine_ID}', '{sName}' )".format(
                    cBig_C=i[0],
                    cLit_C=i[1] + 'kmi#' + self.sett.branch_no,
                    Dine_ID=self.sett.Dine_ID,
                    sName=i[2]
                )
                curApp.execute(lsSql)

            # 菜品数据同步
            lsSql = r"update Dine_Goods set Status = 0 where Dine_ID = '{Dine_ID}'".format(Dine_ID=self.sett.Dine_ID)
            curApp.execute(lsSql)
            for i in resItem:
                lsSql = r"select 1 from Dine_Goods where goodsid = '{goodsid}' and Dine_ID = '{Dine_ID}'".format(
                    goodsid=i[0] + "kmi#" + self.sett.branch_no,
                    Dine_ID=self.sett.Dine_ID
                )
                curApp.execute(lsSql)
                res = curApp.fetchall()
                if len(res) == 0:
                    lsSql = r"insert into Dine_Goods ( goodsid, Dine_ID, goodscode, goodsname, unit, price, CLASSID, property, Status ) values ( '{goodsid}', '{Dine_ID}', '{goodscode}', '{goodsname}', '{unit}', {price}, '{cBig_C}_{cLit_C}', 0, 1 ) ".format(
                        goodsid=i[0] + "kmi#" + self.sett.branch_no,
                        Dine_ID=self.sett.Dine_ID,
                        goodscode=i[1],
                        goodsname=i[2],
                        unit=i[3],
                        price=i[4],
                        cBig_C=i[5],
                        cLit_C=i[6] + "kmi#" + self.sett.branch_no
                    )
                else:
                    lsSql = r"update Dine_Goods set goodscode='{goodscode}', goodsname='{goodsname}', unit='{unit}', price={price}, CLASSID='{cBig_C}_{cLit_C}', Status = 1 where goodsid = '{goodsid}' and Dine_ID = '{Dine_ID}' ".format(
                        goodsid=i[0] + "kmi#" + self.sett.branch_no,
                        Dine_ID=self.sett.Dine_ID,
                        goodscode=i[1],
                        goodsname=i[2],
                        unit=i[3],
                        price=i[4],
                        cBig_C=i[5],
                        cLit_C=i[6] + "kmi#" + self.sett.branch_no
                    )
                curApp.execute(lsSql)

            if 1 == 2:
                # 菜品数据同步：因删除了图片、说明等字段，改用更新的方式同步数据，如上
                lsSql = r"delete from Dine_Goods where Dine_ID = '{Dine_ID}'".format(Dine_ID=self.sett.Dine_ID)
                curApp.execute(lsSql)
                for i in resItem:
                    lsSql = r"insert into Dine_Goods ( goodsid, Dine_ID, goodscode, goodsname, unit, price, CLASSID, property, Status ) values ( '{goodsid}', '{Dine_ID}', '{goodscode}', '{goodsname}', '{unit}', {price}, '{cBig_C}_{cLit_C}', 0, 1 ) ".format(
                        goodsid=i[0],
                        Dine_ID=self.sett.Dine_ID,
                        goodscode=i[1],
                        goodsname=i[2],
                        unit=i[3],
                        price=i[4],
                        cBig_C=i[5],
                        cLit_C=i[6]
                    )
                    curApp.execute(lsSql)

        # 套餐数据同步
        lsSql = r"delete from Dine_GOODSBOM"
        curApp.execute(lsSql)
        lsSql = r"select    suit.cSuit_C, " \
                r"          suit.cFood_C, " \
                r"          suit.nQty, " \
                r"          suit.sunit " \
                r"from      c_t_food food, " \
                r"          c_t_food_suit suit " \
                r"where     food.cFood_C = suit.cSuit_C " \
                r"and       food.bUse = 1 " \
                r"order by  suit.cSuit_C asc, " \
                r"          suit.cFood_C asc "
        curErp.execute(lsSql)
        resSuit = curErp.fetchall()
        iTmp = 0
        sSuit = ""
        for i in resSuit:
            iTmp += 1
            lsSql = r"insert into Dine_GOODSBOM ( TableID, goodsid, GOODSIDS, Qty, Unit ) values ( '{TableID}', '{goodsid}', '{GOODSIDS}', {Qty}, '{Unit}' ) ".format(
                TableID=("0" + str(iTmp))[-2:],
                goodsid=i[0] + "kmi#" + self.sett.branch_no,
                GOODSIDS=i[1] + "kmi#" + self.sett.branch_no,
                Qty=i[2],
                Unit=i[3]
            )
            curApp.execute(lsSql)
            if i[0] != sSuit:
                lsSql = r"update Dine_Goods set property = 1 where goodsid = '{goodsid}' ".format(goodsid=i[0] + "kmi#" + self.sett.branch_no)
                curApp.execute(lsSql)
                sSuit = i[0]

        # 口味数据同步
        lsSql = r"delete from Dine_cooknote where Dine_ID = '{Dine_ID}'".format(Dine_ID=self.sett.Dine_ID)
        curApp.execute(lsSql)
        lsSql = r"select cMade_C, cMade_N, cMadeCls from f_t_made"
        curErp.execute(lsSql)
        resMadeGroup = curErp.fetchall()
        for i in resMadeGroup:
            lsSql = r"insert into Dine_cooknote ( COOKNOTEID, Dine_ID, COOKNOTENAME, COOKNOTEGID ) values ( '{COOKNOTEID}', '{Dine_ID}', '{COOKNOTENAME}', '{COOKNOTEGID}' ) ".format(
                COOKNOTEID=i[0] + "kmi#" + self.sett.branch_no,
                Dine_ID=self.sett.Dine_ID,
                COOKNOTENAME=i[1],
                COOKNOTEGID=i[2]
            )
            curApp.execute(lsSql)

        # 菜品口味数据同步
        lsSql = r"delete from Dine_GoodsCookNote"
        curApp.execute(lsSql)
        lsSql = r"select cFood_C, cMade from c_t_food_made"
        curErp.execute(lsSql)
        resMadeGroup = curErp.fetchall()
        iTmp = 0
        for i in resMadeGroup:
            iTmp += 1
            lsSql = r"insert into Dine_GoodsCookNote ( TableID, GoodsID, COOKNOTEID ) values ( '{TableID}', '{GoodsID}', '{COOKNOTEID}' ) ".format(
                TableID=("0000" + str(iTmp))[-4:],
                GoodsID=i[0] + "kmi#" + self.sett.branch_no,
                COOKNOTEID=i[1] + "kmi#" + self.sett.branch_no
            )
            curApp.execute(lsSql)

        # 提交事务，关闭连接
        connErp.close()
        connApp.commit()
        connApp.close()

    def interToErp(self):
        """
        向Erp写入账单数据，提交事务
        :return:
        """
        # 获取数据库连接
        connErp = self.dbErp.GetConnect()
        curErp = connErp.cursor()
        if not curErp:
            raise Exception("Erp端数据库连接失败")
        connApp = self.dbApp.GetConnect()
        curApp = connApp.cursor()
        if not curApp:
            raise Exception("App端数据库连接失败")

        # 获取App单据号数组，判断条件：App单据日期=Erp当前营业日期，且没有传输过
        lsSql = r"select        Dine_ID, " \
                r"              SALESID, " \
                r"              PEOPLE, " \
                r"              TEL, " \
                r"              convert(char(10), BEGINDate, 120) + right(convert(char(19), BEGINTIME, 120), 9), " \
                r"              convert(char(19), CREATED_TIME, 120), " \
                r"              AMTGOODS, " \
                r"              AMTAR, " \
                r"              SALESCODE " \
                r"from          Dine_sales " \
                r"where         Dine_ID = '{Dine_ID}' " \
                r"and           convert(char(10), BEGINDate, 120) = '{sDate}' " \
                r"and           status = 1 " \
                r"and           SALESID not in ( select app_billno from interTmp0 where Dine_ID = '{Dine_ID}' and busiDate = '{sDate}' ) " \
                r" ".format(Dine_ID=self.sett.Dine_ID, sDate=self.sBusiness)
        curApp.execute(lsSql)
        resBill = curApp.fetchall()

        if len(resBill) > 0:
            # 逐单插入
            for i in resBill:
                # 插入主表
                lsSql = r"insert into wx_t_order_master0 ( branch_no, dBusiness, orderid, status, tabnumber, people, mobile, storeid, diningtime, createtime, " \
                        r"totalprice, realprice, contact, promotioninfo, sitem, cServiceMan, ordertype, sPayType, nServiceFee, nDisRate, nDisAmt, DoggyBoxPrice, autoTurnBill, autosettle, nflag, bVipPrc, billSource, thirdOrderNo ) " \
                        r"values( '{branch_no}', '{dBusiness}', '{orderid}', 10, '{tabnumber}', {people}, '{mobile}', '{storeid}', '{diningtime}', '{createtime}', " \
                        r"{totalprice}, {realprice}, '0', '', '请查看日志', '', 4, '6', 0.00, {nDisRate}, {nDisAmt}, 0.00, 1, 1, 0, 0, '', '{thirdOrderNo}' ) ".format(
                    branch_no=self.sett.branch_no,
                    dBusiness=self.sBusiness,
                    orderid=i[1],
                    tabnumber=self.sett.tabnumber,
                    people=i[2],
                    mobile=i[3],
                    storeid=self.sett.branch_no,
                    diningtime=i[4],
                    createtime=i[5],
                    totalprice=i[6],
                    realprice=i[7],
                    nDisRate=round(i[7]/i[6] if i[6] != 0 else 1.00, 2),
                    nDisAmt=(i[6] - i[7]),
                    thirdOrderNo=i[8]
                )
                curErp.execute(lsSql)

                # 插入支付表
                lsSql = r"insert into d_t_bill_pay_alipay0 ( dBusiness, cbill_c, cbill_guid, paytype, nRequestAmt, nRealPayAmt, Result, BranchNo, paymode, autoSettle ) " \
                        r"values ( '{dBusiness}', '{cbill_c}', '01', '6', {nRequestAmt}, {nRealPayAmt}, 1, '{branch_no}', 0, 1 ) ".format(
                    dBusiness=self.sBusiness,
                    cbill_c=i[1],
                    nRequestAmt=i[7],
                    nRealPayAmt=i[7],
                    branch_no=self.sett.branch_no
                )
                curErp.execute(lsSql)

                # 插入明细表
                lsSql = r"select        Dine_salesdd.GOODSNO, " \
                        r"              Dine_salesdd.goodsid, " \
                        r"              Dine_salesdd.GOODSNAME, " \
                        r"              Dine_salesdd.QTY, " \
                        r"              Dine_salesdd.UNIT, " \
                        r"              Dine_salesdd.NOTE, " \
                        r"              Dine_salesdd.PRICE, " \
                        r"              Dine_salesdd.MEALSETFLAG " \
                        r"from          Dine_sales, " \
                        r"              Dine_salesdd " \
                        r"where         Dine_sales.SALESID = Dine_salesdd.SALESID " \
                        r"and           Dine_sales.SALESID = '{billno}' " \
                        r"and           Dine_sales.status = 1 " \
                        r"and           Dine_salesdd.status = 1 " \
                        r"order by      Dine_salesdd.Detail_ID asc " \
                        r" ".format(billno=i[1])
                curApp.execute(lsSql)
                resDetail = curApp.fetchall()
                iTmp = -1
                for j in resDetail:
                    if j[7] == -1:
                        iTmp = 0
                        sSuitFlag = "套餐"
                        sSuitBill = ""
                    elif j[7] > 0:
                        iTmp += 1
                        sSuitFlag = "子项"
                        sSuitBill = ("0" + str(iTmp))[-2:]
                    else:
                        sSuitFlag = "单品"
                        sSuitBill = ""
                    lsSql = r"insert into wx_t_order_detail0 ( dBusiness, orderid, cfoodbill, cfood_c, cfood_n, eSuitFlag, eSuitBill, nQty, sunit, sMade, nPrc, bDelete, bAdd, nExPrc ) " \
                            r"values ( '{dBusiness}', '{orderid}', '{cfoodbill}', '{cfood_c}', '{cfood_n}', '{eSuitFlag}', '{eSuitBill}', {nQty}, '{sunit}', '{sMade}', {nPrc}, 0, 0, 0.00 ) " \
                            r" ".format(
                        dBusiness=self.sBusiness,
                        orderid=i[1],
                        cfoodbill=("0" + str(j[0]))[-2:],
                        cfood_c=j[1][:-6],
                        cfood_n=j[2],
                        eSuitFlag=sSuitFlag,
                        eSuitBill=sSuitBill,
                        nQty=j[3],
                        sunit=j[4],
                        sMade=j[5],
                        nPrc=j[6]
                    )
                    curErp.execute(lsSql)

                # 标记已传输单据
                lsSql = r"insert into interTmp ( Dine_ID, busiDate, app_billno ) values ( '{Dine_ID}', '{sDate}', '{app_billno}' ) ".format(
                    Dine_ID=self.sett.Dine_ID,
                    sDate=self.sBusiness,
                    app_billno=i[1]
                )
                curApp.execute(lsSql)
                lsSql = r"insert into interTmp0 ( Dine_ID, busiDate, app_billno ) values ( '{Dine_ID}', '{sDate}', '{app_billno}' ) ".format(
                    Dine_ID=self.sett.Dine_ID,
                    sDate=self.sBusiness,
                    app_billno=i[1]
                )
                curApp.execute(lsSql)

        # 提交事务，关闭连接
        connErp.commit()
        connErp.close()
        connApp.commit()
        connApp.close()
