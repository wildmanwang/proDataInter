"""
"""

class OrmBase(object):
    def queryFilter(self, session, model, para):
        """
        查询条件处理
        para:[
            "colname":      字段名,
            "oper":         比较方式,
            "value":        值
        ]
        枚举：
            比较方式            值
            >                   3 or date or datetime
            >=                  3 or date or datetime
            ==                  3 or "abc" or date or datetime
            <=                  3 or date or datetime
            <                   3 or date or datetime
            !=                  3 or "abc" or date or datetime
            between             (1, 3) or (date1, date2) or (time1, time2)
            in                  [1, 3, 9] or ["a", "bb", "f"] or [date1, date2, date3]
            not in              [1, 3, 9] or ["a", "bb", "f"] or [date1, date2, date3]
            like                "a%" or "%a" or "%a%"
        """
        rtnData = {
            "result":False,                # 逻辑控制 True/False
            "dataString":"",               # 字符串
            "dataNumber":0,                # 数字
            "dataObj":None,
            "info":"",                      # 信息
            "entities": {}
        }

        try:
            objQuery = session.query(model)
            for line in para:
                objValue = line["value"]
                if line["oper"] == ">":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) > objValue)
                elif line["oper"] == ">=":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) >= objValue)
                elif line["oper"] == "==":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) == objValue)
                elif line["oper"] == "<=":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) <= objValue)
                elif line["oper"] == "<":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) < objValue)
                elif line["oper"] == "!=":
                    objQuery = objQuery.filter(getattr(model, line["colname"]) != objValue)
                elif line["oper"] == "between":
                    if type(objValue) in (list, tuple):
                        if len(objValue) == 2:
                            objQuery = objQuery.filter(getattr(model, line["colname"]).between(*objValue))
                elif line["oper"] == "in":
                    if type(objValue) == list:
                        objQuery = objQuery.filter(getattr(model, line["colname"]).in_(objValue))
                elif line["oper"] == "not in":
                    if type(objValue) == list:
                        objQuery = objQuery.filter(getattr(model, line["colname"]).notin_(objValue))
                elif line["oper"] == "like":
                    if type(objValue) == str:
                        objQuery = objQuery.filter(getattr(model, line["colname"]).like(objValue))
            rtnData["result"] = True
            rtnData["dataObj"] = objQuery
        except Exception as e:
            rtnData["info"] = str(e)

        return rtnData
