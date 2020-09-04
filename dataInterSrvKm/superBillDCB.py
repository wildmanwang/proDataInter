# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
from os import path
import time

class SuperBillDCB():
    """
    点菜宝父类
    """

    def __init__(self, sett):
        self.sett = sett
        self.station = []

    def _getStation(self):
        """
        获取基站号
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        if len(self.station) == 0:
            rtnData["info"] = "基站繁忙，请稍后再试"
        else:
            rtnData["result"] = True
            self.station.sort()
            rtnData["dataNumber"] = self.station.pop(0)

        return rtnData

    def _writeBusiData(self, station, data):
        """
        写通讯数据到文件
        :param station: 基站号
        :param data: 数据列表，一项表示一行
        :return:
        """
        rtnData = {
            "result":True,                 # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }
        if station >=0 and station <= 8:
            filename = path.join(self.sett.dataPath, "T{station}.txt".format(station=str(station)))
        elif station == 10:
            filename = path.join(self.sett.dataPath, "DL.txt")
        else:
            rtnData["result"] = False
            rtnData["info"] = "基站号超出范围：{num}".format(num=station)

        if rtnData["result"]:
            data = [i + "\n" for i in data]
            with open(filename, "w", encoding="utf-8") as f:
                f.writelines(data)
            time.sleep(0.1)
            rtnData["result"] = True

        if rtnData["result"]:
            rtnData = self._socketRequest(station)

        return rtnData

    def _socketRequest(self, station):
        """
        向WX发送操作请求
        :param station:
        :return:
        """
        rtnData = {
            "result": False,            # 逻辑控制 True/False
            "dataString": "",           # 字符串
            "dataNumber": 0,            # 数字
            "info": "",                 # 信息
            "entities": {}
        }

        import socket

        sock = socket.socket()
        sock.settimeout(45)
        sock.connect((self.sett.WXServer, self.sett.WXPort))
        try:
            self.sett.logger.info("Srv-socket发送开台请求：{num}".format(num=station))
            sock.send(str(station).encode("utf-8"))
            rtnData["dataNumber"] = int(sock.recv(1024).decode("utf-8"))
            self.sett.logger.info("Srv-socket收到处理结果：{num}".format(num=rtnData["dataNumber"]))
            rtnData["result"] = True
        except socket.timeout as e:
            rtnData["dataNumber"] = 0
            rtnData["info"] = "数据处理超时，请稍后重试"
        except Exception as e:
            rtnData["dataNumber"] = -1
            rtnData["info"] = str(e)

        sock.close()

        return  rtnData

    def _readRtnData(self, station, operType, data, judgeType = 0, judgeStr = "", judgeLine = 1):
        """
        读操作返回结果
        :param station:基站号
        :param operType: 操作类型，用于提示信息
        :param data: 请求的数据，用于与结果对比
        :param judgeType: 判断类型 0 直接判断结果=1 1 间接比较字符串
        :param judgeStr: 当judgeType=1时有用，返回结果匹配到指定字符串则执行成功，否则，返回结果第一个字符=1则执行成功
        :param judgeLine: 判断行数 当judgeType=1时有用，以返回信息第几行为标准判断是否成功
        :return:
        """
        rtnData = {
            "result":True,                 # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }
        filename = ""
        if station >=0 and station <= 8:
            filename = path.join(self.sett.dataPath, "R{station}.txt".format(station=str(station)))
        elif station == 10:
            filename = path.join(self.sett.dataPath, "DL.txt")
        else:
            rtnData["result"] = False
            rtnData["info"] = "基站号超出范围：{num}".format(num=station)

        if len(filename) > 0:
            time.sleep(self.sett.fileWait / 1000)
            if not path.exists(filename):
                rtnData["result"] = False
                rtnData["info"] = "操作返回文件[{file}]不存在".format(file=filename)

        if rtnData["result"]:
            with open(filename, "r", encoding="ANSI") as f:
                readCon = f.readlines()
            if len(readCon) >= 2:
                if readCon[0][:8] == data[0][:8]:
                    if judgeType == 0:
                        if readCon[judgeLine][0] != "1":
                            rtnData["result"] = False
                    elif judgeType == 1:
                        judgeStr = judgeStr.strip()
                        if len(judgeStr) > 0:
                            if judgeStr not in readCon[judgeLine]:
                                rtnData["result"] = False
                    else:
                        rtnData["result"] = False
                    for i in readCon[1:]:
                        if i[0:2] == "1 ":
                            rtnData["info"] += (i[2:].rstrip() + "\n")
                        else:
                            rtnData["info"] += (i.rstrip() + "\n")
                else:
                    rtnData["result"] = False
                    rtnData["info"] = "{type}返回的结果[{read}]与请求[{req}]不匹配".format(type=operType, read=readCon[0].rstrip(), req=data[0].rstrip())
            else:
                rtnData["result"] = False
                rtnData["info"] = "{type}返回的数据格式错误，R{i}应至少返回2行信息".format(type=operType, i=station)

        return rtnData

    def _readBasicData(self, filename):
        """
        读取基础资料数据
        :param filename: 文件名
        :return:
        """
        rtnData = {
            "result": True,  # 逻辑控制 True/False
            "dataString": "",  # 字符串
            "dataNumber": 0,  # 数字
            "info": "",  # 信息
            "entities": {}
        }
        if len(filename) > 0:
            filename = path.join(self.sett.dataPath, filename)
            if path.exists(filename):
                with open(filename, "r", encoding="ANSI") as f:
                    pass        #读取文件
            else:
                rtnData["result"] = False
                rtnData["info"] = "文件不存在：" + filename
        else:
            rtnData["result"] = False
            rtnData["info"] = "基础资料文件名无效"

        return rtnData

    def userLogin(self, data):
        """
        登录
        :param data:
        :return:
        """
        pass

    def billOpen(self, data):
        """
        开台
        :param data:
        :return:
        """
        pass

    def billPut(self, data):
        """
        下单
        :param data:
        :return:
        """
        pass

if __name__ == "__main__":
    from interConfig import Settings
    sett = Settings()
    obj = SuperBillDCB(sett)
    obj._writeBusiData(9, "T", ["AAA1", "BBBB1B", "CCCCCC1CC"])
