# -*- coding:utf-8 -*-
"""
消息转发站
"""
import configparser
import win32api, win32gui
import win32con, winerror
from ctypes import windll
import sys, os, time, datetime
import logging
from queue import Queue
import socket
from threading import Thread
from datetime import datetime

class MainWindow:
    def __init__(self):
        self.code = "TabletOrderingYD"
        self.name = "平板点餐服务YD"

        # 获取编程环境下的代码路径
        # self.path = os.path.abspath(os.path.dirname(__file__))
        # 获取打包后的可执行文件路径
        self.path = os.path.dirname(sys.executable)

        # 获取配置参数
        config = configparser.ConfigParser()
        confFile = os.path.join(self.path, "wx.conf")
        if os.path.exists(confFile):
            config.read(confFile, encoding="utf-8")
            self.WXPort = config.getint("client", "WXPort")
            if self.WXPort == 0 or self.WXPort == None:
                self.WXPort = 8009
        else:
            self.WXPort = 8009
        self.logFile = os.path.join(self.path, "wxlog.log")

        # 创建日志对象
        self.logger = self._getLogger()

        msg_TaskbarRestart = win32gui.RegisterWindowMessage("TaskbarCreated")
        message_map = {
            msg_TaskbarRestart: self.OnRestart,
            win32con.WM_CLOSE: self.OnClose,
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_COMMAND: self.OnCommand,
            win32con.WM_USER + 20: self.OnTaskbarNotify,
            1280: self.OnPostMessage,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = self.code
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map  # could also specify a wndproc.

        # Don't blow up if class already registered to make testing easier
        try:
            classAtom = win32gui.RegisterClass(wc)
        except Exception as e:
            self.logger.error(str(e))

                # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(wc.lpszClassName, self.name, style,
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        self._DoCreateIcons()

        # 获取启动WX窗口的程序句柄
        self._interHandle = 0
        if len(sys.argv) > 1:
            if sys.argv[1].isdigit():
                if self._interHandle == 0 and int(sys.argv[1]) > 0:
                    self._interHandle = int(sys.argv[1])

        # 初始化登录标志
        self._loginFlag = 0

        # 创建socket server线程
        if self._interHandle > 0:
            # 通知接口程序WX的窗口句柄
            windll.user32.PostMessageW(self._interHandle, 1280, 0, self.hwnd)

            # 创建线程共享数据队列
            self.messageQ = Queue()

            try:
                tSocket = Thread(target=self.OnSocket, args=(self.WXPort, self.messageQ, self._interHandle, ))
                tSocket.daemon = True
                tSocket.start()
            except Exception as e:
                self.logger.error("启动进程Err:" + str(e))

    def _DoCreateIcons(self):
        # Try and find a custom icon
        hinst = win32api.GetModuleHandle(None)
        iconPathName = os.path.abspath(os.path.join(os.path.split(sys.executable)[0], "pyc.ico"))
        if not os.path.isfile(iconPathName):
            # Look in DLLs dir, a-la py 2.5
            iconPathName = os.path.abspath(os.path.join(os.path.split(sys.executable)[0], "DLLs", "pyc.ico"))
        if not os.path.isfile(iconPathName):
            # Look in the source tree.
            iconPathName = os.path.abspath(os.path.join(os.path.split(sys.executable)[0], "..\\PC\\pyc.ico"))
        if os.path.isfile(iconPathName):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        else:
            # print("Can't find a Python icon file - using default")
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, self.name)
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except Exception as e:
            # This is common when windows is starting, and this code is hit
            # before the taskbar has been created.
            print("Failed to add the taskbar icon - is explorer running?")
            # but keep running anyway - when explorer starts, we get the
            # TaskbarCreated message.

    def OnSocket(self, WXPort, messageQ, interHandle):
        try:
            socketSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketSrv.bind(("127.0.0.1", WXPort))
            socketSrv.listen(50)
            while True:
                client, _ = socketSrv.accept()  # 开始监听，阻塞，等待客户端连接
                # 给每个客户端创建一个独立的线程进行管理
                thread = Thread(target=self.socketHandle, args=(client, messageQ, interHandle,))
                # 设置成守护线程
                thread.setDaemon(True)
                thread.start()
        except Exception as e:
            self.logger.error(str(e))

    def socketHandle(self, client, messageQ, interHandle):
        """
        消息处理
        :param client:
        :return:
        """
        bytes = client.recv(1024)
        if len(bytes) > 0:
            data = int(bytes.decode("utf-8"))
            windll.user32.PostMessageW(interHandle, 1280, 0, data)
            iTimeOut = 45000
            iWait = 0
            while iWait < iTimeOut:
                item = messageQ.get()
                if item == data:
                    client.sendall(str(data).encode("utf-8"))
                    break
                else:
                    messageQ.put(data)
                    time.sleep(0.3)
                    iWait += 300

    def OnPostMessage(self, hwnd, msg, wparam, lparam):
        if hwnd == self.hwnd:
            self.messageQ.put(lparam)

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._DoCreateIcons()

    def OnClose(self, hwnd, msg, wparam, lparam):
        """
        收到关闭消息
        :param hwnd:
        :param msg:
        :param wparam:
        :param lparam:
        :return:
        """
        win32gui.DestroyWindow(self.hwnd)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        """
        收到销毁消息
        :param hwnd:
        :param msg:
        :param wparam:
        :param lparam:
        :return:
        """
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONUP:
            pass
            # print("You clicked me.")
        elif lparam == win32con.WM_LBUTTONDBLCLK:
            # print("You double-clicked me - goodbye")
            # win32gui.DestroyWindow(self.hwnd)
            pass
        elif lparam == win32con.WM_RBUTTONUP:
            # print("You right clicked me.")
            menu = win32gui.CreatePopupMenu()
            # win32gui.AppendMenu(menu, win32con.MF_STRING, 1023, "Display Dialog")
            # win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, "Say Hello")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, "退出")
            pos = win32gui.GetCursorPos()
            # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)
        """
        if id == 1023:
            import win32gui_dialog
            win32gui_dialog.DemoModal()
        if id == 1024:
            print("Hello")
        """
        if id == 1025:
            # print("Goodbye")
            win32gui.DestroyWindow(self.hwnd)
        else:
            print("Unknown command -", id)

    def _getLogger(self):
        logger = logging.getLogger("[{code}]".format(code=self.code))
        handler = logging.FileHandler(self.logFile)
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

def main():
    w = MainWindow()
    win32gui.PumpMessages()


if __name__ == '__main__':
    main()
