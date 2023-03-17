# -*- coding:utf-8 -*-
__author__ = "Cliff.wang"
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

sett = config.DevelopmentConfig()

app = Flask(__name__)
app.config.from_object(sett)

db = SQLAlchemy(app)

# 每个模块显式导入至少一个模型、或者导入整个模型所在模块，flask-migrate才会跟踪对应的模型变化
from apps.admin import models
from apps.goods import models

migrate = Migrate(app=app, db=db, compare_server_default=True)

from apps.admin import admin
from apps.goods import goods

app.register_blueprint(admin, url_prefix='')
app.register_blueprint(goods, url_prefix='/goods')

from apps import admin, goods

__all__ = ["admin", "goods"]
