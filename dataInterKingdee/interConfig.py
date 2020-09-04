# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
import configparser
import logging
import os

class Settings():

    def __init__(self, path, file):
        self.path = path

        self.logger = self._getLogger()

        config = configparser.ConfigParser()
        config.read(os.path.join(path, file), encoding="utf-8")

        # 前端连接frontEnd
        # self.frontCode = config.get("frontEnd", "frontCode")    # 前端代码，支持类型：Kemai
        self.frontCode = "KMHCM"                                # 目前不必配置，写死
        # self.frontCode = "KMTTYS"                                # 目前不必配置，写死
        # self.frontName = config.get("frontEnd", "frontName")   # 前端简称
        self.frontName = "科脉天天饮食"                          # 目前不必配置，写死
        self.frontHost = config.get("frontEnd", "host")         # 前端服务器地址
        if self.frontHost[-1:] == "/":
            self.frontHost = self.frontHost[:-1]
        self.frontUser = config.get("frontEnd", "user")         # 前端用户名
        self.frontPwd = config.get("frontEnd", "password")      # 前端密码
        self.frontDb = config.get("frontEnd", "database")       # 前端数据库名

        # 后端连接backEnd
        # self.backCode = config.get("backEnd", "backCode")       # 后端代码，支持类型：Kingdee,Emptydb
        self.backCode = "Kingdee"                               # 目前不必配置，写死
        # self.backName = config.get("backEnd", "backName")     # 后端简称
        self.backName = "金蝶云"                               # 目前不必配置，写死
        self.backHost = config.get("backEnd", "host")         # 后端服务器地址
        if self.backHost[-1:] == "/":
            self.backHost = self.backHost[:-1]
        self.backUser = config.get("backEnd", "user")         # 后端用户名
        self.backPwd = config.get("backEnd", "password")      # 后端密码
        self.backDb = config.get("backEnd", "database")       # 后端数据库名

        # 数据库连接controlEnd
        self.controlHost = config.get("controlEnd", "host")         # 控制端数据库地址
        self.controlUser = config.get("controlEnd", "user")         # 控制端数据库用户名
        self.controlPwd = config.get("controlEnd", "password")      # 控制端数据库密码
        self.controlDb = config.get("controlEnd", "database")       # 控制端数据库名

        # 控制参数control
        self.timingBaseInterval = config.getint("control", "timingBaseInterval")   # 基础资料对接间隔时间
        self.timingBusiDay = config.getint("control", "timingBusiDay")             # 业务数据对接延迟天数
        self.timingBusiTime = config.get("control", "timingBusiTime")           # 业务数据对接定时时间 必须是5位 ##:##

        # 组织机构org
        self.org = {}
        orgList = config.items("org")
        for i in orgList:
            self.org[i[0]] = int(i[1])

        # 支付方式payment
        self.payment = {}
        payList = config.items("payment")
        for i in payList:
            self.payment[i[0]] = i[1]

        # 金蝶后台业务参数
        self.defaultOrgNo = config.get("busiBackKingdee", "defaultOrgNo")   # 默认机构编码
        self.clsBigNo = config.get("busiBackKingdee", "clsBigNo")       # 默认食品大类
        self.deptNo = config.get("busiBackKingdee", "deptNo")          # 默认部门编码
        self.userNo = config.get("busiBackKingdee", "userNo")          # 默认操作员

        # 状态
        self.run = True
        self.processing = False

    def _getLogger(self):
        logger = logging.getLogger("[DataInterCatering]")
        handler = logging.FileHandler(os.path.join(self.path, "service.log"))
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

if __name__ == "__main__":
    sett = Settings(r"E:\AI\Python\proDataInter\dataInterKingdee\config")
    i = 1
    i += 1
