# -*- coding:utf-8 -*-
"""
自定义工具类
"""
__author__ = "Cliff.wang"

import json
from decimal import Decimal
from datetime import datetime

class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return str(o)
        else:
            return super().default(o)
