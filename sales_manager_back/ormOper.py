# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from sqlalchemy import create_engine, func, and_, or_
from sqlalchemy.orm import sessionmaker
import json

class OrmOper():
    def __init__(self, sett):
        self.sett = sett
        self.engine = create_engine("mysql+pymysql://{user}:{password}@{server}:{port}/{database}".format(
            user=sett.serverUser,
            password=sett.serverPwd,
            server=sett.serverHost,
            port=sett.serverPort,
            database=sett.serverDb
        ), echo=True)

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

        iDb = False
        try:
            if len(sQuery) > 0:
                dQuery = json.loads(sQuery)
            else:
                dQuery = {}
            dPara = {}
            if len(sPage) > 0:
                dPage = json.loads(sPage)
            else:
                dPage = {"page": 1, "limit": 100}
            select_db = sessionmaker(self.engine)
            db_session = select_db()
            iDb = True
            dataModel = None
            if sType == "category":
                from ormModel import Category
                dataModel = Category
                iNum = dQuery.get("status")
                if iNum is None:
                    dPara["status"] = -1
                else:
                    if iNum == 0 or iNum == 1:
                        dPara["status"] = iNum
                    else:
                        dPara["status"] = -1
                sStr = dQuery.get("name")
                if sStr is None:
                    dPara["name"] = ""
                else:
                    sStr = sStr.strip()
                    if len(sStr) > 0:
                        dPara["name"] = sStr
                    else:
                        dPara["name"] = ""
            elif sType == "supplier":
                from ormModel import Supplier
                dataModel = Supplier
            elif sType == "goods":
                from ormModel import Goods
                dataModel = Goods
            else:
                raise Exception("Data Type [{type}] is not defined.".format(type=sType))
            rs1 = db_session.query(dataModel)
            rs2 = db_session.query(dataModel)
            if dPara["status"] != -1:
                rs1 = rs1.filter(dataModel.status == dPara["status"])
                rs2 = rs2.filter(dataModel.status == dPara["status"])
            if dPara["name"] != "":
                rs1 = rs1.filter(dataModel.name.like("{name}%".format(name=dPara["name"])))
                rs2 = rs2.filter(dataModel.name.like("{name}%".format(name=dPara["name"])))
            rs1 = rs1.limit(dPage["limit"]).offset((dPage["page"] - 1) * dPage["limit"]).all()
            rtnData["dataNumber"] = rs2.count()
            rtnData["entities"][sType] = []
            for obj in rs1:
                row = {}
                attr = [a for a in dir(obj) if not a.startswith("_") and a not in ('metadata', 'registry')]
                for col in attr:
                    row[col] = getattr(obj, col)
                rtnData["entities"][sType].append(row)
            if sType == "category":
                for line in rtnData["entities"][sType]:
                    line["enum_status"] = "正常" if line["status"] == 1 else "无效"
            rtnData["result"] = True
            rtnData["info"] = "查询到{cnt}条记录.".format(cnt=rtnData["dataNumber"])
        except Exception as e:
            rtnData["info"] = str(e)
            print(rtnData["info"])
        finally:
            if iDb:
                db_session.close()
        
        return rtnData


    def _queryFilter(self, model, query, para):
        """
        查询条件拼接
        para:[
            "colname":      字段名,
            "oper":         比较方式,
            "value":        值
        ]
        枚举：
            比较方式            值
            >                   3 or date or datetime
            >=                  3 or date or datetime
            ==                  3 or "abc" or date or datetime
            <=                  3 or date or datetime
            <                   3 or date or datetime
            !=                  3 or "abc" or date or datetime
            between             (1, 3) or (date1, date2) or (time1, time2)
            in                  [1, 3, 9] or ["a", "bb", "f"] or [date1, date2, date3]
            not in              [1, 3, 9] or ["a", "bb", "f"] or [date1, date2, date3]
            like                "a%" or "%a" or "%a%"
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        for line in para:
            if para["oper"] == "==":
                query.filter(getattr(model, para["colname"]) == para["value"])

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

        iDb = False
        try:
            select_db = sessionmaker(self.engine)
            db_session = select_db()
            iDb = True
            dataModel = None
            if sType == "category":
                from ormModel import Category
                dataModel = Category
            elif sType == "supplier":
                from ormModel import Supplier
                dataModel = Supplier
            elif sType == "goods":
                from ormModel import Goods
                dataModel = Goods
            else:
                raise Exception("Data Type [{type}] is not defined.".format(type=sType))
            icnt = db_session.query(dataModel).filter(dataModel.id==iID).delete()
            db_session.commit()
            rtnData["result"] = True
            rtnData["dataNumber"] = icnt
            rtnData["info"] = "数据[{id}]已成功删除.".format(id=iID)
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            if iDb:
                db_session.close()

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

        sTitle = ""
        iDb = False
        try:
            select_db = sessionmaker(self.engine)
            db_session = select_db()
            iDb = True
            dataModel = None
            if sType == "category":
                sTitle = "类别"
                from ormModel import Category
                if not para.get("name"):
                    raise Exception("请输入{title}名称.".format(title=sTitle))
                elif len(para["name"].rstrip()) <= 2:
                    raise Exception("{title}名称长度至少2位.".format(title=sTitle))
                elif len(para["name"].rstrip()) > 20:
                    raise Exception("{title}名称长度不能超过20.".format(title=sTitle))
                newObj = Category(para)
            elif sType == "supplier":
                sTitle = "供应商"
                from ormModel import Supplier
                if not para.get("name"):
                    raise Exception("请输入{title}名称.".format(title=sTitle))
                elif len(para["name"].rstrip()) <= 4:
                    raise Exception("{title}名称长度至少4位.".format(title=sTitle))
                elif len(para["name"].rstrip()) > 50:
                    raise Exception("{title}名称长度不能超过50.".format(title=sTitle))
                newObj = Supplier(para)
            elif sType == "goods":
                sTitle = "商品"
                from ormModel import Goods
                if not para.get("name"):
                    raise Exception("请输入{title}名称.".format(title=sTitle))
                elif len(para["name"].rstrip()) <= 5:
                    raise Exception("{title}名称长度至少5位.".format(title=sTitle))
                elif len(para["name"].rstrip()) > 50:
                    raise Exception("{title}名称长度不能超过50.".format(title=sTitle))
                newObj = Goods(para)
            else:
                raise Exception("Data Type [{type}] is not defined.".format(type=sType))
            db_session.add(newObj)
            db_session.commit()
            rtnData["result"] = True
            rtnData["dataNumber"] = 1
            rtnData["info"] = "新增数据[{id}].".format(id=newObj.id)
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            if iDb:
                db_session.close()

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

        iDb = False
        try:
            select_db = sessionmaker(self.engine)
            db_session = select_db()
            iDb = True
            dataModel = None
            if sType == "category":
                from ormModel import Category
                dataModel = Category
            elif sType == "supplier":
                from ormModel import Supplier
                dataModel = Supplier
            elif sType == "goods":
                from ormModel import Goods
                dataModel = Goods
            else:
                raise Exception("Data Type [{type}] is not defined.".format(type=sType))
            obj = db_session.query(dataModel).filter(dataModel.id==para.get("id"))
            icnt = obj.update(para)
            db_session.commit()
            rtnData["result"] = True
            rtnData["dataNumber"] = icnt
            rtnData["info"] = "数据[{id}]更新成功.".format(id=obj.first().id)
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            if iDb:
                db_session.close()

        return rtnData

