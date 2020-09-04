# -*- coding:utf-8 -*-
"""
数据对接控制类
数据操作标准返回值结构：
{
    "result":True/False,            # 逻辑控制
    "dataString":"",                # 字符串
    "dataNumber":0,                 # 数字
    "info":"",                      # 信息
    "entities":{                    # 表体集
        "item":{
            "subItem":[(            # 表体代码
                    recordNo,       # 记录标识 可能是字符串或数字
                    recordName,     # 记录名称/备注
                    recordBranch,   # 记录名称/备注
                    recordDate      # 记录日期 可能为空字符串
                )
            ]
        }
    }
}
"""
__author__ = "Cliff.wang"
from datetime import datetime, timedelta
from interMssql import MSSQL


class InterControl():

    def __init__(self, sett):
        """
        接口控制类
        """
        self.sett = sett

        # 业务前端定义
        if self.sett.frontCode == "KMHCM":
            from frontKemaiHcmDb import FrontKemaiHcmDb
            self.front = FrontKemaiHcmDb(sett, "front")
        elif self.sett.frontCode == "KMTTYS":
            from frontKemaiTtysDb import FrontKemaiTtysDb
            self.front = FrontKemaiTtysDb(sett, "front")
        else:
            raise Exception("非法的前端营业系统代码[{frontCode}]".format(frontCode=self.sett.frontCode))

        # 业务后端定义
        if self.sett.backCode == "Testdb":
            from backTestDb import BackTestDb
            self.back = BackTestDb(sett, "back")
        elif self.sett.backCode == "Kingdee":
            from backKingdeeWeb import BackKingdeeWeb
            self.back = BackKingdeeWeb(sett, "back")
        else:
            raise Exception("非法的后端营业系统代码[{backCode}]".format(backCode=self.sett.backCode))

        # 对接内容定义：{"item", "saleBill", "accBill"}
        self.interItemsBase = {"item"}
        self.interItemsBusi = {"saleBill", "accBill"}

        self.interConn = {}
        self.interConn["host"] = self.sett.controlHost
        self.interConn["user"] = self.sett.controlUser
        self.interConn["password"] = self.sett.controlPwd
        self.interConn["database"] = self.sett.controlDb
        self.db = MSSQL(self.interConn["host"], self.interConn["user"], self.interConn["password"], self.interConn["database"])
        self.sett.logger.info("数据对象初始化成功")

    def interInit(self):
        """
        控制初始化
        :return:
        """
        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("初始化失败：控制数据库[{db}]连接失败".format(db=self.interConn["database"]))

        # 创建标志表
        lsSql = r"select 1 from sysobjects where xtype = 'U' and id = OBJECT_ID('InterControl')"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            # 创建门店控制表
            lsSql = r"create table InterControl ( " \
                    r"  Id          varchar(100)    not null, " \
                    r"  Name        varchar(100)    not null, " \
                    r"  Value       varchar(100)    not null, " \
                    r"  Description varchar(255)    null, " \
                    r"  primary key ( Id ) ) "
            cur.execute(lsSql)

        # 对接日期
        lsSql = r"select Value from InterControl where Id = 'dInter'"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            # 插入参数
            initDate = datetime.strftime(datetime.today(), "%Y-%m-%d")
            lsSql = r"insert into InterControl ( Id, Name, Value, Description ) " \
                    r"values ( 'dInter', 'Kemai-Kingdee接口启动日期', '{curDate}', '用于Kingdee接口' )".format(curDate=initDate)
            cur.execute(lsSql)
        # 条码控制（金蝶接口强制要求必须有6位条码，在此以自增数字代替）
        lsSql = r"select Value from InterControl where Id = 'maxBarcode'"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            # 插入参数
            lsSql = r"insert into InterControl ( Id, Name, Value, Description ) " \
                    r"values ( 'maxBarcode', '条码控制', '0', '用于适应接口对条码的强制要求' )"
            cur.execute(lsSql)
            self.sett.maxBarcode = 0
        else:
            self.sett.maxBarcode = int(rs[0][0])

        # 创建接口门店表
        lsSql = r"select 1 from sysobjects where xtype = 'U' and id = OBJECT_ID('InterBranch')"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            # 创建门店控制表
            lsSql = r"create table InterBranch ( " \
                    r"  branchNo        varchar(20) not null, " \
                    r"  branchName      varchar(60) not null, " \
                    r"  interDate       varchar(10) not null, " \
                    r"  status          int         not null, " \
                    r"  primary key ( branchNo ) ) "
            cur.execute(lsSql)

        # 创建对接数据控制表
        lsSql = r"select 1 from sysobjects where xtype = 'U' and id = OBJECT_ID('InterCompleted')"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            # 创建门店控制表
            lsSql = r"create table InterCompleted ( " \
                    r"  dataID          int not null IDENTITY(1,1), " \
                    r"  dataType        varchar(50) not null, " \
                    r"  sNumber         varchar(60) null, " \
                    r"  iNumber         bigint null, " \
                    r"  sName           varchar(100) not null, " \
                    r"  sBranch         varchar(20) not null, " \
                    r"  sDate           varchar(10) not null, " \
                    r"  primary key ( dataID ) ) "
            cur.execute(lsSql)

        # 提交事务，关闭连接
        conn.commit()
        conn.close()

        # 前后端接口初始化
        self.front.interInit()
        self.back.interInit()

    def getDataCompleted(self, sItem, sBranch, sFrom, sTo):
        """
        获取已对接的数据
        :param sItem:                       # 数据项
        :param sBranch:                     # 门店
        :param sFrom:                       # 开始日期
        :param sTo:                         # 截至日期
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                sItem: {                    # 表体代码
                    sItem:[]
                }
            }
        }

        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("初始化失败：控制数据库[{db}]连接失败".format(db=self.interConn["database"]))

        # 获取数据
        lsSql = r"select    sNumber, " \
            r"          iNumber, " \
            r"          sName, " \
            r"          sBranch, " \
            r"          sDate " \
            r"from      InterCompleted " \
            r"where     dataType = '{sItem}' " \
            r"and       sBranch = '{sBranch}' " \
            r"and       sDate >= '{sFrom}' " \
            r"and       sDate <= '{sTo}' " \
            "".format(
            sItem = sItem,
            sBranch = sBranch,
            sFrom = sFrom,
            sTo = sTo
        )
        cur.execute(lsSql)
        rsData = cur.fetchall()
        rtnData["result"] = True
        for i in rsData:
            if i[0]:
                rtnData["entities"][sItem][sItem].append((i[0], i[2], i[3], i[4]))
            else:
                rtnData["entities"][sItem][sItem].append((i[1], i[2], i[3], i[4]))

        return rtnData

    def putDataCompleted(self, putData):
        """
        更新已对接的数据
        :param putData:
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }
        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("初始化失败：控制数据库[{db}]连接失败".format(db=self.interConn["database"]))

        for i in putData["entities"]:
            rtnData["entities"][i] = {}
            for j in putData["entities"][i]:
                rtnData["entities"][i][j] = []
                for k in putData["entities"][i][j]:
                    if type(k[0]) == type("aa"):
                        sNumber = k[0]
                        iNumber = "null"
                    else:
                        sNumber = ""
                        iNumber = k[0]
                    lsSql = r"insert into InterCompleted ( dataType, sNumber, iNumber, sName, sBranch, sDate ) " \
                        r"values ( '{dataType}', '{sNumber}', {iNumber}, '{sName}', '{sBranch}', '{sDate}' ) " \
                        "".format(
                        dataType=i,
                        sNumber=sNumber,
                        iNumber=iNumber,
                        sName=k[1],
                        sBranch=k[2],
                        sDate=k[3]
                    )
                    cur.execute(lsSql)
                    rtnData["entities"][i][j].append(k)

        # 金蝶菜品接口特殊处理
        if self.back.interCode == "Kingdee" and "item" in putData["entities"]:
            lsSql = r"update InterControl set Value = '{maxBarcode}' where Id = 'maxBarcode'".format(maxBarcode=self.sett.maxBarcode)
            cur.execute(lsSql)

        # 关闭连接
        conn.commit()
        conn.close()

        rtnData["result"] = True
        return rtnData

    def interBranchs(self):
        """
        更新门店信息
        :return:
        """
        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("基础数据获取失败：控制数据库[{db}]连接失败".format(db=self.interConn["database"]))

        # 获取全部门店信息
        rsBranchs = self.front.getBranchs()["entities"]["branch"]["branch"]
        sBranchsID = set([i[0] for i in rsBranchs])

        # 获取已存在门店信息
        lsSql = r"select branchNo, branchName from InterBranch where status = 1"
        cur.execute(lsSql)
        rsExists = cur.fetchall()
        sExistsID = set([i[0] for i in rsExists])

        # 更新门店信息状态
        sDel = sExistsID - sBranchsID
        for i in sDel:
            lsSql = r"update InterBranch set status = 0 where branchNo = '{ID}'".format(ID=i)
            cur.execute(lsSql)

        # 新增门店
        sNew = sBranchsID - sExistsID
        lastDate = datetime.strftime(datetime.today() + timedelta(days=-1), "%Y-%m-%d")
        sInfo = ""
        for i in sNew:
            branchName = ""
            for j in rsBranchs:
                if i == j[0]:
                    branchName = j[1]
                    break
            lsSql = r"insert into InterBranch ( branchNo, branchName, interDate, status ) " \
                    r"values( '{ID}', '{Name}', '{sDate}', 1 ) " \
                    r"".format(ID=i, Name=branchName, sDate=lastDate)
            cur.execute(lsSql)
            sInfo += "," + i
        if sInfo != "":
            sInfo = sInfo[1:]
            self.sett.logger.info("增加{n}个门店：{s}".format(n=len(sNew), s=sInfo))

        # 关闭连接
        conn.commit()
        conn.close()

    def interBaseData(self):
        """
        基础资料对接
        :return:
        """
        # 获取数据范围
        itemsRange = self.interItemsBase & self.front.interItems & self.back.interItems

        # 计算需要对接的数据
        for key in itemsRange:
            # 取出数据
            if self.front.interBase == "out":
                getData = self.front.getBaseData(key)
            else:
                getData = self.back.getBaseData(key)

            # 获取已对接的数据
            dataCompleted = self.getDataCompleted(key, "", "", "")
            if key in dataCompleted["entities"] and key in getData["entities"]:
                for i in dataCompleted["entities"][key][key]:
                    for j in getData["entities"][key][key]:
                        if i[0] == j[0]:
                            getData["entities"][key][key].remove(j)
                            break

            # 保存数据
            if len(getData["entities"][key][key]) > 0:
                self.sett.logger.info("准备导入{item}数据{num}条……".format(item=key, num=len(getData["entities"][key][key])))
                if self.back.interBase == "in":
                    putData = self.back.putBaseData(getData)
                else:
                    putData = self.front.putBaseData(getData)

                # 更新历史记录
                self.putDataCompleted(putData)

                # 显示日志
                for i in putData["entities"]["item"]:
                    if i == "item":
                        name = "菜品档案"
                    else:
                        name = i
                    self.sett.logger.info("成功导入[{item}]{num}条.".format(item=i, num=len(putData["entities"]["item"][i])))

    def interBusiData(self):
        """
        销售单据对接
        对接对象：{"saleBill","accBill"}
        :return:
        """
        self.sett.logger.info("开始导入业务数据……")

        # 获取数据范围
        itemsRange = self.interItemsBusi & self.front.interItems & self.back.interItems

        # 更新门店信息
        self.interBranchs()

        # 基础信息同步
        self.interBaseData()

        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("业务数据对接失败：控制数据库[{db}]连接失败".format(db=self.interConn["database"]))

        # 获取处理最大日期
        dPoint = datetime.today() + timedelta(days=self.sett.timingBusiDay * -1)
        sTo = datetime.strftime(dPoint, "%Y-%m-%d")

        # 各门店循环处理
        lsSql = r"select branchNo, branchName, interDate from InterBranch " \
                r"where interDate < '{processDate}' " \
                r"order by branchNo ".format(processDate=sTo)
        cur.execute(lsSql)
        rsBranch = cur.fetchall()
        for i in rsBranch:
            if i[0] in self.sett.org:
                orgID = self.sett.org[i[0]]
            else:
                # raise Exception("请在参数中配置[{front}]机构[{branch}]的应的[{back}]机构ID.".format(front=self.sett.frontName, branch=i[1], back=self.sett.backName))
                # 没有配置对应关系的门店不对接，继续执行其他门店
                self.sett.logger.info("[{end}]的门店[{branch}]没有配置对应关系.".format(end=self.sett.frontName, branch=i[0]))
                continue

            # 初始化对接日期
            interDate = ""
            # 初始化对接结果
            interResult = True

            # 获取开始日期
            sFrom = datetime.strftime(datetime.strptime(i[2], "%Y-%m-%d") + timedelta(days=1), "%Y-%m-%d")

            # 获得新增的数据
            for key in itemsRange:
                # 取出数据
                getData = self.front.getBusiData(key, i[0], sFrom, sTo)

                # 获取已对接的数据
                dataCompleted = self.getDataCompleted(key, i[0], sFrom, sTo)
                if key in dataCompleted["entities"] and key in getData["entities"]:
                    for l in dataCompleted["entities"][key][key]:
                        for m in getData["entities"][key]["bill"]:
                            if m[0] == l[0]:
                                getData["entities"][key]["bill"].remove(m)
                                list1 = []
                                for n in getData["entities"][key]["item"]:
                                    if n[0] == l[0]:
                                        list1.append(n)
                                for n in list1:
                                    getData["entities"][key]["item"].remove(n)
                                list2 = []
                                for o in getData["entities"][key]["pay"]:
                                    if o[0] == l[0]:
                                        list2.append(o)
                                for o in list2:
                                    getData["entities"][key]["pay"].remove(o)
                                break

                if len(getData["entities"][key]["bill"]) > 0:
                    # 保存数据
                    putData = self.back.putBusiData(orgID, getData)

                    if not putData["result"]:
                        interResult = False

                    if putData["result"] and getData["dataString"] > interDate:
                        interDate = getData["dataString"]

                    # 记录对接历史
                    self.putDataCompleted(putData)

                    # 记录日志
                    for itemType in putData["entities"]:
                        if itemType == "saleBill":
                            name = "菜品销售单"
                        elif itemType == "accBill":
                            name = "财务记账单"
                        else:
                            name = itemType
                        self.sett.logger.info("成功导入[{item}]{num}条.".format(item=name, num=len(putData["entities"][itemType]["bill"])))

            # 记录断点
            if interResult and interDate != "":
                lsSql = r"update    InterBranch " \
                        r"set       interDate = '{updateDate}' " \
                        r"where     branchNo = '{branchno}' " \
                        r"".format(updateDate=interDate, branchno=i[0])
                cur.execute(lsSql)
                conn.commit()

        # 关闭连接
        conn.close()
        self.sett.logger.info("业务数据导入结束.")
