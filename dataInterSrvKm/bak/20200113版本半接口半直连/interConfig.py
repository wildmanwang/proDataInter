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
        # self.serverCode = config.get("dbServer", "serverCode")    # 服务端代码，支持类型：KMHCM
        self.serverCode = "KMHCM"                                # 目前不必配置，写死
        # self.serverName = config.get("dbServer", "serverName")   # 服务端简称
        self.serverName = "科脉好餐谋"                          # 目前不必配置，写死
        self.serverHost = config.get("dbServer", "host")         # 服务端地址
        self.dataPath = config.get("dbServer", "dataPath")          # 数据交换路径
        self.foodPicPath = config.get("dbServer", "foodPicPath")    # 菜品图片存放路径
        self.tableQRPath = config.get("dbServer", "tableQRPath")    # 桌台结帐二维码路径

        # 点餐前端
        # self.clientCode = config.get("Client", "clientCode")      # 客户端代码，支持类型YDHDY
        self.clientCode = "YDHDY"                               # 目前不必配置，写死
        # self.clientName = config.get("client", "clientName")      # 客户端简称
        self.clientName = "云蝶平板点餐"                          # 目前不必配置，写死
        self.terminal = config.get("client", "terminal")            # 当前支持boli6.00
        self.WXServer = config.get("client", "WXServer")            # WX窗口的socket地址
        self.WXPort = config.getint("client", "WXPort")             # WX窗口的socket端口

        if self.serverHost[-1:] == "/":
            self.serverHost = self.serverHost[:-1]
        self.serverUser = config.get("dbServer", "user")         # 服务端用户名
        self.serverPwd = config.get("dbServer", "password")      # 服务端密码
        self.serverDb = config.get("dbServer", "database")       # 服务端数据库名

        # web服务器
        self.webHost = config.get("webServer", "host")          # web服务器
        self.webPort = config.getint("webServer", "port")          # web端口

        # 业务设置
        self.fileWait = config.getint("busiSet", "fileWait")       # 读文件延迟毫秒数，防止读到脏数据
        self.softNumber = config.get("busiSet", "softNumber")       # 默认点菜宝编号
        self.serialNumber = config.get("busiSet", "serialNumber")   # 默认点菜宝序列号
        self.loginUser = config.get("busiSet", "loginUser")         # 默认登录用户号
        self.loginPassword = config.get("busiSet", "loginPassword") # 默认登录用户密码
        self.bLogin = False                                         # 默认用户是否已登录

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
