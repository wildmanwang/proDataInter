# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
from interMssql import MSSQL
from datetime import date, datetime

if __name__ == "__main__":
    if 1 == 2:
        dbTest = MSSQL("192.168.0.101", "sa", "0Wangle?", "kmcy_v8")
        conn = dbTest.GetConnect()
        cur = conn.cursor()

        lsSql = r"select max(dBusiness) from d_t_food_bill where cBranch_C = '11'"
        cur.execute(lsSql)
        res = cur.fetchall()
        print(res)

    if 1 == 2:
        import schedule
        import time

        def dosomething():
            print("I'm working...")

        schedule.every(10).seconds.do(dosomething)

        while True:
            schedule.run_pending()
            time.sleep(1)

    if 1 == 1:
        from decimal import Decimal

        d1 = Decimal("12.3")
        print(d1)
        print(float(d1))

    if 1 == 2:
        from urllib import parse, request
        import json

        url = r"https://szyd.ik3cloud.com/K3Cloud/getalldatacenters.eatsun"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
        req = request.Request(url=url, headers=headers)
        try:
            res = request.urlopen(req)
            res = res.read().decode("utf-8")
        except Exception as e:
            print(str(e))
        else:
            obj = json.loads(res)
            # print(obj)
            print("Result:", obj["Result"])
            print("Id:", obj["ReturnValue"][0]["Id"])

    if 1 == 2:
        from urllib import parse, request
        import json

        url = r"https://szyd.ik3cloud.com/K3Cloud/login.eatsun"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
        data = {
            "UserToken":"",
            "ActionName":"",
            "PostData":[
                {
                    "AccountID":"20190422204900",
                    "UserName":"administrator",
                    "Password":"szyd@5201"
                }
            ]
        }
        #data = parse.urlencode(data).encode("utf-8")
        data = json.dumps(data).encode("utf-8")
        print(data)
        req = request.Request(url=url, headers=headers, data=data)
        res = request.urlopen(req)
        res = res.read().decode("utf-8")
        res = json.loads(res)
        bResult = res["Result"]
        print(res)
        if bResult:
            pass
        else:
            pass
