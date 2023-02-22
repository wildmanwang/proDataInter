# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import json

class ctl_admin():
    def __init__(self, sett):
        self.sett = sett
        self.engine = create_engine(self.sett.DATABASE_URI, echo=True, pool_pre_ping=True)


    def user_login(self, sUser, sPwd):
        """
        用户登录
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        rtnData["result"] = True
        rtnData["entities"] = {
            "token": "admin-token"
        }

        return rtnData


    def user_info(self, sToken):
        """
        用户信息
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        rtnData["result"] = True
        rtnData["entities"] = {
            "roles": ["admin"],
            "introduction": "I am a super administrator",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            "name": "Cliff Wang"
        }

        return rtnData


    def user_logout(self):
        """
        用户登出
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        rtnData["result"] = True
        rtnData["entities"] = "success"

        return rtnData
