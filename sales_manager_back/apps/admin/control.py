# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import json, datetime
from flask_login import login_user
from apps.admin.models import User, SysModel, SysFunction
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
            user = User.query.filter(User.account==sUser).first()
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
    

    def user_permission(self):
        """
        获取用户操作权限
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
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
        rtnData["dataString"] = "success"

        return rtnData


    def get_menu(self, user):
        """
        获取菜单
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "dataObject":None,              # 对象
            "info":"",                      # 信息
            "entities": {}
        }

        try:
            obj = []
            models = SysModel.query.all()
            funs = SysFunction.query.all()
            obj = [{
                "code":item1.code,
                "component":"Layout",
                "icon":item1.icon,
                "id":item1.id,
                "name":item1.name,
                "pid":"0",
                "remark":item1.remark,
                "router":"",
                "sort":item1.order_number,
                "type":1,
                "children":[{
                    "code":item2.code,
                    "component":"Layout",
                    "icon":item2.icon,
                    "id":item2.id + 10000,
                    "name":item2.name,
                    "pid":str(item2.sysmodel),
                    "remark":item2.remark,
                    "router":"",
                    "sort":item2.order_number,
                    "type":2,
                    "children":[]
                } for item2 in funs if item2.sysmodel==item1.id] } for item1 in models]
            rtnData["dataObject"] = obj
            rtnData["result"] = True
            rtnData["dataString"] = "success"
        except Exception as e:
            rtnData["info"] = str(e)
        finally:
            pass

        return rtnData
"""
https://blog.csdn.net/qq_36873710/article/details/124430511
"data": [
    {
      "code": "",
      "component": "Layout",
      "icon": "el-icon-s-help",
      "id": "1",
      "name": "平台管理",
      "pid": "0",
      "remark": "目录",
      "router": "/user-Management",
      "sort": 1,
      "type": 1,
      "children": [
        {
          "children": [],
          "code": "",
          "component": "views/user-Management/index",
          "icon": "table",
          "id": "4",
          "name": "用户管理",
          "pid": "1",
          "remark": "菜单",
          "router": "user",
          "sort": 4,
          "type": 2
        }
      ]
    }
  ],
  """