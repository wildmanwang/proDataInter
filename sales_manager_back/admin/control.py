# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import json
from flask_login import login_user
from admin.models import User
from ormBase import OrmBase

class ctl_admin(OrmBase):
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

        iDb = False
        try:
            select_db = sessionmaker(self.engine)
            db_session = scoped_session(select_db)
            user = db_session.query(User).filter(User.name==sUser).first()
            if user is not None:
                if user.password_check(sPwd):
                    login_user(user)
                    rtnData["result"] = True
                    rtnData["entities"] = {
                        "token": "admin-token"
                    }
                else:
                    rtnData["info"] = "密码错误"
            else:
                rtnData["info"] = "用户名错误：{name}".format(name=sUser)
        except Exception as e:
            rtnData["info"] = str(e)
            print(rtnData["info"])
        finally:
            if iDb:
                db_session.close()

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
