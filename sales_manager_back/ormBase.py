"""
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class OrmBase(object):
    def __init__(self, sett):
        self.sett = sett
        self.engine = create_engine(self.sett.DATABASE_URI, echo=True, pool_pre_ping=True)


    def singleDataList(self, dataModel, dQuery, dPage):
        """
        获取数据列表
        :param dataModel: 数据模型
        :param sQuery: 查询条件
            {"para":[
                {"colname":"name","oper":"like","value":"%"},
                {"colname":"status","oper":"==","value":1}]
            }
        :param sPage: 分页条件
            {
                "page":2,
                "limit":10,
                "sortCol":"",
                "sortType":"asc"
            }
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
            # 连接数据库
            select_db = sessionmaker(self.engine)
            db_session = scoped_session(select_db)
            iDb = True
            # 加入查询条件
            rtn = self.queryFilter(db_session, dataModel, dQuery)
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
            rtnData["entities"]["single"] = []
            for obj in rs:
                row = {}
                attr = [a for a in dir(obj) if not a.startswith("_") and a not in ('metadata', 'registry')]
                for col in attr:
                    row[col] = getattr(obj, col)
                rtnData["entities"]["single"].append(row)
            # 标记成功
            rtnData["result"] = True
            rtnData["info"] = "查询到{cnt}条记录.".format(cnt=rtnData["dataNumber"])
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            if iDb:
                db_session.close()
        
        return rtnData


    def queryFilter(self, session, model, para):
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


    def singleDataDelete(self, dataModel, iID):
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
            db_session = scoped_session(select_db)
            iDb = True
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


    def singleDataNew(self, newObj):
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
            db_session = scoped_session(select_db)
            iDb = True
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


    def singleDataModify(self, dataModel, para):
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
            db_session = scoped_session(select_db)
            iDb = True
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
