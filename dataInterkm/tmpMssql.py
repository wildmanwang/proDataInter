# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
import pymssql

class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.password = pwd
        self.db = db

    def GetConnect(self):
        if not self.db:
            raise Exception("没有配置数据库信息")
        conn = pymssql.connect(host=self.host, port="1433", user=self.user, password=self.password, database=self.db, charset="utf8")
        if not conn:
            raise Exception("数据库连接失败")
        else:
            return conn

    def __GetCursor(self):
        if not self.db:
            raise Exception("没有配置数据库信息")
        self.conn = pymssql.connect(host=self.host, port="14133", user=self.user, password=self.password, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise Exception("数据库连接失败")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetCursor()
        cur.execute(sql)
        resList = cur.fetchall()

        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetCursor()
        cur.execute(sql)

        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    if 1 == 2:
        #
        ms = MSSQL(host=r"PC-20170506RFIY:1433", user="sa", pwd="0Wangle?", db="InterTest")
        lsSql = r"select 1 from sysobjects where id = object_id('cus_info')"
        res = ms.ExecQuery(lsSql)
        if len(res) == 0:
            lsSql = r"create table cus_info (" \
                    "cus_id         varchar(20) primary key," \
                    "cus_name       varchar(50) not null," \
                    "cus_remark     varchar(100) null )"
            ms.ExecNonQuery(lsSql)
        else:
            lsSql = r"select max(cus_id) from cus_info"
            res = ms.ExecQuery(lsSql)
            if not res[0][0]:
                lsID = '01'
            else:
                lsID = "00" + str(int(res[0][0]) + 1)
                lsID = lsID[-2:]
            lsSql = r"insert into cus_info ( cus_id, cus_name, cus_remark ) values ('{cus_id}', '{cus_id}', '{cus_id}')".format(cus_id = lsID)
            ms.ExecNonQuery(lsSql)

    if 1 == 1:
        ms = MSSQL(host=r".\MSSQL2008", user="sa", pwd="0Wangle?", db="kmcy_v8")
        #ms = MSSQL(host=r"192.168.0.100:1433", user="sa", pwd="0Wangle?", db="kmcy_v8")
        lsSql = r"select sys_var_value from sys_t_system where sys_var_id = 'dBusiness'"
        res = ms.ExecQuery(lsSql)
        print(res[0][0])
