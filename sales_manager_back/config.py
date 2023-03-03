"""
配置文件
added at 2023-02-10 by Cliff Wang
"""


class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = r""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    WEB_SERVER_HOST = ""
    WEB_SERVER_PORT = ""

    # 秘钥，Session等模块需要用到
    SECRET_KEY = "dsfao85238792lk2,-1"


class ProductionConfig(Config):
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = r"mysql+pymysql://root:123456@127.0.0.1:3306/sales_manager"

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = "8008"


class TestingConfig(Config):
    TESTING = True
