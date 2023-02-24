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
import json
from flask import Flask, request, jsonify, session
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

import config

sett = config.DevelopmentConfig()

from admin import admin
from goods import goods
from admin.control import ctl_admin
from admin.models import User

app = Flask(__name__)
app.config.from_object(sett)
app.register_blueprint(admin, url_prefix='')
app.register_blueprint(goods, url_prefix='/goods')

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.login_message = "Access denied."


@app.route('/hello', methods=['get', 'post'])
def home():
    return "这里是石将军数据服务接口"


@app.route('/test', methods=['get', 'post'])
def test():
    session["username"] = "张三三"
    return session.get("username")


@login_manager.user_loader
def load_user(id):
    """加载用户"""
    iDb = False
    user = None
    try:
        engine = create_engine(sett.DATABASE_URI, echo=True, pool_pre_ping=True)
        select_db = sessionmaker(engine)
        db_session = scoped_session(select_db)
        iDb = True
        user = db_session.query(User).filter(User.id==int(id)).first()
    except Exception as e:
        rtnData["info"] = str(e)
        print(rtnData["info"])
    finally:
        if iDb:
            db_session.close()
    
    return user


if __name__ == '__main__':
    app.run(host=app.config["WEB_SERVER_HOST"], port=app.config["WEB_SERVER_PORT"], debug=True)
