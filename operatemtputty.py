# -*- coding: utf-8 -*-
import re
import sys
# set coinit_flags (there will be a warning message printed in console by pywinauto, you may ignore that)
sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED
from pywinauto import application
import tkinter
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import time
import win32gui
import win32api
import win32con
import os
import shutil

class Operatemtputty():
    # def __init__(self):


    def openmtputty(self,path='./mtputty/'):
        app = application.Application(backend="win32").start("./mtputty/mtputty.exe")
        time.sleep(3)

    def doClick(self,cx, cy, hwnd):
        # hwnd为需要点击的窗口控件句柄，cx、cy为点击位置在该窗口的相对坐标
        long_position = win32api.MAKELONG(cx, cy)  # 模拟鼠标指针 传送到指定坐标
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)  # 模拟鼠标弹起

    def get_child_windows(self,parent):
        '''
        获得parent的所有子窗口句柄
         返回子窗口句柄列表
         '''
        if not parent:
            return
        hwndChildList = []
        win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
        return hwndChildList

    def openconnectto(self):
        handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
        menu = win32gui.GetMenu(handle)  # get menu from handle
        menu1 = win32gui.GetSubMenu(menu, 0)  # get server menu
        cmd_ID = win32gui.GetMenuItemID(menu1, 10)  # get add server bottom
        win32gui.PostMessage(handle, win32con.WM_COMMAND, cmd_ID, 0)  # bottom

    # def connetdevice(self):
        # handle_mtputty = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
        # TToolBar = win32gui.FindWindowEx(handle_mtputty, 0, "TToolBar", "")
        # self.doClick(15,15,TToolBar)

    def clickok(self):
        TfrmPuttyProps = win32gui.FindWindow("TfrmPuttyProps", "Properties")
        okbutton = win32gui.FindWindowEx(TfrmPuttyProps, 0, "TButton", "OK")
        win32api.SendMessage(okbutton, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)  # 模拟鼠标按下
        win32api.SendMessage(okbutton, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)

    def clickbutton(self,handle):
        win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)  # 模拟鼠标按下
        win32api.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)

    def inputtext(self,handle,text):
        win32api.SendMessage(handle, win32con.WM_SETTEXT, 0, text)
        # for char in text:
        #     win32gui.PostMessage(handle, win32con.WM_CHAR, ord(char), 0)
        #     time.sleep(1)

    def connetdevice(self, device):
        self.openconnectto()
        time.sleep(3)
        TfrmConnectTo = win32gui.FindWindow("TfrmConnectTo", "Connect to")
        hwndChildList = self.get_child_windows(TfrmConnectTo)
        serialbutton = hwndChildList[0]
        cancelbutton = hwndChildList[1]
        okbutton = hwndChildList[2]
        sshbutton = hwndChildList[4]
        rloginbutton = hwndChildList[5]
        telnetbutton = hwndChildList[6]
        rawbutton = hwndChildList[7]
        porthandle = hwndChildList[3]
        serverip = hwndChildList[8]

        name = device[1]
        type = device[2]
        port = device[4]
        ip = device[3]
        self.inputtext(serverip,ip)
        # for i in ip:
        #     win32gui.PostMessage(serverip, win32con.WM_CHAR, ord(i), 0)
        #     time.sleep(1)
        if type == 'telnet':
            # win32gui.PostMessage(TfrmConnectTo, win32con.WM_COMMAND, telnetbutton, 0)
            win32api.SendMessage(telnetbutton, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)  # 模拟鼠标按下
            win32api.SendMessage(telnetbutton, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
        elif type == 'ssh':
            win32api.SendMessage(sshbutton, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)  # 模拟鼠标按下
            win32api.SendMessage(sshbutton, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
        self.inputtext(porthandle, port)
        # for j in port:
        #     win32gui.PostMessage(porthandle, win32con.WM_CHAR, ord(j), 0)
        #     time.sleep(1)
        win32api.SendMessage(okbutton, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)  # 模拟鼠标按下
        win32api.SendMessage(okbutton, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
        time.sleep(3)

    def protestmasterconfig(self, tmname):

        handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
        subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
        subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", tmname)
        subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", tmname)
        subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", tmname)
        if subhadle4:
            # 登录
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('1'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('2'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('3'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('4'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('5'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('6'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            # 同步时间
            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('h'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('w'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('k'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('-'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('w'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            # 切到 /opt/TestMaster/logs路径
            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('p'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('T'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('M'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)

            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)

            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('1'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('2'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('3'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('4'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('5'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('6'), 0)

            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            # 删除当前文件夹所有文件
            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('-'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('_'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('.'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('2'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('0'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('2'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('2'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('0'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('*'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('.'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
        else:
            handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
            subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
            subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", tmname.split(':')[0])
            subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", tmname.split(':')[0])
            subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", tmname.split(':')[0] + " - PuTTY")
            # 登录
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('1'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('2'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('3'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('4'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('5'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('6'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            # 同步时间
            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('h'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('w'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('k'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('-'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('w'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            # 切到 /opt/TestMaster/logs路径
            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('p'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('T'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('M'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)

            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)

            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('1'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('2'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('3'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('4'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('5'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('6'), 0)

            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            # 删除当前文件夹所有文件
            time.sleep(1)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('-'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('_'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('.'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('2'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('0'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('2'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('2'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('0'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('*'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('.'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

    def endtestmasterconfig(self, tmname):

        ipaddre = tmname.split(':')[0]
        path = re.sub(re.compile("\\\\"), '/', os.path.abspath("."))
        test = "pscp -pw 123456 root@" + ipaddre + ":/opt/TestMaster/logs/frr_emulator.2022*.log " + path + "/" + "TMlog/"
        os.system(test)
        # print(test)
        #
        # handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
        # subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
        # subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", tmname)
        # subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", tmname)
        # subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", tmname)
        # if subhadle4:
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('v'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('_'), 0)
        #
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('.'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('*'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('.'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('p'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('T'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('M'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
        # else:
        #     handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
        #     subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
        #     subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", tmname.split(':')[0])
        #     subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", tmname.split(':')[0])
        #     subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", tmname.split(':')[0] + " - PuTTY")
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('v'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('_'), 0)
        #
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('.'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('*'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('.'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('p'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('T'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('M'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('/'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        #     win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

    def saveconfig(self,devicename):
        # 遍历不同句柄时从这里使用for循环进行遍历 for dutx in list:

        handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
        subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
        subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename)
        subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename)
        subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename)  # ---找到mtputty中对应子窗口
        if subhadle4:
            # 收集设备初始配置
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('v'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('i'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('.'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            time.sleep(3)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('y'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            time.sleep(3)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('y'), 0)  # 当文件已存在的情况下，需要重复确认
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            time.sleep(3)
        else:
            handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
            subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
            subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename.split(':')[0])
            subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename.split(':')[0])
            subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename.split(':')[0] + " - PuTTY")
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('v'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('i'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('.'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            time.sleep(3)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('y'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            time.sleep(3)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('y'), 0)  # 当文件已存在的情况下，需要重复确认
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            time.sleep(3)

    def precomconfig(self, devicename):
        handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
        subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
        subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename)
        subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename)
        subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename)
        if subhadle4:
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('b'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            ########start#######
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
        else:
            handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
            subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
            subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename.split(':')[0])
            subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename.split(':')[0])
            subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename.split(':')[0] + " - PuTTY")
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('b'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            # win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            ########start#######
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

    def prenetcofconfig(self, devicename):
        handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
        subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
        subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename)
        subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename)
        subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename)
        if subhadle4:
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('b'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            # undo debugging all
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('b'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('i'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            # t m t d
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
        else:
            handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
            subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
            subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename.split(':')[0])
            subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename.split(':')[0])
            subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename.split(':')[0] + " - PuTTY")
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('b'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

            # undo debugging all
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('b'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('i'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            # t m t d
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

        # netconf log source all
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('y'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('v'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('b'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        # protocol-operation all  \row-operation  \ verbose
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('p'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('-'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('p'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('i'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('w'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('-'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('p'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('i'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('c'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('v'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('b'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

        ########start#######
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('a'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

    def startrecording(self, top, devicename, config):

        scale = 100
        # 得传个参数过来，判断一下是netconf脚本还是功能脚本，需要使用不同的预配置函数
        top1 = tkinter.Toplevel()
        top1.title("录制准备进度展示")
        top1.geometry('800x100')
        pb = Progressbar(top1, length=700, mode="determinate", orient=HORIZONTAL)
        pb.pack(padx=10, pady=20)
        pb["maximum"] = 100
        pb["value"] = 0

        print("\n" * 2)
        print("执行开始".center(scale + 28, '_'))
        start = time.perf_counter()
        if config == 1:
            for i in range(scale + 1):

                if i == 50:
                    self.saveconfig(devicename)
                    self.precomconfig(devicename)

                pb["value"] = i
                top.update()
                a = '*' * i
                b = '.' * (scale - i)
                c = (i / scale) * 100
                t = time.perf_counter() - start
                print("\r任务进度:{:>3.0f}% [{}->{}]消耗时间:{:.2f}s".format(c, a, b, t), end="")
                time.sleep(0.03)
        if config == 2:
            for i in range(scale + 1):

                if i == 50:
                    self.saveconfig(devicename)
                    self.prenetcofconfig(devicename)

                pb["value"] = i
                top.update()
                a = '*' * i
                b = '.' * (scale - i)
                c = (i / scale) * 100
                t = time.perf_counter() - start
                print("\r任务进度:{:>3.0f}% [{}->{}]消耗时间:{:.2f}s".format(c, a, b, t), end="")
                time.sleep(0.03)
        print("\n" + "执行结束".center(scale + 28, '_'))
        top1.destroy()

    def endconfig(self, devicename):
        # 遍历不同句柄时从这里使用for循环进行遍历 for dutx in list:

        handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
        subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
        subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename)
        subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename)
        subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename)  # ---找到mtputty中对应子窗口
        if subhadle4:
            # 收集设备初始配置
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('i'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('b'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            ########end#######
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
        else:
            handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
            subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
            subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename.split(':')[0])
            subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename.split(':')[0])
            subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename.split(':')[0] + " - PuTTY")
            # 收集设备初始配置
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('i'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('s'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('l'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('g'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('b'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('f'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('r'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('m'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('u'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('o'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('t'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord(' '), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车
            ########end#######
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('e'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('n'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('d'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_CHAR, ord('#'), 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(subhadle4, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  # 发送回车

    def stoprecording(self, top, devicename):
        scale = 100
        top1 = tkinter.Toplevel()
        top1.title("停止准备进度展示")
        top1.geometry('800x100')
        pb = Progressbar(top1, length=700, mode="determinate", orient=HORIZONTAL)
        pb.pack(padx=10, pady=20)
        pb["maximum"] = 100
        pb["value"] = 0

        print("\n" * 2)
        print("执行开始".center(scale + 28, '_'))
        start = time.perf_counter()
        for i in range(scale + 1):
            if i == 50:
                self.endconfig(devicename)

            pb["value"] = i
            top.update()
            a = '*' * i
            b = '.' * (scale - i)
            c = (i / scale) * 100
            t = time.perf_counter() - start
            print("\r任务进度:{:>3.0f}% [{}->{}]消耗时间:{:.2f}s".format(c, a, b, t), end="")
            time.sleep(0.03)
        print("\n" + "执行结束".center(scale + 28, '_'))
        top1.destroy()

    def copyfile(self,sourcepath,despath,filenamelist):
        # self.removefile(despath)
        for file in filenamelist:
            full_file_name = os.path.join(sourcepath,file)
            try:
                if os.path.isfile(full_file_name):
                    shutil.copy(full_file_name,despath)
            except OSError:
                self.popwarningwin('log保存路径不能为当前路径log文件夹')
                # print('路径一致')
            except IOError:
                self.popwarningwin('请检查文件夹读写权限')

    def removefile(self,path):
        shutil.rmtree(path)
        os.mkdir(path)

    def extraputtyset(self, devicename):
        handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
        subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
        subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename)
        subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename)
        subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename)
        try:
            if subhadle4:  # ---找到mtputty中对应子窗口
                menu = win32gui.GetMenu(subhadle4)  # get menu from handle
                menu1 = win32gui.GetSubMenu(menu, 0)  # get server menu
                cmd_ID = win32gui.GetMenuItemID(menu1, 5)  # get add server bottom
                win32gui.PostMessage(subhadle4, win32con.WM_COMMAND, cmd_ID, 0)  # bottom
            else:
                handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
                subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
                subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename.split(':')[0])
                subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename.split(':')[0])
                subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename.split(':')[0] + " - PuTTY")
                menu = win32gui.GetMenu(subhadle4)  # get menu from handle
                menu1 = win32gui.GetSubMenu(menu, 0)  # get server menu
                cmd_ID = win32gui.GetMenuItemID(menu1, 5)  # get add server bottom
                win32gui.PostMessage(subhadle4, win32con.WM_COMMAND, cmd_ID, 0)  # bottom
        except:
            self.popwarningwin('获取句柄失败，重试一次')
            try:
                handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
                subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
                subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename)
                subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename)
                subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename)
                if subhadle4:  # ---找到mtputty中对应子窗口
                    menu = win32gui.GetMenu(subhadle4)  # get menu from handle
                    menu1 = win32gui.GetSubMenu(menu, 0)  # get server menu
                    cmd_ID = win32gui.GetMenuItemID(menu1, 5)  # get add server bottom
                    win32gui.PostMessage(subhadle4, win32con.WM_COMMAND, cmd_ID, 0)  # bottom
                else:
                    handle = win32gui.FindWindow("TTYPLUSMAIN", "MTPuTTY (Multi-Tabbed PuTTY)")
                    subhadle1 = win32gui.FindWindowEx(handle, 0, "TaqDockingSite", "")
                    subhadle2 = win32gui.FindWindowEx(subhadle1, 0, "TaqDockingControl", devicename.split(':')[0])
                    subhadle3 = win32gui.FindWindowEx(subhadle2, 0, "TfrmPutty", devicename.split(':')[0])
                    subhadle4 = win32gui.FindWindowEx(subhadle3, 0, "PuTTY", devicename.split(':')[0] + " - PuTTY")
                    menu = win32gui.GetMenu(subhadle4)  # get menu from handle
                    menu1 = win32gui.GetSubMenu(menu, 0)  # get server menu
                    cmd_ID = win32gui.GetMenuItemID(menu1, 5)  # get add server bottom
                    win32gui.PostMessage(subhadle4, win32con.WM_COMMAND, cmd_ID, 0)  # bottom
            except:
                self.popwarningwin('获取句柄失败！')

        # def get_menu_item_txt(menu, idx):
        #     import win32gui_struct
        #     mii, extra = win32gui_struct.EmptyMENUITEMINFO()  # 新建一个win32gui的空的结构体mii
        #     win32gui.GetMenuItemInfo(menu, idx, True, mii)  # 将子菜单内容获取到mii
        #     ftype, fstate, wid, hsubmenu, hbmpchecked, hbmpunchecked, dwitemdata, text, hbmpitem = win32gui_struct.UnpackMENUITEMINFO(mii)  # 解包mii
        #     return text
        # #
        # print(get_menu_item_txt(menu1, 5))

    def clicklogging(self):
        handle = win32gui.FindWindow("PuTTYConfigBox", "PuTTY Reconfiguration (Save mode : File)")
        subhadle1 = win32gui.FindWindowEx(handle, 0, "SysTreeView32", "")
        self.doClick(65,26,subhadle1)

    def clickwindow(self):
        handle = win32gui.FindWindow("PuTTYConfigBox", "PuTTY Reconfiguration (Save mode : File)")
        subhadle1 = win32gui.FindWindowEx(handle, 0, "SysTreeView32", "")
        self.doClick(45,138,subhadle1)

    def setlogging(self,logpath):
        # self.extraputtyset()
        time.sleep(3)
        self.clicklogging()
        time.sleep(3)
        handle = win32gui.FindWindow("PuTTYConfigBox", "PuTTY Reconfiguration (Save mode : File)")
        handlelist = self.get_child_windows(handle)
        logsethandle = handlelist[16]
        allprintenablehandle = handlelist[8]
        timesethandle = handlelist[14]
        overwritehandle = handlelist[20]
        applyhandle = handlelist[0]
        puttyloghandle = handlelist[12]
        self.clickbutton(allprintenablehandle)
        time.sleep(1)
        win32api.PostMessage(puttyloghandle, win32con.CB_SETCURSEL, 2, 0)
        # if win32api.SendMessage(puttyloghandle, win32con.CB_SETCURSEL, 2, 0) == 2:
        #     win32api.PostMessage(puttyloghandle, win32con.CB_SETCURSEL, 2, 0)
        #     win32api.SendMessage(handle, win32con.WM_COMMAND, 0x90000, puttyloghandle)
        #     win32api.SendMessage(handle, win32con.WM_COMMAND, 0x10000, puttyloghandle)
        time.sleep(1)
        self.clickbutton(puttyloghandle)
        self.inputtext(timesethandle, '[%Y/%m/%d %H:%M:%S]')
        self.inputtext(logsethandle, logpath)
        self.clickbutton(overwritehandle)
        time.sleep(2)
        self.setloglength()
        time.sleep(2)
        self.clickbutton(applyhandle)
        time.sleep(2)

    def setputtylog(self):
        time.sleep(3)
        self.clicklogging()
        time.sleep(3)
        handle = win32gui.FindWindow("PuTTYConfigBox", "PuTTY Reconfiguration (Save mode : File)")
        handlelist = self.get_child_windows(handle)
        puttyloghandle = handlelist[12]
        applyhandle = handlelist[0]
        time.sleep(1)
        if win32api.SendMessage(puttyloghandle, win32con.CB_SETCURSEL, 2, 0) == 2:
            win32api.SendMessage(handle, win32con.WM_COMMAND, 0x90000, puttyloghandle)
            win32api.SendMessage(handle, win32con.WM_COMMAND, 0x10000, puttyloghandle)
        time.sleep(3)
        self.clickbutton(applyhandle)

    def clickbehaviour(self):
        self.extraputtyset()
        handle = win32gui.FindWindow("PuTTYConfigBox", "PuTTY Reconfiguration (Save mode : File)")
        subhadle1 = win32gui.FindWindowEx(handle, 0, "SysTreeView32", "")
        self.doClick(78,170,subhadle1)

    def setwindowtitle(self, title):
        self.clickbehaviour()
        handle = win32gui.FindWindow("PuTTYConfigBox", "PuTTY Reconfiguration (Save mode : File)")
        handlelist = self.get_child_windows(handle)
        applyhandle = handlelist[0]
        windowtitlehandle = handlelist[6]
        self.inputtext(windowtitlehandle, title)
        self.clickbutton(applyhandle)

    def popwarningwin(self,warningtext):
        root = tkinter.Tk()
        root.withdraw()
        tkinter.messagebox.showinfo(title='Warning', message=warningtext)

    def remove_lines(self,logname):
        f = open('./log/{logname}'.format(logname=logname), 'rb')
        f_w = open('./log/log_bak.log', 'w')
        while True:
            line = f.readline()
            if not line:
                break
            else:
                try:
                    line.decode('utf-8')
                    f_w.write(str(line, 'utf-8'))
                # 为了暴露出错误，最好此处不print测试log.log
                except UnicodeDecodeError:
                    self.popwarningwin('请修改文件编码格式')
                    print(str(line))
                continue
        f.close()
        f_w.close()
        os.remove('./log/{logname}'.format(logname=logname))
        # os.chdir(r'.\log')
        os.rename('./log/log_bak.log', './log/{logname}'.format(logname=logname))

    def del_notutf_8(self, path):
        for root, dirs, files in os.walk(path, True):
            for name in files:
                pathname = os.path.splitext(os.path.join(root, name))
                self.remove_lines(name)

    def del_files(self,dir, topdown=True):
        for root, dirs, files in os.walk(dir, topdown):
            for name in files:
                pathname = os.path.splitext(os.path.join(root, name))
                if (pathname[1] == ".log"):
                    os.remove(os.path.join(root, name))
                    # print(os.path.join(root, name))
                    # dir = os.getcwd()
                    # print(dir)
                    # self.del_files(dir)  # will delete the self .py file after run !!!-_-
                    # os.removedirs(dir)  # delete the empty directory recursively

    def setloglength(self):
        time.sleep(3)
        self.clickwindow()
        time.sleep(3)
        handle = win32gui.FindWindow("PuTTYConfigBox", "PuTTY Reconfiguration (Save mode : File)")
        handlelist = self.get_child_windows(handle)
        lengthhandle = handlelist[6]
        rowhandle = handlelist[8]
        self.inputtext(lengthhandle, '500')
        self.inputtext(rowhandle, '47')


# f = open('./log/isis.topo', 'rb')
# f.close()
# ss=Operatemtputty()
# ss.del_files("./log")


#
# path = re.sub(re.compile("\\\\"), '/', os.path.abspath("."))
# test = "pscp -pw 123456 h3c@" + "10.99.72.86" + ":/opt/TestMaster/logs/frr_emulator.20220524-142537.log " + path + "/" + "TMlog/"
# print(test)
# os.system("pscp -pw 123456 h3c@10.99.72.86:/opt/TestMaster/logs/frr_emulator.20220524-142537.log D:/test/")
