# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import os
from interConfig import Settings
#from interProcess import InterProcess
from interControl import InterControl

if __name__ == "__main__":
    try:
        path = os.path.abspath(os.path.dirname(__file__))
        sett = Settings(path, "config")
        inter = InterControl(sett)
        inter.interInit()
        if 1 == 2:
            # 传输基础资料、业务数据
            inter.interBusiData()
        elif 1 == 2:
            # 获取部门ID和用户ID
            pass
    except Exception as e:
        print(str(e))
