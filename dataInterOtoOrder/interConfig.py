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
        # self.path = os.path.abspath(os.path.dirname(__file__))
        # 获取打包后的可执行文件路径
        self.path = os.path.dirname(sys.executable)

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
        self.timingItemTime = config.get("controlEnd", "timingItemTime")  # 商品传输时点
        self.timingItemInterval = config.getint("controlEnd", "timingItemInterval")  # 商品传输间隔分钟
        self.timingOrderTime = config.get("controlEnd", "timingOrderTime")  # 订单传输时点
        self.timingOrderInterval = config.getint("controlEnd", "timingOrderInterval")  # 订单传输间隔分钟
        self.timingFeedbackTime = config.get("controlEnd", "timingFeedbackTime")  # 订单回调时点
        self.timingFeedbackInterval = config.getint("controlEnd", "timingFeedbackInterval")  # 订单回调间隔分钟
        self.timingStockTime = config.get("controlEnd", "timingStockTime")  # 库存传输时点
        self.timingStockInterval = config.getint("controlEnd", "timingStockInterval")  # 库存传输间隔分钟
        self.timingStateInterval = config.getint("controlEnd", "timingStateInterval")   # 上下架状态更新间隔分钟

        # [businessLogic]
        self.defaultOrgNo = config.get("businessLogic", "defaultOrgNo")  # 默认机构编码
        self.defaultOrgName = config.get("businessLogic", "defaultOrgName")  # 默认机构名称
        self.pickupDelay = config.get("businessLogic", "pickupDelay")  # 支付后多少分钟可以提货

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
