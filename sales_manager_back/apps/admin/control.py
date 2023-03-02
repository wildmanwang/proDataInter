# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import json, datetime
from flask_login import login_user
from apps.admin.models import User
from ormBase import OrmBase
import jwt

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

        try:
            user = User.query.filter(User.name==sUser).first()
            if user is not None:
                if user.password_check(sPwd):
                    login_user(user)
                    jwtDic = {
                        'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
                        'iss': 'Cliff Wang',  # 签名
                        'data': {
                            'username': sUser
                        }
                    }
                    rtnData["result"] = True
                    rtnData["dataObject"] = {
                        "token": jwt.encode(jwtDic, self.sett.SECRET_KEY, algorithm='HS256')  # 加密生成字符串
                    }
                else:
                    rtnData["info"] = "密码错误"
            else:
                rtnData["info"] = "用户名错误：{name}".format(name=sUser)
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            pass

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
        jwtDic = jwt.decode(sToken, self.sett.SECRET_KEY, issuer='Cliff Wang', algorithms=['HS256'])
        rtnData["dataObject"] = {
            "roles": ["admin"],
            "introduction": "I am a super administrator",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            "name": jwtDic["data"]["username"]
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
        rtnData["dataObject"] = "success"

        return rtnData
