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

        # 数据库服务器
        self.serverHost = config.get("dbServer", "host")         # 服务端地址
        if self.serverHost[-1:] == "/":
            self.serverHost = self.serverHost[:-1]
        self.serverUser = config.get("dbServer", "user")         # 服务端用户名
        self.serverPwd = config.get("dbServer", "password")      # 服务端密码
        self.serverDb = config.get("dbServer", "database")       # 服务端数据库名

        # web服务器
        self.webHost = config.get("webServer", "host")          # web服务器
        self.webPort = config.getint("webServer", "port")          # web端口

        # other
        self.callComputer = config.get("other", "callComputer") # 呼叫取餐的电脑
        self.kmHttpSrv = ""
        self.kmHttpPort = ""

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
