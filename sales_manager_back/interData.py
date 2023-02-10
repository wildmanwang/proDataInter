# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from interMysql import MYSQL
import os
import json


class InterData():
    def __init__(self, sett):
        self.sett = sett
        self.db = MYSQL(self.sett.serverHost, self.sett.serverUser, self.sett.serverPwd, self.sett.serverDb)

    def user_login(self, sUser, sPwd):
        """
        用户登录
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        rtnData["result"] = True
        rtnData["entities"] = {
            "token": "admin-token"
        }

        return rtnData

    def user_info(self, sToken):
        """
        用户信息
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        rtnData["result"] = True
        rtnData["entities"] = {
            "roles": ["admin"],
            "introduction": "I am a super administrator",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            "name": "Cliff Wang"
        }

        return rtnData

    def user_logout(self):
        """
        用户登出
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        rtnData["result"] = True
        rtnData["entities"] = "success"

        return rtnData

    def basicDataList(self, sType, sQuery, sPage):
        """
        获取基础资料
        :param sType:
        category            类别
            category
        supplier            供应商
            supplier
        goods               商品
            goods
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 总记录数
            "info":"",                      # 信息
            "entities": {}
        }
        bConn = False
        ldItem = {}
        ldKey = {}
        lsTotal = ""
        try:
            if len(sQuery) > 0:
                dQuery = json.loads(sQuery)
            if len(sPage) > 0:
                dPage = json.loads(sPage)
            if sType == 'category':
                ldItem["category"] = r"select id, name, order_num, status, (case status when 1 then '正常' else '无效' end) enum_status, remark from category where 1=1"
                lsTotal = r"select count(id) from category where 1=1"
                if dQuery.get("name"):
                    ldItem["category"] += r" and name like '%{name}%'".format(name=dQuery.get("name"))
                    lsTotal += r" and name like '%{name}%'".format(name=dQuery.get("name"))
                if dQuery.get("status") >= 0:
                    ldItem["category"] += r" and status = {status}".format(status=dQuery.get("status"))
                    lsTotal += r" and status = {status}".format(status=dQuery.get("status"))
                if dPage.get("sortCol"):
                    ldItem["category"] += r" order by {sortCol} {sortType}".format(
                        sortCol=dPage["sortCol"],
                        sortType=dPage["sortType"]
                    )
                else:
                    ldItem["category"] += r" order by order_num asc, id asc"
                ldItem["category"] += r" limit {pageFrom}, {pageTo}".format(
                    pageFrom=(dPage["page"] - 1) * dPage["limit"],
                    pageTo=dPage["limit"]
                )
                ldKey["category"] = ["id", "name", "order_num", "status", "enum_status", "remark"]
            elif sType == 'supplier':
                ldItem["supplier"] = r"select id, name, simple_name, code, status, remark from supplier"
                lsTotal = r"select count(id) from supplier"
                ldKey["supplier"] = ["id","name", "simple_name", "code", "status", "remark"]
            elif sType == "goods":
                ldItem["goods"] = r"select id, code, name, category, category_name, supplier, supplier_name, model, image, status, remark from goods order by order_num"
                lsTotal = r"select count(id) from goods"
                ldKey["goods"] = ["id", "code", "name", "category", "category_name", "supplier", "supplier_name", "model", "image", "status", "remark"]
            else:
                raise Exception("非法的数据类型参数:{sType}".format(sType=sType))
            conn = self.db.GetConnect()
            bConn = True
            cur = conn.cursor()
            if not cur:
                raise Exception("基础数据获取失败：{name}数据库[{db}]连接失败".format(name=self.sett.serverName, db=self.sett.serverDb))
            for lsItem in ldItem:
                lsSql = ldItem[lsItem]
                cur.execute(lsSql)
                rsData = cur.fetchall()
                rsData = [[(col.rstrip() if isinstance(col, str) else col) for col in line] for line in rsData]
                rtnData["entities"][lsItem] = []
                for line in rsData:
                    rtnData["entities"][lsItem].append(dict(zip(ldKey[lsItem], line)))
            cur.execute(lsTotal)
            rsData = cur.fetchall()
            rtnData["result"] = True
            rtnData["dataNumber"] = rsData[0][0]
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            if bConn:
                conn.close()

        return rtnData

    def basicDataDelete(self, sType, iID):
        """
        删除基础资料
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        bConn = False
        sSqlList = {}
        sTitle = ""
        try:
            if sType == "category":
                sTitle = "商品类别"
                sSqlList["category"] = r"delete from category where id = {id}".format(id=iID)
            else:
                raise Exception("非法的基础资料类型：{type}".format(type=sType))
            conn = self.db.GetConnect()
            bConn = True
            cur = conn.cursor()
            if not cur:
                raise Exception("{title}删除失败：{name}数据库[{db}]连接失败".format(title=sTitle, name=self.sett.serverName, db=self.sett.serverDb))
            for lsItem in sSqlList:
                lsSql = sSqlList[lsItem]
                cur.execute(lsSql)
            conn.commit()
            rtnData["result"] = True
            rtnData["info"] = "{title}删除成功！".format(title=sTitle)
        except Exception as e:
            rtnData["info"] = "{title}删除失败：".format(title=sTitle) + str(e)
        finally:
            if bConn:
                conn.close()

        return rtnData

    def basicDataNew(self, sType, para):
        """
        新增基础资料
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        bConn = False
        sSqlList = {}
        sTitle = ""
        try:
            if sType == "category":
                sTitle = "商品类别"
                if len(para["name"].rstrip()) == 0:
                    raise Exception("请输入{title}名称".format(title=sTitle))
                elif len(para["name"].rstrip()) > 20:
                    raise Exception("{title}名称长度不能超过20".format(title=sTitle))
                sSqlList["category"] = r"insert into category ( name, order_num, status, remark ) values ( '{name}', {order_num}, {status}, '{remark}' )".format(
                    name=para["name"],
                    order_num=para["order_num"],
                    status=para["status"],
                    remark=para["remark"]
                )
            else:
                raise Exception("非法的基础资料类型：{type}".format(type=sType))
            conn = self.db.GetConnect()
            bConn = True
            cur = conn.cursor()
            if not cur:
                rtnData["info"] = "{title}新增失败：{name}数据库[{db}]连接失败".format(title=sTitle, name=self.sett.serverName, db=self.sett.serverDb)
            else:
                for lsItem in sSqlList:
                    lsSql = sSqlList[lsItem]
                    cur.execute(lsSql)
            conn.commit()
            rtnData["result"] = True
            rtnData["info"] = "{title}新增成功！".format(title=sTitle)
            rtnData["dataNumber"] = cur.lastrowid
        except Exception as e:
            rtnData["info"] = "{title}新增失败：".format(title=sTitle) + str(e)
        finally:
            if bConn:
                conn.close()

        return rtnData

    def basicDataModify(self, sType, para):
        """
        修改基础资料
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        bConn = False
        sSqlList = {}
        sTitle = ""
        try:
            if sType == "category":
                sTitle = "商品类别"
                if len(para["name"].rstrip()) == 0:
                    raise Exception("请输入{title}名称".format(title=sTitle))
                elif len(para["name"].rstrip()) > 20:
                    raise Exception("{title}名称长度不能超过20".format(title=sTitle))
                sSqlList["category"] = r"update category set name='{name}', order_num={order_num}, status={status}, remark='{remark}' where id={id}".format(
                    id=para["id"],
                    name=para["name"],
                    order_num=para["order_num"],
                    status=para["status"],
                    remark=para["remark"]
                )
            else:
                raise Exception("非法的基础资料类型：{type}".format(type=sType))
            conn = self.db.GetConnect()
            bConn = True
            cur = conn.cursor()
            if not cur:
                rtnData["info"] = "{title}修改失败：{name}数据库[{db}]连接失败".format(title=sTitle, name=self.sett.serverName, db=self.sett.serverDb)
            else:
                for lsItem in sSqlList:
                    lsSql = sSqlList[lsItem]
                    cur.execute(lsSql)
            conn.commit()
            rtnData["result"] = True
            rtnData["info"] = "{title}修改成功！".format(title=sTitle)
        except Exception as e:
            rtnData["info"] = "{title}修改失败：".format(title=sTitle) + str(e)
        finally:
            if bConn:
                conn.close()

        return rtnData


if __name__ == "__main__":
    from interConfig import Settings
    a = Settings()
    b = InterData(a)
    c = b.basicDataList("category")
    if c["result"]:
        print(c["entities"]["category"])
    else:
        print("Some wrong is happen.")
