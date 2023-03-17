# -*- coding:utf-8 -*-
"""
flask框架实现数据接口服务
数据返回格式：
rtnData = {
    "result":True,                  # 逻辑控制 True/False
    "dataString":"",               # 字符串
    "dataNumber":1,                # 数字
    "info":"",                      # 信息
    "entities": {                   # 表体集
        "bill":[],                   # 销售单
        "billItem":[],               # 销售单
        "billPay":[]                 # 销售单
    }
}
"""
__author__ = "Cliff.wang"
from flask import session
from apps import app
from flask_login import LoginManager

@app.route('/hello', methods=['get', 'post'])
def home():
    return "这里是石将军数据服务接口"


@app.route('/test', methods=['get', 'post'])
def test():
    session["username"] = "张三三"
    return session.get("username")


login_manager = LoginManager(app)
login_manager.login_view = "admin.user_login"
login_manager.login_message_category = "info"
login_manager.login_message = "Access denied."


@login_manager.user_loader
def load_user(id):
    """加载用户"""
    rtnData = {
        "result":False,                # 逻辑控制 True/False
        "dataString":"",               # 字符串
        "dataNumber":0,                # 数字
        "dataObject":None,              # 对象
        "info":"",                      # 信息
        "entities": {}
    }

    user = None
    try:
        from apps.admin.models import User
        user = User.query.get(int(id))
    except Exception as e:
        rtnData["info"] = str(e)
        print(rtnData["info"])
    finally:
        pass
    
    return user


if __name__ == '__main__':
    app.run(host=app.config["WEB_SERVER_HOST"], port=app.config["WEB_SERVER_PORT"], debug=True)
    """
    from apps import db
    from apps.admin.models import User

    with app.app_context():
        user = User({"name": "Zhang san", "password": "123456", "status": 1})
        db.session.add(user)
        db.session.commit()
    """
    