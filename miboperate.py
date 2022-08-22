# -*- coding: utf-8 -*-
import tkinter
from tkinter import filedialog
from tkinter.ttk import Treeview
from tkinter import *
import tkinter as tk
import os
import pickle
import tkinter.messagebox
from ListView import ListView
from operatemtputty import Operatemtputty
from extractlog import ExtractLog
from generateNetconfTcl import generateNetconfTcl
import time


class MibOperate():

    def __init__(self):
        self.init_window = tk.Tk()

    def mib_gui(self):
        self.init_window.title("mib脚本开发系统")
        # self.init_window.state('zoomed') # 打开是不是全屏
        self.init_window.geometry('1068x681+260+100')
        self.init_window["bg"] = "Beige"


        self.button1 = Button(self.init_window, text=" snmp_connect ", background="lightblue", foreground='black', width=15, command=self.snmp_connect)
        self.button1.place(x=100, y=100, anchor='nw', )
        self.button2 = Button(self.init_window, text='连接测试仪', background="lightblue", foreground='black', width=15, command=self.ss)
        self.button2.place(x=100, y=180, anchor='nw')
        self.button3 = Button(self.init_window, text='snmp_get', background="lightblue", foreground='black', width=15, command=self.snmp_get)
        self.button3.place(x=100, y=260, anchor='nw')
        self.button4 = Button(self.init_window, text=' snmp_getnext ', background="lightblue", foreground='black', width=15, command=self.snmp_getnext)
        self.button4.place(x=100, y=340, anchor='nw')
        self.button5 = Button(self.init_window, text=' snmp_getbulk ', background="lightblue", foreground='black', width=15, command=self.snmp_getbulk)
        self.button5.place(x=100, y=420, anchor='nw')
        self.button6 = Button(self.init_window, text=' snmp_set ', background="lightblue", foreground='black', width=15, command=self.snmp_set)
        self.button6.place(x=100, y=500, anchor='nw')
        self.button7 = Button(self.init_window, text=' snmp_getnext ', background="lightblue", foreground='black', width=15, command=self.ss)
        self.button7.place(x=350, y=20, anchor='nw')
        self.button8 = Button(self.init_window, text=' snmp_getbulk ', background="lightblue", foreground='black', width=15, command=self.ss)
        self.button8.place(x=550, y=20, anchor='nw')
        self.button9 = Button(self.init_window, text=' 保存 ', background="lightblue", foreground='black', width=5, command=self.ss)
        self.button9.place(x=700, y=135, anchor='nw')

        # 输出框
        self.logtext = Text(self.init_window, height=4, width=70)
        self.logtext.place(x=250, y=75, anchor='nw')
        self.tcltext = Text(self.init_window, height=25, width=70)
        self.tcltext.place(x=250, y=180, anchor='nw')
        self.showpath()
        self.writetext()

        self.init_window.mainloop()

    def ss(self):
        pass

    def showpath(self):
        if not os.path.exists('./log'):
            os.mkdir('./log')
        if not os.path.exists('./result'):
            os.mkdir('./result')
        path = os.path.abspath(".")
        # path.set(os.path.abspath("."))
        # ss = path.get()
        self.logpath = path + '\\devicelog'
        self.tclpath = path + '\\result'

    def writetext(self):
        self.logtext.delete(0.0, END)
        self.logtext.insert(tk.INSERT, 'Log保存路径：' + self.logpath)
        self.logtext.insert(tk.INSERT, '\n')
        self.logtext.insert(tk.INSERT, 'Tcl保存路径：' + self.tclpath)

    def snmp_connect(self):

        def onSumbitClick():
            ip = str(ipval.get())
            version = str(versionval.get())
            username = str(usernameval.get())
            passworld = str(passworldval.get())
            # print(type)
            popwind.destroy()

        # 定义弹窗
        popwind = tkinter.Toplevel(self.init_window)
        # popwind = tk.Tk()
        popwind.title("设备连接信息")
        popwind.geometry('300x320+386+163')
        popwind["bg"] = "Ivory"

        tkinter.Label(popwind, text='地址:').place(x=50, y=30, anchor='nw')
        tkinter.Label(popwind, text='版本:').place(x=50, y=90, anchor='nw')
        tkinter.Label(popwind, text='用户:').place(x=50, y=150, anchor='nw')
        tkinter.Label(popwind, text='密码:').place(x=50, y=210, anchor='nw')

        # 将输入的注册名赋值给变量
        ipval = tkinter.StringVar()
        versionval = tkinter.StringVar()
        versionval.set('v1')
        usernameval = tkinter.StringVar()
        passworldval = tkinter.StringVar()

        ipentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=ipval)
        ipentry.place(x=100, y=30)
        usernameentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=usernameval)
        usernameentry.place(x=100, y=150)
        versionentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=versionval)
        versionentry.place(x=100, y=90)
        passworldentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=passworldval)
        passworldentry.place(x=100, y=210)
        tkinter.Button(popwind, text='确定', width=10, command=onSumbitClick).place(x=120, y=280, anchor='nw')
        tkinter.Button(popwind, text='取消', width=10, command=popwind.destroy).place(x=210, y=280, anchor='nw')

    def snmp_get(self):
        # 定义弹窗
        popwind = tkinter.Toplevel(self.init_window)
        # popwind = tk.Tk()
        popwind.title("设备连接信息")
        popwind.geometry('300x170+386+163')
        popwind["bg"] = "Ivory"

        tkinter.Label(popwind, text='oid:').place(x=40, y=30, anchor='nw')
        tkinter.Label(popwind, text='check值:').place(x=40, y=90, anchor='nw')


        # 将输入的注册名赋值给变量
        oidval = tkinter.StringVar()
        checkval = tkinter.StringVar()
        checkval.set('v1')


        oidentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=oidval)
        oidentry.place(x=100, y=30)
        checkentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=checkval)
        checkentry.place(x=100, y=90)
        tkinter.Button(popwind, text='确定', width=10, command=self.ss).place(x=120, y=130, anchor='nw')
        tkinter.Button(popwind, text='取消', width=10, command=popwind.destroy).place(x=210, y=130, anchor='nw')

    def snmp_getnext(self):
        # 定义弹窗
        popwind = tkinter.Toplevel(self.init_window)
        # popwind = tk.Tk()
        popwind.title("设备连接信息")
        popwind.geometry('300x170+386+163')
        popwind["bg"] = "Ivory"

        tkinter.Label(popwind, text='oid:').place(x=40, y=30, anchor='nw')
        tkinter.Label(popwind, text='check值:').place(x=40, y=90, anchor='nw')

        # 将输入的注册名赋值给变量
        oidval = tkinter.StringVar()
        checkval = tkinter.StringVar()
        checkval.set('v1')

        oidentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=oidval)
        oidentry.place(x=100, y=30)
        checkentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=checkval)
        checkentry.place(x=100, y=90)
        tkinter.Button(popwind, text='确定', width=10, command=self.ss).place(x=120, y=130, anchor='nw')
        tkinter.Button(popwind, text='取消', width=10, command=popwind.destroy).place(x=210, y=130, anchor='nw')

    def snmp_getbulk(self):
        pass

    def snmp_set(self):
        pass





ss = MibOperate()
ss.mib_gui()