# -*- coding:utf-8 -*-
"""
"""
__author__ = "Cliff.wang"
import win32con,win32gui, win32api
import time
from ctypes import windll

class MyWindow():
    def __init__(self):
        #注册一个窗口类
        wc = win32gui.WNDCLASS()
        wc.lpszClassName = 'MyWindow'
        wc.hbrBackground = win32con.COLOR_BTNFACE+1 #这里颜色用法有点特殊，必须+1才能得到正确的颜色
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDI_APPLICATION)
        wc.lpfnWndProc = self.wndProc #可以用一个函数，也可以用一个字典

        class_atom = win32gui.RegisterClass(wc)
        #创建窗口
        self.hwnd = win32gui.CreateWindow(
            class_atom, '平板点餐服务YD', win32con.WS_OVERLAPPEDWINDOW,
            win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
            0,0, 0, None)
        #设置窗口大小
        win32gui.MoveWindow(self.hwnd, 120, 80, 480, 320, True)
        #显示窗口
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)

    def wndProc(self, hwnd, msg, wParam, lParam):
        """
        消息处理
        :param hwnd:
        :param msg:
        :param wParam:
        :param lParam:
        :return:
        """
        if msg == win32con.WM_PAINT:
            hdc, ps = win32gui.BeginPaint(hwnd)
            rect = win32gui.GetClientRect(hwnd)
            win32gui.DrawText(hdc, 'GUI Python', len('GUI Python'), rect, win32con.DT_SINGLELINE | win32con.DT_CENTER | win32con.DT_VCENTER)
            win32gui.EndPaint(hwnd, ps)
        if msg == win32con.WM_CREATE:
            print('message: WM_CREATE')
        if msg == win32con.WM_SIZE:
            print('message: WM_SIZE')
        if msg == win32con.WM_PAINT:
            print('message: WM_PAINT')
        if msg == 1280:
            print("message: 1280")
        if msg == win32con.WM_CLOSE:
            print('message: WM_CLOSE')
        if msg == win32con.WM_DESTROY:
            print('message: WM_DESTROY')
            win32gui.PostQuitMessage(0)
        return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

mw = MyWindow()
win32gui.PumpMessages()
