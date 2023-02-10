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
        self.engine = create_engine(sett.DATABASE_URI, echo=True)


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

        iDb = False
        try:
            # 检查查询条件有效性
            if len(sQuery) > 0:
                dQuery = json.loads(sQuery)["para"]
            else:
                dQuery = []
            dQuery = [line for line in dQuery if not (line["colname"]=="status" and line["value"] not in (0, 1))]
            # 检查分页、排序条件有效性
            if len(sPage) > 0:
                dPage = json.loads(sPage)
            else:
                dPage = {"page": 1, "limit": 100}
            if dPage.get("sortCol"):
                if dPage.get("sortType") == "desc":
                    pass
                else:
                    dPage["sortType"] = "asc"
            # 连接数据库
            select_db = sessionmaker(self.engine)
            db_session = select_db()
            iDb = True
            # 选择数据模型
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
            # 加入查询条件
            rtn = self._queryFilter(db_session, dataModel, dQuery)
            if rtn["result"]:
                objQuery = rtn["dataObj"]
            else:
                raise Exception(rtn["info"])
            # 查询总记录条数
            rtnData["dataNumber"] = objQuery.count()
            # 排序处理
            if dPage.get("sortCol"):
                if dPage.get("sortType") == "desc":
                    objQuery = objQuery.order_by(getattr(dataModel, dPage["sortCol"]).desc())
                else:
                    objQuery = objQuery.order_by(getattr(dataModel, dPage["sortCol"]).asc())
            # 分页处理
            if rtnData["dataNumber"] <= (dPage["page"] - 1) * dPage["limit"]:
                dPage["page"] = 1
            # 检索数据
            rs = objQuery.limit(dPage["limit"]).offset((dPage["page"] - 1) * dPage["limit"]).all()
            # 按特定格式返回数据
            rtnData["entities"][sType] = []
            for obj in rs:
                row = {}
                attr = [a for a in dir(obj) if not a.startswith("_") and a not in ('metadata', 'registry')]
                for col in attr:
                    row[col] = getattr(obj, col)
                rtnData["entities"][sType].append(row)
            if sType == "category":
                for line in rtnData["entities"][sType]:
                    line["enum_status"] = "正常" if line["status"] == 1 else "无效"
            elif sType == "supplier":
                for line in rtnData["entities"][sType]:
                    line["enum_status"] = "正常" if line["status"] == 1 else "无效"
            elif sType == "goods":
                for line in rtnData["entities"][sType]:
                    line["enum_status"] = "正常" if line["status"] == 1 else "无效"
            # 标记成功
            rtnData["result"] = True
            rtnData["info"] = "查询到{cnt}条记录.".format(cnt=rtnData["dataNumber"])
        except Exception as e:
            rtnData["info"] = str(e)
            print(rtnData["info"])
        finally:
            if iDb:
                db_session.close()
        
        return rtnData


    def _queryFilter(self, session, model, para):
        """
        查询条件处理
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
            "dataObj":None,
            "info":"",                      # 信息
            "entities": {}
        }

        try:
            objQuery = session.query(model)
            for line in para:
                objValue = line["value"]
                if line["oper"] == ">":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) > objValue)
                elif line["oper"] == ">=":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) >= objValue)
                elif line["oper"] == "==":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) == objValue)
                elif line["oper"] == "<=":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) <= objValue)
                elif line["oper"] == "<":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) < objValue)
                elif line["oper"] == "!=":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) != objValue)
                elif line["oper"] == "between":
                    if type(objValue) in (list, tuple):
                        if len(objValue) == 2:
                            objQuery = objQuery.filter(getattr(model, line["colname"]).between(*objValue))
                elif line["oper"] == "in":
                    if type(objValue) == list:
                        objQuery = objQuery.filter(getattr(model, line["colname"]).in_(objValue))
                elif line["oper"] == "not in":
                    if type(objValue) == list:
                        objQuery = objQuery.filter(getattr(model, line["colname"]).notin_(objValue))
                elif line["oper"] == "like":
                    if type(objValue) == str:
                        objQuery = objQuery.filter(getattr(model, line["colname"]).like(objValue))
            rtnData["result"] = True
            rtnData["dataObj"] = objQuery
        except Exception as e:
            rtnData["info"] = str(e)

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
                elif len(para["name"].rstrip()) < 4:
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
            rtnData["dataNumber"] = newObj.id
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

