# -*- coding:utf-8 -*-
"""
软件前后端的父类
数据操作标准返回值结构：
{
    "result":True/False,            # 逻辑控制
    "dataString":"",                # 字符串
    "dataNumber":0,                 # 数字
    "info":"",                      # 信息
    "entities":{                    # 表体集
        "item":[(                   # 表体代码
                recordNo,           # 记录标识
                recordName          # 记录名称/备注
            )
        ]
    }
}
"""
__author__ = "Cliff.wang"

class BusiProcess():

    def __init__(self, sett, endType):
        """
        实例化
        :param sett: 参数
        :param endType:  接口端型 front:前端 back:后端
        """
        self.sett = sett
        self.endType = endType
        self.interConn = {}
        if self.endType == "front":
            self.interCode = self.sett.frontCode
            self.interName = self.sett.frontName
            self.interConn["host"] = self.sett.frontHost
            self.interConn["user"] = self.sett.frontUser
            self.interConn["password"] = self.sett.frontPwd
            self.interConn["database"] = self.sett.frontDb
        else:
            self.interCode = self.sett.backCode
            self.interName = self.sett.backName
            self.interConn["host"] = self.sett.backHost
            self.interConn["user"] = self.sett.backUser
            self.interConn["password"] = self.sett.backPwd
            self.interConn["database"] = self.sett.backDb
        if self.endType == "front":
            self.interName = "前端" + self.interName
        else:
            self.interName = "后端" + self.interName

    def interInit(self):
        """
        接口初始化
        :return:
        """
        pass

    def getBranchs(self):
        """
        获取需要对接的门店列表
        前端需要实现
        :return:                            # 返回门店数据表
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "item": {                    # 表体代码
                    "subItem":[(            # 子表
                            "recordNo",     # 记录标识 可能是字符串或数字
                            "recordName",   # 记录名称/备注
                            "recordBranch", # 记录门店
                            "recordDate"    # 记录日期 可能是空字符串
                        )
                    ]
                }
            }
        }

        return rtnData

    def getBaseData(self, item):
        """
        基础资料对接
        基础资料导出端需要实现
        :param item: 数据项
        :return: 导出的基础资料
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "item": {                    # 表体代码
                    "item":[(                # 子表 这里同表体代码
                            "recordNo",     # 记录标识 可能是字符串或数字
                            "recordName",   # 记录名称/备注
                            "",               # 记录门店 这里为空字符串
                            ""                # 记录日期 这里为空字符串
                        )
                    ]
                }
            }
        }

        return rtnData

    def putBaseData(self, putData):
        """
        基础资料对接
        基础资料导入端需要实现
        :param putData: 传入的基础资料
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "item": {                    # 表体代码
                    "subItem":[(            # 子表
                            "recordNo",     # 记录标识 可能是字符串或数字
                            "recordName",   # 记录名称/备注
                            "recordBranch", # 记录门店
                            "recordDate"    # 记录日期 可能是空字符串
                        )
                    ]
                }
            }
        }

        return rtnData

    def getBusiData(self, item, branch, sFrom, sTo):
        """
        销售单据对接
        前端需要实现
        :param item: 数据项
        :param branch: 门店
        :param sFrom: 开始日期
        :param sTo: 截至日期
        :return: 导出的业务数据
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "item": {                    # 表体代码
                    "subItem":[(            # 子表
                            "recordNo",     # 记录标识 可能是字符串或数字
                            "",              # 记录名称/备注 这里为空字符串
                            "recordBranch", # 记录门店
                            "recordDate"    # 记录日期 可能是空字符串
                        )
                    ]
                }
            }
        }

        return rtnData

    def putBusiData(self, branch, putData):
        """
        销售单据对接
        后端需要实现
        :param branch: 门店
        :param putData: 传入的业务数据
            dataString: 本次同步的最大日期
            entities:   数据字典
                bill:   主单表集合
                item:   商品表集合
                pay:    付款表集合
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "item": {                    # 表体代码
                    "subItem":[(            # 子表
                            "recordNo",     # 记录标识 可能是字符串或数字
                            "",              # 记录名称/备注 这里为空字符串
                            "recordBranch", # 记录门店
                            "recordDate"    # 记录日期 可能是空字符串
                        )
                    ]
                }
            }
        }

        return rtnData
