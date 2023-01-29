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
            else:
                raise Exception("Data Type is not found.")
            rs = db_session.query(dataModel).all()
            rtnData["entities"][sType] = []
            print("1")
            print("data cnt:{cnt}".format(cnt=len(rs)))
            for line in rs:
                row = {}
                row["id"] = line.id
                row["name"] = line.name
                row["status"] = line.status
                row["remark"] = line.remark
                rtnData["entities"][sType].append(row)
            rtnData["result"] = True
            rtnData["dataNumber"] = len(rs)
            print("OK!")
            print(rtnData)
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            db_session.close()
        
        return rtnData
