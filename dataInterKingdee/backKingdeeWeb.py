# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
from urllib import request
from http import cookiejar
import json
from myTools import MyJSONEncoder
import time
import uuid
from datetime import datetime
from busiProcess import BusiProcess
import ssl

class BackKingdeeWeb(BusiProcess):
    """
    Kingdee《金蝶云星空V7.2》作为业务后端，http访问：
    菜品资料：导入
    销售单据：导入
    """

    def __init__(self, sett, endType):
        """
        实例化
        :param sett:
        :param endType:
        """
        super().__init__(sett, endType)
        self.interType = "web"          # 接口类型 db:直连数据库 web:web访问
        self.interBase = "in"           # 基础资料传输方向 in:写入 out:导出
        self.interItems = {"item", "saleBill", "accBill"}  # 对接数据项 item:商品表 saleBill:销售单 accBill:财务凭证
        # self.interItems = {"item", "saleBill"}  # 临时测试调整
        self.interHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
        self.loginTime = None           # 登入时间戳
        self.loginToken = None          # 登录token
        self.timeOut = 11               # 登录失效时间（h）
        ssl._create_default_https_context = ssl._create_unverified_context
        self.cookie = cookiejar.CookieJar()              # 登录cookie
        self.BooksID = self._getBooksID()
        i = 0
        while not self.BooksID and i < 3:
            i += 1
            time.sleep(i)
            self.BooksID = self._getBooksID()
        if not self.BooksID:
            raise Exception("初始化[{name}]接口失败：获取帐套ID失败.".format(name=self.interName))

        # 建立菜品编码和ID之间的转换关系缓存
        self.foodMap = {}
        # 建立结算方式和ID之间的转换关系缓存
        self.payMap = {}
        # 建立部门在所在门店ID之间的转换关系缓存，同一个部门编码，在不同的门店ID不同
        self.deptMap = {}       # 金蝶的人说查看表单接口不要用，用批量查询字段集接口
        getDept = self._getBaseIDSet("BD_Department", "fNumber, fDeptID, fUseOrgID", "")
        if getDept["result"]:
            for line in getDept["entities"]["BD_Department"]["BD_Department"]:
                self.deptMap[line[2]] = line[1]
        # 建立用户在所在门店ID之间的转换关系缓存，同一个用户编码，在不同的门店ID不同
        self.userMap = {}       # 同部门资料，金蝶的人建议用批量查询字段集接口
        getUser = self._getBaseIDSet("SEC_User", "fNumber, fUserID", "len(fNumber) > 0")
        if getUser["result"]:
            for line in getUser["entities"]["SEC_User"]["SEC_User"]:
                self.userMap[line[0]] = line[1]

    def _getBooksID(self):
        """
        获取服务器帐套ID
        :return:
        """

        url = r"{serverIP}/K3Cloud/getalldatacenters.eatsun".format(serverIP=self.interConn["host"])
        req = request.Request(url=url, headers=self.interHeaders)
        res = request.urlopen(req)
        res = res.read().decode("utf-8")
        res = json.loads(res)
        bResult = res["Result"]
        if bResult:
            return res["ReturnValue"][0]["Id"]
        else:
            return None

    def _getBaseID(self, sType, sNumber, orgId):
        """
        获取基础资料ID
        :param sType: 类型/表名
            组织机构    ORG_Organizations
            部门      BD_Department
            用户      SEC_User
            菜品      DE_DIN_Food
            口味要求    DE_DIN_POSFeelInfo
            结算方式    BD_SETTLETYPE
        :param sNumber:编码
        :param orgId:创建组织ID
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        # 登录
        rtnLogin = self._login2()
        if not rtnLogin["result"]:
            raise Exception(rtnLogin["info"])

        # 提交数据
        url = r"{serverIP}/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.View.common.kdsvc".format(serverIP=self.interConn["host"])
        paraList = [sType]
        if orgId > 0:
            detail = r'{"CreateOrgId":%d, "Number":"%s"}' % (orgId, sNumber)
        else:
            detail = r'{"Number":"%s"}' % (sNumber)
        paraList.append(detail)
        rtnBase = self._request_by_cookie(url, paraList)
        if not rtnBase["Result"]["ResponseStatus"]:
            rtnData["result"] = True
            rtnData["dataNumber"] = rtnBase["Result"]["Result"]["Id"]
            rtnData["info"] = "Get ID successfully"
        else:
            rtnData["result"] = False
            rtnData["info"] = rtnBase["Result"]["ResponseStatus"]["Errors"][0]["FieldName"]

        return rtnData

    def _getBaseIDSet(self, sForm, sFields, sFilter):
        """
        表单查询，用于查询基础数据的编码和ID的对应关系
        :param sFrom:表名
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        # 登录
        rtnLogin = self._login2()
        if not rtnLogin["result"]:
            raise Exception(rtnLogin["info"])

        # 提交数据
        url = r"{serverIP}/k3cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery.common.kdsvc".format(serverIP=self.interConn["host"])
        paraList = []
        if len(sFilter) > 0:
            detail = r'{"FormId":"%s", "FieldKeys":"%s", "FilterString":"%s"}' % (sForm, sFields, sFilter)
        else:
            detail = r'{"FormId":"%s", "FieldKeys":"%s"}' % (sForm, sFields)
        paraList.append(detail)
        rtnBase = self._request_by_cookie(url, paraList)
        rtnData["result"] = True
        rtnData["entities"] = {}
        rtnData["entities"][sForm] = {}
        rtnData["entities"][sForm][sForm] = rtnBase
        rtnData["info"] = "Get {form} fields successfully".format(form=sForm)

        return rtnData

    def _distributeFood(self, lFood, lBranch):
        """
        批量为食品分配机构
        没有找到接口地址
        金蝶人员说该接口不可用，但可以直接在金蝶系统类配置自动分配规则
        :param lFood:
        :param lBranch:
        :return:
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "info":"",                      # 信息
            "entities": {}
        }

        # 登录
        rtnLogin = self._login2()
        if not rtnLogin["result"]:
            raise Exception(rtnLogin["info"])

        # 提交数据
        url = r"{serverIP}/K3Cloud/......".format(serverIP=self.interConn["host"])
        paraList = ["DE_DIN_Food"]
        sFoods = ""
        for i in lFood:
            if sFoods == "":
                sFoods = str(i)
            else:
                sFoods += "," + str(i)
        sBranchs = ""
        for i in lBranch:
            if sBranchs == "":
                sBranchs = str(i)
            else:
                sBranchs += "," + str(i)
        detail = r'{"PkIds":"%s", "TOrgIds":"%s", "IsAutoSubmitAndAudit":"true"}' % (sFoods, sBranchs)
        paraList.append(detail)
        rtnBase = self._request_by_cookie(url, paraList)
        if not rtnBase["Result"]["ResponseStatus"]:
            rtnData["entities"]["item"] = {}
            rtnData["entities"]["item"]["item"] = []
            rtnData["entities"]["item"]["item"].extend(lFood)
            rtnData["info"] = "Get ID successfully"
        else:
            rtnData["result"] = False
            rtnData["info"] = rtnBase["Result"]["ResponseStatus"]["Errors"][0]["FieldName"]

        return rtnData

    def _request_by_cookie(self, url, paraList):
        """
        网络请求（cookie版）
        :param url:
        :param paraList:
        :return:
        """

        cookie_handler = request.HTTPCookieProcessor(self.cookie)
        opener = request.build_opener(cookie_handler)
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            "Content-Type":"application/json"
        }
        headerList = []
        for key in headers:
            headerList.append((key, headers[key]))
        opener.addheaders = headerList
        para = json.dumps(paraList)
        data = {}
        data["format"] = 1
        data["useragent"] = "ApiClient"
        data["rid"] = str(hash(uuid.uuid1()))
        data["parameters"] = para
        data["timestamp"] = time.time()
        data["v"] = "1.0"
        data = json.dumps(data).encode("utf-8")
        req = request.Request(url=url, data=data, headers=headers)
        res = opener.open(req, timeout=1000*60*10)
        res = res.read().decode()
        res = json.loads(res, encoding="utf-8")

        return res

    def _login(self):
        """
        登录token
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "item": {                    # 表体代码
                    "item":[]                # 菜品表
                }
            }
        }
        # 判断登录是否已失效
        if self.loginToken and time.time() - self.loginTime < self.timeOut * 60 * 60:
            rtnData["result"] = True
            rtnData["info"] = "登录还在生效中"
            return rtnData

        # 登录
        url = r"{serverIP}/K3Cloud/login.eatsun".format(serverIP=self.interConn["host"])
        data = {
            "UserToken":"",
            "ActionName":"",
            "PostData":[
                {
                    "AccountID":self.BooksID,
                    "UserName":self.interConn["user"],
                    "Password":self.interConn["password"]
                }
            ]
        }
        data = json.dumps(data).encode("utf-8")
        req = request.Request(url=url, headers=self.interHeaders, data=data)
        res = request.urlopen(req)
        res = res.read().decode("utf-8")
        res = json.loads(res)
        bResult = res["Result"]
        if bResult:
            self.loginToken = res["ReturnValue"]
            self.loginTime = time.time()
            rtnData["result"] = True
            rtnData["info"] = "登录成功"
        else:
            self.loginToken = None
            self.loginTime = None
            rtnData["result"] = False
            rtnData["info"] = "登录失败：" + res["ReturnValue"]
        return rtnData

    def _login2(self):
        """
        登录cookie
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "item": {                    # 表体代码
                    "item":[]                # 菜品表
                }
            }
        }
        # 登录
        url = r"{serverIP}/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.AuthService.ValidateUser.common.kdsvc".format(serverIP=self.interConn["host"])
        paraList = []
        paraList.append(self.BooksID)
        paraList.append(self.interConn["user"])
        paraList.append(self.interConn["password"])
        paraList.append(2052)
        rtnLogin = self._request_by_cookie(url, paraList)
        if rtnLogin["LoginResultType"] == 1:
            rtnData["result"] = True
            rtnData["info"] = "登录成功"
        else:
            rtnData["result"] = False
            rtnData["info"] = "登录失败：" + rtnLogin["Message"]
        return rtnData

    def _putSaleBill(self, branch, putData):
        """
        导入销售单据
        :param branch: 金蝶门店ID
        :param putData:
        :return:
        """
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
        addList = []

        # 获取部门ID
        if branch in self.deptMap:
            deptId = self.deptMap[branch]
        else:
            raise Exception("查找机构[{org}]部门[{dept}]的ID失败.".format(org=branch, dept=self.sett.deptNo))

        # 提交数据
        url = r"{serverIP}/K3Cloud/v1.eatsun".format(serverIP=self.interConn["host"])
        data = {
            "AppID": "",                                            # 预留开发商ID
            "ActionName": "FoodSalesBill/add",                  # 固定值
            "UserToken": self.loginToken,
            "PostData": []
        }
        for i in putData["entities"]["saleBill"]["bill"]:
            bBase = True                                          # 临时处理：如果食品编码没有找到，放弃单据
            sBill = i[0]
            newBill = {
                "OrgId": branch,                                    # 组织ID
                "DeptId": deptId,                                   # 部门ID
                "ShopDay": datetime.strftime(i[2], "%Y-%m-%d"),    # 营业日期
                "IsEndDay": "1",                                    # 清机标志，0-未清机，1-已清机
                "BillSequence": sBill,                              # 帐单流水号
                "FoodSalesBillItems": []                            # 帐单食品明细项
            }
            data["PostData"].append(newBill)
            for j in putData["entities"]["saleBill"]["item"]:
                if sBill == j[0]:
                    if j[14] == "单品":
                        iItemSuit = 1
                    elif j[14] == "套餐":
                        iItemSuit = 3
                        # 忽略：把套餐当单品处理
                        continue
                    elif j[14] == "套餐子项":
                        iItemSuit = -1
                        # 转化：把套餐当单品处理
                        iItemSuit = 1
                    else:
                        continue
                    if j[4] in self.foodMap:
                        foodId = self.foodMap[j[4]]
                    else:
                        getFood = self._getBaseID("DE_DIN_Food", j[4], 0)
                        if getFood["result"]:
                            foodId = getFood["dataNumber"]
                            self.foodMap[j[4]] = foodId
                        else:
                            # raise Exception("获取{end}门店食品[{food}]的ID失败.".format(end=self.interName, food=j[4]))
                            # 食品编码没有找到，放弃单据
                            bBase = False
                            break
                    if iItemSuit == -1:
                        suitItem = {
                            "FoodId": foodId,
                            "Qty": str(j[9]),
                            "Amount": str(j[13])
                        }
                        newItem["FoodCombineItems"].append(suitItem)
                    elif iItemSuit == 1 or iItemSuit == 3:
                        newItem = {
                            "FoodId":foodId,
                            "Qty":str(j[9]),
                            "Amount":str(j[13]),
                            "FoodType":iItemSuit,
                            "FeelItems":[],
                            "FoodCombineItems":[]
                        }
                        data["PostData"][len(data["PostData"]) - 1]["FoodSalesBillItems"].append(newItem)
            if bBase:
                addList.append((sBill, "", i[1], datetime.strftime(i[2], "%Y-%m-%d")))
            else:
                # 食品编码没有找到，放弃单据
                data["PostData"].pop()

        data = json.dumps(data, cls=MyJSONEncoder).encode("utf-8")
        req = request.Request(url=url, headers=self.interHeaders, data=data)
        res = request.urlopen(req)
        res = res.read().decode("utf-8")
        res = json.loads(res)
        bResult = res["Result"]
        if bResult:
            rtnData["result"] = True
            rtnData["info"] = "Successfully handled"
            rtnData["entities"]["saleBill"]["bill"].extend(addList)
        else:
            rtnData["result"] = False
            rtnData["info"] = res["ReturnValue"]["ErrorMessage"]
            self.sett.logger.info("导入菜品销售单失败:{info}".format(info=rtnData["info"]))

        return rtnData

    def _putAccBill(self, branch, putData):
        """
        获取财务单据
        :param branch: 金蝶门店ID
        :param putData:
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {                   # 表体集
                "accBill": {                # 表体代码
                    "bill":[]                # 销售单
                }
            }
        }
        addList = []

        # 获取部门ID
        if branch in self.deptMap:
            deptId = self.deptMap[branch]
        else:
            raise Exception("查找机构[{org}]部门[{dept}]的ID失败.".format(org=branch, dept=self.sett.deptNo))

        # 获取用户ID
        if self.sett.userNo in self.userMap:
            userId = self.userMap[self.sett.userNo]
        else:
            raise Exception("查找用户[{user}]ID失败.".format(user=self.sett.userNo))

        # 提交数据
        url = r"{serverIP}/K3Cloud/v1.eatsun".format(serverIP=self.interConn["host"])
        data = {
            "AppID": "",                                            # 预留开发商ID
            "ActionName": "RevenueFinancial/add",               # 固定值
            "UserToken": self.loginToken,
            "PostData": []
        }
        for i in putData["entities"]["accBill"]["bill"]:
            bBase = True                                            # 临时处理：如果食品编码没有找到，放弃单据
            sBill = i[0]
            newBill = {
                "OrgId": branch,                                     # 使用组织ID(必填)
                "UserId": userId,                                   # 用户ID(必填)
                "FPosBillID": int(sBill),                           # 门店单据id(必填)
                "FDate": datetime.strftime(i[2], "%Y-%m-%d"),      # 营业日期
                "FTotalBillTax": float(i[5]),                       # 账单价税合计
                "FTotalServiceFeeTax": float(i[6] + i[7] - i[8] + i[9]),  # 服务费价税合计
                "FBillTax": float(0.00),                             # 账单税额
                "FServiceFeeTax": float(0.00),                      # 服务费税额
                "Remark": i[13],                                     # 备注
                "SettlementEntity": [],                            # 结算方式明细
                "FoodEntity": []                                    # 帐单食品明细项
            }
            data["PostData"].append(newBill)
            for j in putData["entities"]["accBill"]["pay"]:
                if sBill == j[0]:
                    if j[4] in self.sett.payment:
                        payNo = self.sett.payment[j[4]]
                    elif "other" in self.sett.payment:
                        payNo = self.sett.payment["other"]
                    else:
                        raise Exception("支付方式[{pay}]没有配置.".format(pay=j[4]))
                    # 根据number获取id
                    if payNo in self.payMap:
                        payId = self.payMap[payNo]
                    else:
                        getPay = self._getBaseID("BD_SETTLETYPE", payNo, 0)
                        if getPay["result"]:
                            payId = getPay["dataNumber"]
                            self.payMap[payNo] = payId
                        else:
                            raise Exception("获取{end}结算方式[{pay}]的ID失败.".format(end=self.interName, pay=payNo))
                    payEntity = {
                        "FSettlementEncoding":payId,                # 结算方式ID
                        "FSettlementAmount":float(j[10]),           # 结算金额
                        "FMemberPrincipal":float(0.00),             # 会员本金
                        "FMembershipGrants":float(0.00)             # 会员赠金
                    }
                    data["PostData"][len(data["PostData"]) - 1]["SettlementEntity"].append(payEntity)
            for j in putData["entities"]["accBill"]["item"]:
                if sBill == j[0]:
                    if j[14] == "套餐":
                        continue
                    if j[4] in self.foodMap:
                        foodId = self.foodMap[j[4]]
                    else:
                        getFood = self._getBaseID("DE_DIN_Food", j[4], 0)
                        if getFood["result"]:
                            foodId = getFood["dataNumber"]
                            self.foodMap[j[4]] = foodId
                        else:
                            # raise Exception("获取{end}食品[{food}]的ID失败.".format(end=self.interName, food=j[4]))
                            # 食品编码没有找到，放弃单据
                            bBase = False
                            break
                    saleEntity = {
                        "FoodId":foodId,
                        "FdeptId":deptId,
                        "FSales":float(j[9]),
                        "FLeviedTotal":float(j[13]),
                        "FNonTaxAmount":float(j[13]),
                        "FTax":float(0.00)
                    }
                    data["PostData"][len(data["PostData"]) - 1]["FoodEntity"].append(saleEntity)
            if bBase:
                addList.append((sBill, "", i[1], datetime.strftime(i[2], "%Y-%m-%d")))
            else:
                # 食品编码没有找到，放弃单据
                data["PostData"].pop()

        data = json.dumps(data, cls=MyJSONEncoder).encode("utf-8")
        req = request.Request(url=url, headers=self.interHeaders, data=data)
        res = request.urlopen(req)
        res = res.read().decode("utf-8")
        res = json.loads(res)
        bResult = res["Result"]
        if bResult:
            rtnData["result"] = True
            rtnData["info"] = res["ReturnValue"]
            rtnData["entities"]["accBill"]["bill"].extend(addList)
        else:
            rtnData["result"] = False
            rtnData["info"] = res["ReturnValue"]
            self.sett.logger.info("导入财务记账单失败:{info}".format(info=rtnData["info"]))

        return rtnData

    def putBaseData(self, putData):
        """
        基础资料导入
        :param putData:
        :return:
        """
        rtnData = {
            "result":True,                 # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"Successfully handled",# 信息
            "entities": {                   # 表体集
                "item": {                    # 表体代码
                    "item":[]                # 菜品表
                }
            }
        }

        # 登录
        rtnLogin = self._login2()
        if not rtnLogin["result"]:
            raise Exception(rtnLogin["info"])

        # 提交数据
        url = r"{serverIP}/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Save.common.kdsvc".format(serverIP=self.interConn["host"])
        for i in putData["entities"]["item"]["item"]:
            paraList = ["DE_DIN_Food"]
            detail = r'{' \
                r'"Creator": "",' \
                r'"NeedUpDateFields": [],' \
                r'"NeedReturnFields": [],' \
                r'"IsDeleteEntry": "true",' \
                r'"SubSystemId": "",' \
                r'"IsVerifyBaseDataField": "false",' \
                r'"IsEntryBatchFill": "true",' \
                r'"ValidateFlag": "true",' \
                r'"NumberSearch": "true",' \
                r'"InterationFlags": "",' \
                r'"IsAutoSubmitAndAudit": "false",' \
                r'"Model": {' \
                    r'"FoodID": 0,' \
                    r'"FCreateOrgId": {' \
                        r'"FNumber": "%s"' \
                    r'},' \
                    r'"FUseOrgId": {' \
                        r'"FNumber": "%s"' \
                    r'},' \
                    r'"FNumber": "%s",' \
                    r'"FName": "%s",' \
                    r'"FFoodCode": "CSP",' \
                    r'"FKindNo": {' \
                        r'"FNumber": "%s"' \
                    r'},' \
                    r'"FFoodType": "1",' \
                    r'"FPrice": %d,' \
                    r'"FIsCurrPrice": false,' \
                    r'"FIsSyncToO2O": false,' \
                    r'"FDisplayInPen": true,' \
                    r'"FDisplayInPad": true,' \
                    r'"FCanDisc": false,' \
                    r'"FIsDiscAll": false,' \
                    r'"FCanFree": false,' \
                    r'"FCanChangeAmt": false,' \
                    r'"FCanChangeQty": false,' \
                    r'"FCanCheck1": true,' \
                    r'"FIsService": false,' \
                    r'"FAutoFreeServiceAmt": false,' \
                    r'"FIsFixAmt": false,' \
                    r'"FIsFastSplit": false,' \
                    r'"FIsSumPrnt": true,' \
                    r'"FIsBillPrnt": true,' \
                    r'"FIsPrint": true,' \
                    r'"FIsLocal": false,' \
                    r'"FLocaBill": false,' \
                    r'"FIsPrnSale": false,' \
                    r'"FIsClearSaleLmt": false,' \
                    r'"FIsUserDefine": false,' \
                    r'"FIsPrefDiscFood": false,' \
                    r'"FIsDisale": false,' \
                    r'"FCanModyName": false,' \
                    r'"FIsRevoked": false,' \
                    r'"FBardCode": "%s",' \
                    r'"FMaxConsQtyMode": "1",' \
                    r'"FTaxClassify": {' \
                        r'"FNumber": "WLDSFL01_SYS"' \
                    r'},' \
                    r'"FRateDefault": {' \
                        r'"FNUMBER": "SL06_SYS"' \
                    r'},' \
                    r'"FIsScalage": false,' \
                    r'"FPosIsVisible": true,' \
                    r'"FHasFoodMaterial": false,' \
                    r'"FIfFromMaterial": false,' \
                    r'"FoodCalcTime_Entity": {}' \
                r'}' \
            r'}' % (self.sett.defaultOrgNo, self.sett.defaultOrgNo, i[0], i[1][:30], self.sett.clsBigNo, i[5], ("000000" + str(self.sett.maxBarcode))[-6:])
            paraList.append(detail)
            rtnBase = self._request_by_cookie(url, paraList)
            if rtnBase["Result"]["ResponseStatus"]["IsSuccess"]:
                rtnData["entities"]["item"]["item"].append((i[0], i[1], "", ""))
                self.sett.maxBarcode += 1
            else:
                rtnData["result"] = False
                rtnData["info"] = rtnBase["Result"]["ResponseStatus"]["Errors"][0]["FieldName"]
                self.sett.logger.error(rtnData["info"])
                break

        return rtnData

    def putBusiData(self, branch, putData):
        """
        销售单据导入
        :param branch: 门店
        :param dictData: 传入的销售单据
            maxDate:    本次同步的最大日期
            bill:       主单表集合
            item:       商品表集合
            pay:        付款表集合
        :return:
        """
        rtnData = {
            "result":True,                  # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":1,                # 数字
            "info":"",                      # 信息
            "entities": {}                  # 表体集
        }

        # 登录
        sRet = self._login()
        if not self.loginToken:
            raise Exception(sRet)

        if "saleBill" in putData["entities"]:
            rtn1 = self._putSaleBill(branch, putData)
            rtnData["result"] = rtn1["result"]
            rtnData["info"] = rtn1["info"]
            if rtn1["result"] == True:
                rtnData["entities"]["saleBill"] = {}
                rtnData["entities"]["saleBill"]["bill"] = []
                rtnData["entities"]["saleBill"]["bill"].extend(rtn1["entities"]["saleBill"]["bill"])
        if "accBill" in putData["entities"]:
            rtn2 = self._putAccBill(branch, putData)
            rtnData["result"] = rtn2["result"]
            rtnData["info"] = rtn2["info"]
            if rtn2["result"] == True:
                rtnData["entities"]["accBill"] = {}
                rtnData["entities"]["accBill"]["bill"] = []
                rtnData["entities"]["accBill"]["bill"].extend(rtn2["entities"]["accBill"]["bill"])

        return rtnData
