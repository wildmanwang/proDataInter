# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import json
from ormBase import OrmBase


class ctl_goods(OrmBase):
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
            # 检查查询条件有效性
            if len(sQuery) > 0:
                dQuery = json.loads(sQuery)["para"]
            else:
                dQuery = []
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
            # 选择数据模型
            dataModel = None
            if sType == "category":
                from apps.goods.models import Category
                dataModel = Category
                dQuery = [line for line in dQuery if not (line["colname"]=="status" and line["value"] not in (0, 1))]
            elif sType == "supplier":
                from apps.goods.models import Supplier
                dataModel = Supplier
                dQuery = [line for line in dQuery if not (line["colname"]=="status" and line["value"] not in (0, 1))]
            elif sType == "goods":
                from apps.goods.models import Goods
                dataModel = Goods
                dQuery = [line for line in dQuery if not (line["colname"]=="status" and line["value"] not in (0, 1))]
            else:
                raise Exception("Data Type [{type}] is not defined.".format(type=sType))
            # 查询数据
            rtn = self.singleDataList(dataModel, dQuery, dPage)
            if not rtn["result"]:
                raise Exception(rtn["info"])
            rtnData["dataNumber"] = rtn["dataNumber"]
            rtnData["entities"][sType] = rtn["entities"]["single"]
            # 结果集特殊处理
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
        finally:
            pass
        
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
            dataModel = None
            if sType == "category":
                from apps.goods.models import Category
                dataModel = Category
            elif sType == "supplier":
                from apps.goods.models import Supplier
                dataModel = Supplier
            elif sType == "goods":
                from apps.goods.models import Goods
                dataModel = Goods
            else:
                raise Exception("Data Type [{type}] is not defined.".format(type=sType))
            rtnData = self.singleDataDelete(dataModel, iID)
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            pass

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
        try:
            if sType == "category":
                sTitle = "类别"
                from apps.goods.models import Category
                if not para.get("name"):
                    raise Exception("请输入{title}名称.".format(title=sTitle))
                elif len(para["name"].rstrip()) <= 2:
                    raise Exception("{title}名称长度至少2位.".format(title=sTitle))
                elif len(para["name"].rstrip()) > 20:
                    raise Exception("{title}名称长度不能超过20.".format(title=sTitle))
                newObj = Category(para)
            elif sType == "supplier":
                sTitle = "供应商"
                from apps.goods.models import Supplier
                if not para.get("name"):
                    raise Exception("请输入{title}名称.".format(title=sTitle))
                elif len(para["name"].rstrip()) < 4:
                    raise Exception("{title}名称长度至少4位.".format(title=sTitle))
                elif len(para["name"].rstrip()) > 50:
                    raise Exception("{title}名称长度不能超过50.".format(title=sTitle))
                newObj = Supplier(para)
            elif sType == "goods":
                sTitle = "商品"
                from apps.goods.models import Goods
                if not para.get("name"):
                    raise Exception("请输入{title}名称.".format(title=sTitle))
                elif len(para["name"].rstrip()) <= 5:
                    raise Exception("{title}名称长度至少5位.".format(title=sTitle))
                elif len(para["name"].rstrip()) > 50:
                    raise Exception("{title}名称长度不能超过50.".format(title=sTitle))
                newObj = Goods(para)
            else:
                raise Exception("Data Type [{type}] is not defined.".format(type=sType))
            rtnData = self.singleDataNew(newObj)
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            pass

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

        try:
            dataModel = None
            if sType == "category":
                from apps.goods.models import Category
                dataModel = Category
            elif sType == "supplier":
                from apps.goods.models import Supplier
                dataModel = Supplier
            elif sType == "goods":
                from apps.goods.models import Goods
                dataModel = Goods
            else:
                raise Exception("Data Type [{type}] is not defined.".format(type=sType))
            rtnData = self.singleDataModify(dataModel, para)
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            pass

        return rtnData
