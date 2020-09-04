# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import win32serviceutil
import win32service
import win32event
import os
import logging
import inspect


class DataInterkm(win32serviceutil.ServiceFramework):
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

    _svc_name_ = "DataInterkm"
    _svc_display_name_ = "Data interface for kmcy"
    _svc_description_ = "This is a data interface for kmcy and app."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.run = True

    def _getLogger(self):
        logger = logging.getLogger("[DataInterkm]")

        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "service.log"))

        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcDoRun(self):
        import time
        self.logger.info("service is run...")
        while self.run:
            self.logger.info("I am running...")
            time.sleep(10)

    def SvcStop(self):
        self.logger.info("service is stop...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False


if __name__ == "__main__":
    import sys
    import servicemanager
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(DataInterkm)
            servicemanager.Initialize("DataInterkm", evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(DataInterkm)
