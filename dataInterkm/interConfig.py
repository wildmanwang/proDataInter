# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
import configparser

class Settings():

    def __init__(self, configfile):
        config = configparser.ConfigParser()
        config.read(configfile, encoding="utf-8")

        # 数据库连接App
        self.app_host = config.get("Database_app", "host")
        self.app_user = config.get("Database_app", "user")
        self.app_pwd = config.get("Database_app", "password")
        self.app_db = config.get("Database_app", "database")

        # 数据库连接Erp
        self.erp_host = config.get("Database_erp", "host")
        self.erp_user = config.get("Database_erp", "user")
        self.erp_pwd = config.get("Database_erp", "password")
        self.erp_db = config.get("Database_erp", "database")

        # 单据同步间隔
        self.bill_get_interval = config.getint("Other", "bill_get_interval")
        if self.bill_get_interval < 10:
            self.bill_get_interval = 10

        # 接口餐厅ID
        self.Dine_ID = config.get("Other", "Dine_ID")
        self.branch_no = config.get("Other", "branch_no")
        self.tabnumber = config.get("Other", "tabnumber")

if __name__ == "__main__":
    sett = Settings()
    i = 1
