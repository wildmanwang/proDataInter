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
import datetime
import json


class InterControl():

    def __init__(self, sett):
        """
        接口控制类
        """
        self.sett = sett

        if self.sett.appType == "Hongshang":
            from frontHongshang import FrontHongshang
            self.front = FrontHongshang(self.sett)
        else:
            raise Exception("收银系统类型{appType}不支持.".format(FrontHongshang=self.sett.appType))

        self.interConn = {}
        self.interConn["host"] = self.sett.controlHost
        self.interConn["user"] = self.sett.controlUser
        self.interConn["password"] = self.sett.controlPwd
        self.interConn["database"] = self.sett.controlDb
        self.db = MSSQL(self.interConn["host"], self.interConn["user"], self.interConn["password"], self.interConn["database"])
        self.sett.logger.info("控制端数据对象初始化成功")
        self.interInit()

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

        # 创建参数表
        lsSql = r"select 1 from sysobjects where xtype = 'U' and id = OBJECT_ID('busiParas')"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            lsSql = r"create table busiParas ( " \
                    r"  sCode           varchar(50) not null, " \
                    r"  sName           varchar(50) not null, " \
                    r"  sValue          varchar(50) null, " \
                    r"  sRemark         varchar(60) null " \
                    r"  primary key ( sCode ) ) "
            cur.execute(lsSql)
            dTo = datetime.datetime.now()
            sTo = datetime.datetime.strftime(dTo, "%Y-%m-%d") + " 00:00:00"
            lsSql = r"insert into busiParas ( sCode, sName, sValue, sRemark ) values ( 'order_downline', '订单下载截至时间', '{sTime}', '')".format(
                sTime=sTo
            )
            cur.execute(lsSql)
            conn.commit()

        # 创建对接数据控制表
        lsSql = r"select 1 from sysobjects where xtype = 'U' and id = OBJECT_ID('InterCompleted')"
        cur.execute(lsSql)
        rs = cur.fetchall()
        if len(rs) == 0:
            lsSql = r"create table InterCompleted ( " \
                    r"  cID             int not null IDENTITY(1,1), " \
                    r"  busiType        varchar(50) not null, " \
                    r"  dataType        varchar(50) not null, " \
                    r"  sNumber         varchar(60) null, " \
                    r"  iNumber         bigint null, " \
                    r"  sRelated        varchar(60) not null, " \
                    r"  sName           varchar(100) not null, " \
                    r"  sBranch         varchar(20) not null, " \
                    r"  sTime           varchar(19) not null, " \
                    r"  primary key ( cID ) ) "
            cur.execute(lsSql)

        # 提交事务，关闭连接
        conn.commit()
        conn.close()

    def _getPara(self, sCode):
        """
        获取参数
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        try:
            conn = self.db.GetConnect()
            cur = conn.cursor()
            if not cur:
                raise Exception("参数获取失败：{name}数据库[{db}]连接失败".format(name=self.interName, db=self.interConn["database"]))
            lsSql = r"select sValue from busiParas where sCode = 'order_downline'"
            cur.execute(lsSql)
            dsTmp = cur.fetchall()
            if len(dsTmp) > 0:
                rtnData["dataString"] = dsTmp[0][0]
            else:
                rtnData["result"] = False
        except Exception as e:
            rtnData["result"] = False
            rtnData["info"] = str(e)

        return rtnData

    def _putPara(self, sCode, sValue):
        """
        更新参数
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        try:
            conn = self.db.GetConnect()
            cur = conn.cursor()
            if not cur:
                raise Exception("参数更新失败：{name}数据库[{db}]连接失败".format(name=self.interName, db=self.interConn["database"]))
            lsSql = r"select sValue from busiParas where sCode = 'order_downline'"
            cur.execute(lsSql)
            dsTmp = cur.fetchall()
            if len(dsTmp) == 0:
                lsSql = r"insert into busiParas ( sCode, sName, sValue, sRemark ) values( '{sCode}', '', '{sValue}', '' )".format(
                    sCode=sCode,
                    sValue=sValue
                )
            else:
                lsSql = r"update busiParas set sValue = '{sValue}' where sCode = '{sCode}'".format(
                    sCode=sCode,
                    sValue=sValue
                )
            cur.execute(lsSql)
            conn.commit()
        except Exception as e:
            rtnData["result"] = False
            rtnData["info"] = str(e)

        return rtnData

    def getDataCompleted(self, sType, sBranch, sFrom, sTo):
        """
        获取已对接的数据
        :param sType:                       # 数据项 item/order
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
                sType: []
            }
        }

        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            raise Exception("初始化失败：控制数据库[{db}]连接失败".format(db=self.interConn["database"]))

        # 获取数据
        lsSql = r"select    dataType, " \
            r"          sNumber, " \
            r"          iNumber, " \
            r"          sRelated, " \
            r"          sName, " \
            r"          sBranch, " \
            r"          sTime " \
            r"from      InterCompleted " \
            r"where     busiType = '{sType}' " \
            r"and       sBranch = '{sBranch}' " \
            "".format(
            sType = sType,
            sBranch = sBranch
        )
        if sType not in ["item"]:
            lsSql += r" and sTime >= '{sFrom}' and sTime <= '{sTo}' ".format(
                sFrom=sFrom,
                sTo=sTo
            )
        cur.execute(lsSql)
        rsData = cur.fetchall()
        rtnData["result"] = True
        for i in rsData:
            rtnData["entities"][sType].append({
                "type": sType,
                "code": i[1] if i[0] == "S" else i[2],
                "related": i[3],
                "name": i[4],
                "branch": i[5],
                "date": i[6]
            })

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
            rtnData["entities"][i] = []
            for k in putData["entities"][i]:
                lsSql = r"select dataType from InterCompleted where busiType='{busiType}'".format(busiType=i)
                if type(k["code"]) == type("aa"):
                    dataType = "S"
                    iNumber = "null"
                    sNumber = k["code"]
                    lsSql += r" and sNumber='{code}'".format(code=sNumber)
                else:
                    sNumber = ""
                    dataType = "N"
                    iNumber = k["code"]
                    lsSql += r" and iNumber={code}".format(code=sNumber)
                lsSql += r" and sBranch='{branch}'".format(branch=self.sett.defaultOrgNo)
                cur.execute(lsSql)
                rsTmp = cur.fetchall()
                if len(rsTmp) == 0:
                    lsSql = r"insert into InterCompleted ( busiType, dataType, sNumber, iNumber, sRelated, sName, sBranch, sTime ) " \
                        r"values ( '{busiType}', '{dataType}', '{sNumber}', {iNumber}, '{sRelated}', '{sName}', '{sBranch}', '{sTime}' ) " \
                        r"".format(
                            busiType=k["type"],
                            dataType=dataType,
                            sNumber=sNumber,
                            iNumber=iNumber,
                            sRelated=k["related"],
                            sName=k["name"],
                            sBranch=self.sett.defaultOrgNo,
                            sTime=k["time"]
                        )
                    cur.execute(lsSql)
                    rtnData["entities"][i].append(k)

        # 关闭连接
        conn.commit()
        conn.close()

        rtnData["result"] = True
        return rtnData

    def interBaseData(self):
        """
        基础资料对接
        :return:
        """
        rtnData = {
            "result": True,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 1,  # 数字
            "info": "",  # 信息
            "entities": {}
        }
        bContinue = True

        # 取出数据
        getData = self.front.getItems("")

        # 获取已对接的数据
        if 1 == 2:          # 基础资料允许重复上传，用于更新数据
            dataCompleted = self.getDataCompleted("item", self.sett.defaultOrgNo, "", "")
            if dataCompleted["result"]:
                for i in dataCompleted["entities"]["item"]:
                    for j in getData["entities"]["item"]:
                        if i["code"] == j["out_goods_id"]:
                            getData["entities"]["item"].remove(j)
                            break
            else:
                bContinue = False
                rtnData["info"] = dataCompleted["info"]

        # 保存数据
        if bContinue and len(getData["entities"]["item"]) > 0:
            putData = self.putItems(getData)
            if not putData["result"]:
                bContinue = False
                rtnData["info"] = putData["info"]

            # 更新历史记录
            if bContinue:
                rtnTmp = self.putDataCompleted(putData)
                if not rtnTmp:
                    bContinue = False
                    rtnData["info"] = rtnTmp["info"]

            # 显示日志
            if len(putData["entities"]["item"]) > 0:
                self.sett.logger.info("成功导入商品数据{num}条.".format(num=len(rtnTmp["entities"]["item"])))

        if not bContinue:
            rtnData["result"] = False

        return rtnData

    def interBusiData(self):
        """
        业务单据对接
        :return:
        """
        rtnData = {
            "result": True,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 1,  # 数字
            "info": "",  # 信息
            "entities": {}
        }
        bContinue = True

        # 获取数据库连接
        conn = self.db.GetConnect()
        cur = conn.cursor()
        if not cur:
            bContinue = False
            rtnData["result"] = False
            rtnData["info"] = "业务数据对接失败：控制数据库[{db}]连接失败".format(db=self.interConn["database"])

        # 获取上次已下载订单的截至时间
        if bContinue:
            rtnTmp = self._getPara("order_downline")
            if rtnTmp["result"]:
                sFrom = rtnTmp["dataString"]
                # 本次下载订单截至时间
                dTo = datetime.datetime.now() - datetime.timedelta(minutes=1)
                sTo = datetime.datetime.strftime(dTo, "%Y-%m-%d %H:%M:%S")
            else:
                bContinue = False
                rtnData["result"] = False
                rtnData["info"] =  rtnTmp["info"]

        # 取出数据
        if bContinue:
            getData = self.getOrders(sFrom, sTo)
            if getData["result"]:
                pass
            else:
                bContinue = False
                rtnData["result"] = False
                rtnData["info"] = rtnTmp["info"]

        # 获取已对接的数据
        if bContinue:
            dataCompleted = self.getDataCompleted("order", self.sett.defaultOrgNo, sFrom, sTo)
            if dataCompleted["result"]:
                for l in dataCompleted["entities"]["order"]:
                    for m in getData["entities"]["order"]:
                        if m["order_id"] == l["code"]:
                            getData["entities"]["order"].remove(m)
                            break
            else:
                bContinue = False
                rtnData["result"] = False
                rtnData["info"] = rtnTmp["info"]

        if bContinue:
            if len(getData["entities"]["order"]) > 0:
                # 保存数据
                putData = self.front.putOrders(getData)
                if not putData["result"]:
                    bContinue = False
                    rtnData["result"] = False
                    rtnData["dataNumber"] = len(putData["entities"]["order"])
                    rtnData["info"] = rtnTmp["info"]

                # 记录对接历史
                if bContinue:
                    rtnTmp = self.putDataCompleted(putData)
                    if rtnTmp["result"]:
                        rtnData["entities"]["order"] = rtnTmp["entities"]["order"]
                    else:
                        rtnData["result"] = False
                        rtnData["info"] = rtnTmp["info"]
            else:
                rtnData["dataNumber"] = 0
                rtnData["info"] = rtnTmp["info"]

        # 记录日志
        if rtnData["result"]:
            self.sett.logger.info("成功下载订单{num}条.".format(num=rtnData["dataNumber"]))
            self._putPara("order_downline", sTo)
        else:
            self.sett.logger.error("下载订单失败：{info}".format(info=rtnData["info"]))

        # 关闭连接
        conn.close()

        return rtnData

    def _getSign(self, pData):
        """
        获取接口签名
        """
        rtnData = {
            "result": True,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 1,  # 数字
            "info": "",  # 信息
        }
        import hashlib

        try:
            lPara = sorted(pData.items(), key=lambda x: x[0]) # 字典有两层，处理排序错误
            sSource = ""
            for gitem in lPara:
                if len(sSource) > 0:
                    sSource += "&"
                if gitem[0] == "price":
                    sSource += 'price={"price":' + str(gitem[1]["price"])
                    sSource += ',"original_price":' + str(gitem[1]["original_price"]) + "}"
                else:
                    sSource += str(gitem[0]) + "=" + str(gitem[1])
            sSource += "&appsecret=" + self.sett.appsecret
            sSign = hashlib.md5(sSource.encode(encoding='UTF-8')).hexdigest()
            sSign = sSign.upper()
            rtnData["dataString"] = sSign
        except Exception as e:
            rtnData["result"] = False
            rtnData["info"] = str(e)

        return rtnData

    def putItems(self, putData):
        """
        上传商品
        """
        rtnData = {
            "result": True,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 1,  # 数字
            "info": "",  # 信息
            "entities": {
                "item": []
            }
        }

        iCnt = len(putData["entities"]["item"])
        iNum = 0
        for line in putData["entities"]["item"]:
            pItems = {
                "out_goods_id":     line["out_goods_id"],
                "goods_name":       line["goods_name"],
                "logo":             line["logo"],
                "master_picture":   line["master_picture"],
                "pictures":         line["pictures"],
                "description":      line["description"],
                "comment":          line["comment"],
                "stock":            line["stock"],
                "virtual_sales":    line["virtual_sales"],
                "limited_sale":     line["limited_sale"],
                "limited_single":   line["limited_single"],
                "extra":            line["extra"],
                "cost":             round(line["cost"] * 100),
                "postage":          round(line["postage"] * 100),
                "postage_type":     line["postage_type"],
                "unit":             line["unit"],
                "price": {
                    "price":            round(line["price"] * 100),
                    "original_price":   round(line["original_price"] * 100)
                },
                "pickup":           line["pickup"],
                "pickup_delay_time": line["pickup_delay_time"],
                "pickup_start_time": line["pickup_start_time"],
                "pickup_end_time":  line["pickup_end_time"],
                "sort":             line["sort"],
                "start_time":       line["start_time"],
                "end_time":         line["end_time"],
            }
            rtnTmp = self._getSign(pItems)
            if rtnTmp["result"]:
                sSign = rtnTmp["dataString"]
            else:
                raise Exception(rtnTmp["info"])
            sUrl = "{url}/mch/goods/upload?app_id={app_id}&sign={sign}".format(
                url=self.sett.interUrl,
                app_id=self.sett.appid,
                sign=sSign
            )
            import requests
            headers = {'Content-Type': 'application/json'}
            res = requests.post(url=sUrl, headers=headers, json=pItems)
            res = json.loads(res.text)
            if res["code"] == "10000":
                rtnData["entities"]["item"].append({
                    "type": "item",
                    "code": line["out_goods_id"],
                    "related": res["data"]["goods_id"],
                    "name": line["goods_name"],
                    "time": datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                })
                iNum += 1
            else:
                rtnData["result"] = False
                rtnData["info"] = res["message"]
                break

        rtnData["info"] += "上传了{num}/{cnt}商品".format(
            num=iNum,
            cnt=iCnt
        )

        return rtnData

    def getOrders(self, sFrom, sTo):
        """
        获取线上订单
        """
        rtnData = {
            "result": True,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 1,  # 数字
            "info": "",  # 信息
            "entities": {
                "order": []
            }  # 表体集
        }

        iPage = 0
        iCnt = 1
        while iPage < iCnt:
            iPage += 1
            pCondition = {
                "page": iPage,
                "pageSize": 100,
                "startTime": sFrom,
                "endTime": sTo,
                "searchWord": "",
                "searchKey": "",
                "order": "order_id asc"
            }
            rtnTmp = self._getSign(pCondition)
            if rtnTmp["result"]:
                sSign = rtnTmp["dataString"]
            else:
                raise Exception(rtnTmp["info"])
            sUrl = "{url}/trade/sale/order/list?app_id={app_id}&sign={sign}".format(
                url=self.sett.interUrl,
                app_id=self.sett.appid,
                sign=sSign
            )
            import requests
            headers = {'Content-Type': 'application/json'}
            res = requests.post(url=sUrl, headers=headers, json=pCondition)
            res = json.loads(res.text)
            if res["code"] == "10000":
                # 这里要分页接收数据
                rtnData["entities"]["order"].extend(res["data"]["data"])
                iPage = res["data"]["currentPage"]
                iCnt = res["data"]["totalPages"]
            else:
                rtnData["result"] = False
                rtnData["info"] = res["message"]
                break

        if len(rtnData["entities"]["order"]) > 0:
            dsItems = self.getDataCompleted("item", self.sett.defaultOrgNo, "", "")
        for bill in rtnData["entities"]["order"]:
            for goods in bill["goodses"]:
                sOnline = goods["goods_id"]
                lFind =[line for line in dsItems["entities"]["item"] if line["related"] == sOnline]
                if len(lFind) > 0:
                    sOffline = lFind[0]["code"]
                else:
                    raise Exception("小程序商品[{code}-{name}]在POS中找不到对应的商品.".format(code=sOnline, name=goods["goods_name"]))
                goods["related"] = sOffline

        return rtnData

if __name__ == "__main__":
    from interConfig import Settings

    try:
        sett = Settings()
        inter = InterControl(sett)
        # rtn = inter.front.getItems()                  # OK
        # rtn = inter.putItems(rtn)                     # OK
        # rtn = inter.interBaseData()                     # OK
        rtn = inter.interBusiData()
        i = 1
        i += 1
    except Exception as e:
        sErr = str(e)
        i = 0
