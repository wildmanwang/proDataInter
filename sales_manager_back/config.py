"""
配置文件
added at 2023-02-10 by Cliff Wang
"""


class Config(object):
    DEBUG = False
    TESTING = False

    MYSQL_DATABASE_HOST = ""
    MYSQL_DATABASE_PORT = ""
    MYSQL_DATABASE_DB = ""
    MYSQL_DATABASE_USER = ""
    MYSQL_DATABASE_PASSWORD = ""

    WEB_SERVER_HOST = ""
    WEB_SERVER_PORT = ""

    # 秘钥，Session等模块需要用到
    SECRET_KEY = "dsfao85238792lk2,-1"

    """
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return r"mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(
            user=self.MYSQL_DATABASE_USER,
            password=self.MYSQL_DATABASE_PASSWORD,
            host=self.MYSQL_DATABASE_HOST,
            port=self.MYSQL_DATABASE_PORT,
            database=self.MYSQL_DATABASE_DB
        )
    """


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    MYSQL_DATABASE_HOST = "127.0.0.1"
    MYSQL_DATABASE_PORT = "3306"
    MYSQL_DATABASE_DB = "sales_manager"
    MYSQL_DATABASE_USER = "root"
    MYSQL_DATABASE_PASSWORD = "123456"

    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = "8008"


class TestingConfig(Config):
    TESTING = True
