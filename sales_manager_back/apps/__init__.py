# -*- coding:utf-8 -*-
__author__ = "Cliff.wang"
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

sett = config.DevelopmentConfig()

app = Flask(__name__)
app.config.from_object(sett)
app.config['SQLALCHEMY_DATABASE_URI'] = r"mysql+pymysql://root:123456@127.0.0.1:3306/sales_manager"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

from apps.admin import admin
from apps.goods import goods

app.register_blueprint(admin, url_prefix='')
app.register_blueprint(goods, url_prefix='/goods')

from apps import admin, goods

__all__ = ["admin", "goods"]
