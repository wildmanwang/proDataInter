# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

        try:
            select_db = sessionmaker(self.engine)
            db_session = select_db()
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
            rs = db_session.query(dataModel).all()
            rtnData["entities"][sType] = []
            for obj in rs:
                row = {}
                attr = [a for a in dir(obj) if not a.startswith("_") and a not in ('metadata', 'registry')]
                for col in attr:
                    row[col] = getattr(obj, col)
                rtnData["entities"][sType].append(row)
            rtnData["result"] = True
            rtnData["dataNumber"] = len(rs)
            rtnData["info"] = "查询到{cnt}条记录.".format(cnt=len(rs))
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            db_session.close()
        
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

        try:
            select_db = sessionmaker(self.engine)
            db_session = select_db()
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
            db_session.close()

        return rtnData


    def basicDataNew(self, sType, **para):
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

        try:
            select_db = sessionmaker(self.engine)
            db_session = select_db()
            dataModel = None
            print(1)
            if sType == "category":
                from ormModel import Category
                print(2)
                newObj = Category(para)
                print(3)
            elif sType == "supplier":
                from ormModel import Supplier
                newObj = Supplier(para)
            elif sType == "goods":
                from ormModel import Goods
                newObj = Goods(para)
            else:
                raise Exception("Data Type [{type}] is not defined.".format(type=sType))
            print(2)
            db_session.add(newObj)
            db_session.commit()
            rtnData["result"] = True
            rtnData["dataNumber"] = 1
            rtnData["info"] = "新增数据[{id}].".format(id=newObj.id)
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            db_session.close()

        return rtnData
