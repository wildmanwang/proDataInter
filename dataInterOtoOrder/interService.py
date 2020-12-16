# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"

import win32serviceutil
import win32service
import win32event
import os
import sys
import inspect
from interConfig import Settings
from interControl import InterControl
import win32timezone        #打包需要


class DataInterCatering(win32serviceutil.ServiceFramework):
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

    _svc_name_ = "YunTongO2O"
    _svc_display_name_ = "Data interface of YunTong"
    _svc_description_ = "This is a data interface of YunTong."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.sett = Settings()
        try:
            self.inter = InterControl(self.sett)
        except Exception as e:
            sError = str(e)
            self.sett.logger.error(sError)

    def SvcDoRun(self):
        import schedule
        import time

        self.sett.logger.info("service is running...")

        try:
            self.inter.interInit()
        except Exception as e:
            sError = str(e)
            self.sett.logger.error(sError)
        else:
            sException = []
            self.sett.logger.info("同步商品资料...")
            self.inter.interBaseData()
            self.sett.logger.info("同步线上订单...")
            self.inter.interBusiData()
            self.sett.logger.info("同步订单状态...")
            self.inter.interOrderFeedback()
            self.sett.logger.info("同步商品库存...")
            self.inter.interStock()
            try:
                if self.sett.timingItemTime != "--:--":
                    schedule.every().day.at(self.sett.timingItemTime).do(self.inter.interBaseData)
                if self.sett.timingItemInterval > 0:
                    schedule.every(self.sett.timingItemInterval).minutes.do(self.inter.interBaseData)
                if self.sett.timingOrderTime != "--:--":
                    schedule.every().day.at(self.sett.timingOrderTime).do(self.inter.interBusiData)
                if self.sett.timingOrderInterval > 0:
                    schedule.every(self.sett.timingOrderInterval).minutes.do(self.inter.interBusiData)
                if self.sett.timingFeedbackTime != "--:--":
                    schedule.every().day.at(self.sett.timingFeedbackTime).do(self.inter.interOrderFeedback)
                if self.sett.timingFeedbackInterval > 0:
                    schedule.every(self.sett.timingFeedbackInterval).minutes.do(self.inter.interOrderFeedback)
                if self.sett.timingStockTime != "--:--":
                    schedule.every().day.at(self.sett.timingStockTime).do(self.inter.interStock)
                if self.sett.timingStockInterval > 0:
                    schedule.every(self.sett.timingStockInterval).minutes.do(self.inter.interStock)
                if self.sett.timingStateInterval > 0:
                    schedule.every(self.sett.timingStateInterval).minutes.do(self.inter.interItemStatus)
            except Exception as e:
                sError = str(e)
                self.sett.logger.error(sError)
            while self.sett.run:
                if not self.sett.processing:
                    try:
                        self.sett.processing = True
                        schedule.run_pending()
                    except Exception as e:
                        sError = str(e)
                        if sError not in sException:
                            self.sett.logger.error(sError)
                            sException.append(sError)
                    finally:
                        self.sett.processing = False
                time.sleep(1)

    def SvcStop(self):
        self.sett.logger.info("service is stoped.")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.sett.run = False


if __name__ == "__main__":
    import servicemanager
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(DataInterCatering)
            servicemanager.Initialize("DataInterCatering", evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(DataInterCatering)
