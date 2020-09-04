# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import win32serviceutil
import win32service
import win32event
import os
import sys
import logging
import inspect
from interConfig import Settings
from interProcess import InterProcess
import win32timezone        #打包报错引入


class DataInterDine(win32serviceutil.ServiceFramework):
    """
    #1.安装服务
    python tmpService.py install
    #2.让服务自动启动
    python tmpService.py --startup auto install
    #3.启动服务
    python tmpService.py start
    #4.重启服务
    python tmpService.py restart
    #5.停止服务
    python tmpService.py stop
    #6.删除/卸载服务
    python tmpService.py remove
    """

    _svc_name_ = "DataInterDine"
    _svc_display_name_ = "Data interface for Dine"
    _svc_description_ = "This is a data interface for erp and app."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        # 获取编程环境下的代码路径
        # self.path = os.path.abspath(os.path.dirname(__file__))
        # 获取打包后的可执行文件路径
        self.path = os.path.dirname(sys.executable)
        self.sett = Settings(os.path.join(self.path, "config"))
        self.inter = InterProcess(self.sett)
        self.logger = self._getLogger()
        self.run = True
        self.processing = False

    def _getLogger(self):
        logger = logging.getLogger("[DataInterDine]")
        handler = logging.FileHandler(os.path.join(self.path, "service.log"))
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcDoRun(self):
        import time

        self.logger.info("service is run...")

        sException = []

        try:
            self.inter.interInit(True)
        except Exception as e:
            sError = str(e)
            if sError not in sException:
                self.logger.error(sError)
                sException.append(sError)

        while self.run:
            if not self.processing:
                self.processing = True
                bInitOK = False

                # 基础资料同步
                try:
                    self.inter.interInit(False)
                    bInitOK = True
                except Exception as e:
                    sError = str(e)
                    if sError not in sException:
                        self.logger.error(sError)
                        sException.append(sError)

                # 单据同步
                if bInitOK:
                    try:
                        self.inter.interToErp()
                    except Exception as e:
                        sError = str(e)
                        if sError not in sException:
                            self.logger.error(sError)
                            sException.append(sError)

                self.processing = False
            time.sleep(self.sett.bill_get_interval)

    def SvcStop(self):
        self.logger.info("service is stop...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False


if __name__ == "__main__":
    import servicemanager
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(DataInterDine)
            servicemanager.Initialize("DataInterDine", evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(DataInterDine)
