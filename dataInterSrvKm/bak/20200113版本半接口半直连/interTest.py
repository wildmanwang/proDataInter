# -*- coding:utf-8 -*-
"""
接口测试
rtnData = {
    "result":True,                  # 逻辑控制 True/False
    "dataString":"",               # 字符串
    "dataNumber":1,                # 数字
    "info":"",                      # 信息
    "entities": {                   # 表体集
        "saleBill": {               # 表体代码
            "bill":[]                # 销售单
        }
    }
}
"""
__author__ = "Cliff.wang"
import unittest
from urllib import request
import json

class InterTest(unittest.TestCase):
    """
    接口测试
    """

    @classmethod
    def setUpClass(cls) -> None:
        # 这里是所有测试用例前的准备工作
        print("开始测试")

    @classmethod
    def tearDownClass(cls) -> None:
        # 这里是所有测试用例后的清理工作
        print("结束测试")

    def setUp(self) -> None:
        # 这里是一个测试用例前的准备工作
        pass

    def tearDown(self) -> None:
        # 这里是一个测试用例后的清理工作
        pass

    @unittest.skip("跳过这个测试用例")
    def test_home(self):
        pass

    @unittest.skip("跳过这个测试用例")
    def test_test(self):
        url = r"http://127.0.0.1:8008/test"
        para = {"dataType":"haha"}
        para = json.dumps(para).encode("utf-8")
        req = request.Request(url=url, data=para, method="post")
        res = request.urlopen(req)
        res = res.read().decode("utf-8")
        res = json.loads(res)
        bResult = res["result"]
        lResult = res["entities"]["test"]
        print(lResult)
        self.assertEqual(True, bResult)

    @unittest.skip("跳过这个测试用例")
    def test_login(self):
        pass

    @unittest.skip("跳过这个测试用例")
    def test_basicDataGet(self):
        #url = r"http://120.77.217.209:8008/basicData"
        url = r"http://127.0.0.1:8008/basicData"
        lsType = "dishCategory"
        para = {"dataType":lsType}
        para = json.dumps(para).encode("utf-8")
        req = request.Request(url=url, data=para)
        res = request.urlopen(req)
        res = res.read().decode("utf-8")
        res = json.loads(res)
        bResult = res["result"]
        lResult = res["entities"]
        print(lResult)
        self.assertEqual(True, bResult)

    @unittest.skip("跳过这个测试用例")
    def test_busiTableStatus(self):
        url = r"http://120.77.217.209:8008/tableStatus"
        # url = r"http://127.0.0.1:8008/tableStatus"
        para = {"tableNo":""}
        para = json.dumps(para).encode("utf-8")
        req = request.Request(url=url, data=para)
        res = request.urlopen(req)
        res = res.read().decode("utf-8")
        res = json.loads(res)
        print(type(res))
        bResult = res["result"]
        lResult = res["entities"]
        print(lResult)
        self.assertEqual(True, bResult)

    @unittest.skip("跳过这个测试用例")
    def test_busiBillOpen(self):
        # url = r"http://120.77.217.209:8008/busiData/billOpen"
        url = r"http://127.0.0.1:8008/busiData/billOpen"
        para = {
            "terminal":"01",                # 终端号
            "table":"",                   # 桌台号
            "waiter":"",                  # 服务员号
            "guestNum":0                  # 客人数量
        }
        para = json.dumps(para).encode("utf-8")
        req = request.Request(url=url, data=para)
        res = request.urlopen(req)
        res = res.read().decode("utf-8")
        res = json.loads(res)
        print(type(res))
        bResult = res["result"]
        lResult = res["entities"]
        print(lResult)
        self.assertEqual(True, bResult)

    def test_busiBillPut(self):
        # url = r"http://120.77.217.209:8008/busiData/billPut"
        url = r"http://127.0.0.1:8008/busiData/billPut"
        para = {
            "terminal":"01",                # 终端号
            "billNo":"",                   # 单号
            "waiter":""                   # 服务员号
        }
        para = json.dumps(para).encode("utf-8")
        req = request.Request(url=url, data=para)
        res = request.urlopen(req)
        res = res.read().decode("utf-8")
        res = json.loads(res)
        print(type(res))
        bResult = res["result"]
        lResult = res["entities"]
        print(lResult)
        self.assertEqual(True, bResult)

    @unittest.skip("跳过这个测试用例")
    def test_busiBillGet(self):
        pass

if __name__ == '__main__':
    unittest.main()
