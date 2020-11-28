# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
import configparser
import logging
import os, sys

class Settings():

    def __init__(self):
        # 获取编程环境下的代码路径
        self.path = os.path.abspath(os.path.dirname(__file__))
        # 获取打包后的可执行文件路径
        # self.path = os.path.dirname(sys.executable)

        self.logger = self._getLogger()

        config = configparser.ConfigParser()
        confFile = os.path.join(os.path.dirname(self.path), "srv.conf")
        if not os.path.exists(confFile):
            confFile = os.path.join(self.path, "srv.conf")
        config.read(confFile, encoding="utf-8")

        # [dbEnd]
        self.appType = config.get("dbEnd", "appType")   # 收银系统类型
        self.serverHost = config.get("dbEnd", "host")  # 服务端地址
        if self.serverHost[-1:] == "/":
            self.serverHost = self.serverHost[:-1]
        self.serverUser = config.get("dbEnd", "user")  # 服务端用户名
        self.serverPwd = config.get("dbEnd", "password")  # 服务端密码
        self.serverDb = config.get("dbEnd", "database")  # 服务端数据库名

        # [onLineEnd]
        self.interUrl = config.get("onLineEnd", "interUrl")          # web服务器
        self.interPort = config.get("onLineEnd", "interPort")          # web端口
        if self.interPort:
            self.interPort = int(self.interPort)
        else:
            self.interPort = 0
        self.appid = config.get("onLineEnd", "appid")          # appid
        self.appsecret = config.get("onLineEnd", "appsecret")          # appsecret

        # [controlEnd]
        self.controlHost = config.get("controlEnd", "host")  # 控制端地址
        if self.controlHost[-1:] == "/":
            self.controlHost = self.controlHost[:-1]
        self.controlUser = config.get("controlEnd", "user")  # 控制端用户名
        self.controlPwd = config.get("controlEnd", "password")  # 控制端密码
        self.controlDb = config.get("controlEnd", "database")  # 控制端数据库名
        self.timingBaseTime = config.get("controlEnd", "timingBaseTime")  # 数据传输间隔：分钟
        self.timingBaseInterval = config.getint("controlEnd", "timingBaseInterval")  # 订单传输单据日期
        self.timingBusiDay = config.getint("controlEnd", "timingBusiDay")  # 控制端数据库名
        self.timingBusiTime = config.get("controlEnd", "timingBusiTime")  # 控制端数据库名
        self.timingBusiInterval = config.getint("controlEnd", "timingBusiInterval")  # 控制端数据库名

        # [businessLogic]
        self.defaultOrgNo = config.get("businessLogic", "defaultOrgNo")  # 默认机构编码
        self.defaultOrgName = config.get("businessLogic", "defaultOrgName")  # 默认机构名称
        self.defaultPayType = config.get("businessLogic", "defaultPayType")  # 默认线上支付方式

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
