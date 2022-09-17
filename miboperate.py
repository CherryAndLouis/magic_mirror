# -*- coding: utf-8 -*-
import tkinter
from tkinter import filedialog
from tkinter.ttk import Treeview
from tkinter import *
import tkinter as tk
import os
# import pickle
from publicmeth import PublicMeth
import tkinter.messagebox
# from ListView import ListView
from operatemtputty import Operatemtputty
# from extractlog import ExtractLog
# from generateNetconfTcl import generateNetconfTcl
# import time
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902


class MibOperate:

    def __init__(self, filepath, dutname):
        # self.init_window = init_window_name
        self.publicmeth = PublicMeth()
        self.operator = Operatemtputty()
        self.connect_dir = {}
        self.filepath = filepath
        self.dutname = dutname
        self.after_data = []
        self.before_data = []


    def mib_gui(self):
        self.init_window = tk.Tk()

        self.init_window.title("mib脚本开发系统")
        # self.init_window.state('zoomed') # 打开是不是全屏
        self.init_window.geometry('1068x681+260+100')
        self.init_window["bg"] = "Beige"
        # if getattr(sys, 'frozen', False):
        #     application_path = os.path.dirname(sys.executable)
        #     os.chdir(application_path)
        # elif __file__:
        #     application_path = os.path.dirname(__file__)
        #     os.chdir(application_path)
        self.image_file_mib = tk.PhotoImage(file='logo_mib.png')  # 创建图片对象
        self.imgLabel_mib = Label(self.init_window, image=self.image_file_mib)  # 把图片整合到标签类中
        self.imgLabel_mib.place(x=70, y=30, anchor='nw', )

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
        # self.button7 = Button(self.init_window, text=' snmp_getnext ', background="lightblue", foreground='black', width=15, command=self.ss)
        # self.button7.place(x=350, y=20, anchor='nw')
        # self.button8 = Button(self.init_window, text=' snmp_getbulk ', background="lightblue", foreground='black', width=15, command=self.ss)
        # self.button8.place(x=550, y=20, anchor='nw')
        self.button9 = Button(self.init_window, text=' 保存 ', background="lightblue", foreground='black', width=5, command=self.save_file)
        self.button9.place(x=800, y=55, anchor='nw')
        self.button10 = Button(self.init_window, text='结束录制', background="lightblue", foreground='black', width=10, command=self.end_test)
        self.button10.place(x=700, y=55, anchor='nw')

        # 输出框
        # self.logtext = Text(self.init_window, height=4, width=70)
        # self.logtext.place(x=250, y=75, anchor='nw')
        self.tcltext = Text(self.init_window, height=34, width=85)
        self.tcltext.place(x=250, y=100, anchor='nw')
        # self.showpath()
        # self.writetext()

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

    def writetext(self, text):
        self.tcltext.insert(END, text)
        self.tcltext.insert(END, '\n')

    def snmp_connect(self):

        def onSumbitClick():

            self.connect_dir = {}
            ip = str(ipval.get())
            version = str(versionddl.get())
            username = str(usernameval.get())
            passworld = str(passworldval.get())
            # print(type)
            if ip:
                self.connect_dir['ip'] = ip
            else:
                self.popwarningwin('输入ip地址')
            if version:
                self.connect_dir['version'] = version
            else:
                self.popwarningwin('请输入snmp版本号')
            if username:
                self.connect_dir['username'] = username
            if passworld:
                self.connect_dir['passworld'] = passworld
            devicename = ip + ':23'
            self.operator.premibconfig(devicename, version)
            popwind.destroy()
            text = self.create_connect(self.connect_dir)
            self.writetext(text)
            self.popwarningwin('mib相关配置成功！')
            self.before_data = self.publicmeth.getconfig(self.filepath)


        # 定义弹窗
        popwind = tkinter.Toplevel(self.init_window)
        # popwind = tk.Tk()
        popwind.title("MIB 连接")
        popwind.geometry('300x320+386+163')
        popwind["bg"] = "Ivory"

        tkinter.Label(popwind, text='地址:').place(x=50, y=30, anchor='nw')
        tkinter.Label(popwind, text='版本:').place(x=50, y=90, anchor='nw')
        tkinter.Label(popwind, text='用户:').place(x=50, y=150, anchor='nw')
        tkinter.Label(popwind, text='密码:').place(x=50, y=210, anchor='nw')

        # 将输入的注册名赋值给变量
        ipval = tkinter.StringVar()
        # ipval.set('88.88.88.88')
        # versionval = tkinter.StringVar()
        # versionval.set('v2')
        usernameval = tkinter.StringVar()
        passworldval = tkinter.StringVar()

        ipentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=ipval)
        ipentry.place(x=100, y=30)
        # ipentry.insert(0,'192.168.56.88')
        usernameentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=usernameval)
        usernameentry.place(x=100, y=150)
        versionddl = tkinter.ttk.Combobox(popwind, state='readonly', width=17)
        versionddl['value'] = ("v1", "v2", "v3")
        versionddl.current(0)
        versionddl.pack(side=tkinter.RIGHT, padx=1, pady=1)
        versionddl.place(x=100, y=90)
        # versionentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=versionval)
        # versionentry.place(x=100, y=90)
        passworldentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=passworldval)
        passworldentry.place(x=100, y=210)
        tkinter.Button(popwind, text='确定', width=10, command=onSumbitClick).place(x=120, y=280, anchor='nw')
        tkinter.Button(popwind, text='取消', width=10, command=popwind.destroy).place(x=210, y=280, anchor='nw')

    def snmp_get(self):

        def clearnresult():
            resulttext.delete(0.0, END)

        def writeresult(text):
            resulttext.insert(END, text)
            resulttext.insert(END, '\n')

        def onSumbitClick():
            temp_config = 1
            self.getnext_dir = {}
            oid = str(oidval.get())
            instance = str(instanceval.get())
            syntax = str(Syntaxddl.get())
            type = str(typeddl.get())
            key = str(keyval.get())
            check = str(checkval.get())
            if type == '全局':
                if instance != '0':
                    self.popwarningwin('全局类型oid实例必须为0，请确认修改！')
                    temp_config = 0
            else:
                if instance == '0' or instance == '':
                    self.popwarningwin('局部类型oid实例不能为0和空，请确认修改！')
                    temp_config = 0

            if temp_config == 1:
                if oid:
                    self.getnext_dir['oid'] = oid
                    if instance:
                        self.getnext_dir['instance'] = instance
                        if syntax:
                            self.getnext_dir['syntax'] = syntax
                            if check:
                                self.getnext_dir['check'] = check
                                if key:
                                    self.getnext_dir['key'] = key
                                    self.getnext_dir['type'] = type
                                    get_oid = oid + '.' + instance
                                    ip = self.connect_dir.get('ip')
                                    version = str(self.connect_dir.get('version'))
                                    if version == 'v1':
                                        errorStatus, varBinds, errorIndication = self.snmp_operate_get(0, ip, get_oid)
                                    elif version == 'v2':
                                        errorStatus, varBinds, errorIndication = self.snmp_operate_get(1, ip, get_oid)
                                    # oid_result = varBinds[0][1]
                                    if errorIndication:
                                        writeresult('获取失败，错误信息如下：')
                                        writeresult(errorIndication)
                                        writeresult('错误码如下：')
                                        writeresult(errorStatus)
                                        writeresult('')
                                    else:
                                        if errorStatus == 0:
                                            self.after_data = self.publicmeth.getconfig(self.filepath)
                                            compare_data = self.publicmeth.compare_list(self.before_data, self.after_data)
                                            if compare_data == 0:
                                                config = ''
                                            else:
                                                config = self.publicmeth.return_config(compare_data)
                                                self.before_data = []
                                                self.before_data = self.after_data
                                                self.after_data = []
                                            writeresult('获取成功，结果如下：')
                                            for varBind in varBinds:
                                                writeresult(varBind)
                                            writeresult('')
                                            get_text = self.create_get(self.getnext_dir, config)
                                            self.writetext(get_text)
                                        else:
                                            writeresult('获取失败，错误码如下：')
                                            writeresult(errorStatus)
                                            writeresult('')
                                else:
                                    self.popwarningwin('请输入命令行返回内容获取值的关键字')
                            else:
                                self.popwarningwin('请输入check值')
                        else:
                            self.popwarningwin('请输入oid数据类型')
                    else:
                        self.popwarningwin('请输入实例')
                else:
                    self.popwarningwin('请输入oid')
            else:
                pass
            # popwind.destroy()
            # print(oid_result)
            # print(errorStatus)
            # get_text = self.create_get(self.getnext_dir)
            # self.writetext(get_text)

        # 定义弹窗
        popwind = tkinter.Toplevel(self.init_window)
        # popwind = tk.Tk()
        popwind.title("MIB GET操作")
        popwind.geometry('500x600+386+163')
        popwind["bg"] = "Ivory"

        tkinter.Label(popwind, text='oid:').place(x=40, y=30, anchor='nw')
        tkinter.Label(popwind, text='实例:').place(x=365, y=30, anchor='nw')
        tkinter.Label(popwind, text='类型:').place(x=245, y=30, anchor='nw')
        tkinter.Label(popwind, text='数据类型:').place(x=40, y=90, anchor='nw')
        tkinter.Label(popwind, text='结果对应命令行:').place(x=40, y=150, anchor='nw')
        tkinter.Label(popwind, text='关键字:').place(x=290, y=150, anchor='nw')
        tkinter.Label(popwind, text='获取结果').place(x=220, y=270, anchor='nw')

        # 将输入的注册名赋值给变量
        oidval = tkinter.StringVar()
        # oidval.set('1.3.6.1.2.1.31.1.1.1.18')
        instanceval = tkinter.StringVar()
        # instanceval.set('1029')
        # Syntaxval = tkinter.StringVar()
        # Syntaxval.set('Octets')
        checkval = tkinter.StringVar()
        keyval = tkinter.StringVar()
        # checkval.set('dis thi ')
        # checkval.set('v1')

        oidentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=oidval)
        oidentry.place(x=85, y=30)
        instanceentry = tkinter.Entry(popwind, highlightbackground='white', width=10, textvariable=instanceval)
        instanceentry.place(x=410, y=30)
        typeddl = tkinter.ttk.Combobox(popwind, state='readonly', width=5)
        typeddl['value'] = ("全局", "局部")
        typeddl.current(0)
        typeddl.pack(side=tkinter.RIGHT, padx=1, pady=1)
        typeddl.place(x=290, y=30)
        Syntaxddl = tkinter.ttk.Combobox(popwind, state='readonly', width=14)
        Syntaxddl['value'] = ("Octets", "INTEGER", "Integer32","OBJECT IDENTIFIER","NULL","IpAddress","Counter32","Gauge32","Unsigned32","TimeTicks","Opaque","Counter64","Bits")
        Syntaxddl.current(0)
        Syntaxddl.pack(side=tkinter.RIGHT, padx=1, pady=1)
        Syntaxddl.place(x=100, y=90)
        # Syntaxentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=Syntaxval)
        # Syntaxentry.place(x=100, y=90)
        checkentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=checkval)
        checkentry.place(x=135, y=150)
        keyentry = tkinter.Entry(popwind, highlightbackground='white', width=15, textvariable=keyval)
        keyentry.place(x=345, y=150)
        resulttext = Text(popwind, height=20, width=60)
        resulttext.place(x=40, y=300, anchor='nw')
        tkinter.Button(popwind, text='GET', width=10, command=onSumbitClick).place(x=320, y=190, anchor='nw')
        tkinter.Button(popwind, text='取消', width=10, command=popwind.destroy).place(x=410, y=190, anchor='nw')

    def snmp_getnext(self):
        def clearnresult():
            resulttext.delete(0.0, END)

        def writeresult(text):
            resulttext.insert(END, text)
            resulttext.insert(END, '\n')

        def onSumbitClick():
            temp_config = 1
            self.get_dir = {}
            oid = str(oidval.get())
            instance = str(instanceval.get())
            syntax = str(Syntaxddl.get())
            type = str(typeddl.get())
            key = str(keyval.get())
            check = str(checkval.get())
            if type == '全局':
                if instance != '0':
                    self.popwarningwin('全局类型oid实例必须为0，请确认修改！')
                    temp_config = 0
            else:
                if instance == '0' or instance == '':
                    self.popwarningwin('局部类型oid实例不能为0和空，请确认修改！')
                    temp_config = 0

            if temp_config == 1:
                if oid:
                    self.get_dir['oid'] = oid
                    if instance:
                        self.get_dir['instance'] = instance
                        if syntax:
                            self.get_dir['syntax'] = syntax
                            if check:
                                self.get_dir['check'] = check
                                if key:
                                    self.get_dir['key'] = key
                                    self.get_dir['type'] = type
                                    get_oid = oid + '.' + instance
                                    ip = self.connect_dir.get('ip')
                                    version = str(self.connect_dir.get('version'))
                                    if version == 'v1':
                                        errorStatus, varBinds, errorIndication = self.snmp_operate_getnext(0, ip, get_oid)
                                    elif version == 'v2':
                                        errorStatus, varBinds, errorIndication = self.snmp_operate_getnext(1, ip, get_oid)
                                    # oid_result = varBinds[0][1]
                                    if errorIndication:
                                        writeresult('获取失败，错误信息如下：')
                                        writeresult(errorIndication)
                                        writeresult('错误码如下：')
                                        writeresult(errorStatus)
                                        writeresult('')
                                    else:
                                        if errorStatus == 0:
                                            self.after_data = self.publicmeth.getconfig(self.filepath)
                                            compare_data = self.publicmeth.compare_list(self.before_data, self.after_data)
                                            if compare_data == 0:
                                                config = ''
                                            else:
                                                config = self.publicmeth.return_config(compare_data)
                                                self.before_data = []
                                                self.before_data = self.after_data
                                                self.after_data = []
                                            writeresult('获取成功，结果如下：')
                                            for varBind in varBinds:
                                                writeresult(varBind)
                                            writeresult('')
                                            get_text = self.create_getnext(self.get_dir, config)
                                            self.writetext(get_text)
                                        else:
                                            writeresult('获取失败，错误码如下：')
                                            writeresult(errorStatus)
                                            writeresult('')
                                else:
                                    self.popwarningwin('请输入命令行返回内容获取值的关键字')
                            else:
                                self.popwarningwin('请输入check值')
                        else:
                            self.popwarningwin('请输入oid数据类型')
                    else:
                        self.popwarningwin('请输入实例')
                else:
                    self.popwarningwin('请输入oid')
            else:
                pass
            # print(oid_result)
            # print(errorStatus)
            # get_text = self.create_get(self.getnext_dir)
            # self.writetext(get_text)

        # 定义弹窗
        popwind = tkinter.Toplevel(self.init_window)
        # popwind = tk.Tk()
        popwind.title("MIB GET_NEXT操作")
        popwind.geometry('500x600+386+163')
        popwind["bg"] = "Ivory"

        tkinter.Label(popwind, text='oid:').place(x=40, y=30, anchor='nw')
        tkinter.Label(popwind, text='实例:').place(x=365, y=30, anchor='nw')
        tkinter.Label(popwind, text='类型:').place(x=245, y=30, anchor='nw')
        tkinter.Label(popwind, text='数据类型:').place(x=40, y=90, anchor='nw')
        tkinter.Label(popwind, text='结果对应命令行:').place(x=40, y=150, anchor='nw')
        tkinter.Label(popwind, text='关键字:').place(x=290, y=150, anchor='nw')
        tkinter.Label(popwind, text='获取结果').place(x=220, y=270, anchor='nw')

        # 将输入的注册名赋值给变量
        oidval = tkinter.StringVar()
        # oidval.set('1.3.6.1.2.1.31.1.1.1.18')
        instanceval = tkinter.StringVar()
        # instanceval.set('1029')
        # Syntaxval = tkinter.StringVar()
        # Syntaxval.set('Octets')
        checkval = tkinter.StringVar()
        keyval = tkinter.StringVar()
        # checkval.set('dis thi ')
        # checkval.set('v1')

        oidentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=oidval)
        oidentry.place(x=85, y=30)
        instanceentry = tkinter.Entry(popwind, highlightbackground='white', width=10, textvariable=instanceval)
        instanceentry.place(x=410, y=30)
        typeddl = tkinter.ttk.Combobox(popwind, state='readonly', width=5)
        typeddl['value'] = ("全局", "局部")
        typeddl.current(0)
        typeddl.pack(side=tkinter.RIGHT, padx=1, pady=1)
        typeddl.place(x=290, y=30)
        Syntaxddl = tkinter.ttk.Combobox(popwind, state='readonly', width=14)
        Syntaxddl['value'] = ("Octets", "INTEGER", "Integer32","OBJECT IDENTIFIER","NULL","IpAddress","Counter32","Gauge32","Unsigned32","TimeTicks","Opaque","Counter64","Bits")
        Syntaxddl.current(0)
        Syntaxddl.pack(side=tkinter.RIGHT, padx=1, pady=1)
        Syntaxddl.place(x=100, y=90)
        # Syntaxentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=Syntaxval)
        # Syntaxentry.place(x=100, y=90)
        checkentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=checkval)
        checkentry.place(x=135, y=150)
        keyentry = tkinter.Entry(popwind, highlightbackground='white', width=15, textvariable=keyval)
        keyentry.place(x=345, y=150)
        resulttext = Text(popwind, height=20, width=60)
        resulttext.place(x=40, y=300, anchor='nw')
        tkinter.Button(popwind, text='GET', width=10, command=onSumbitClick).place(x=320, y=190, anchor='nw')
        tkinter.Button(popwind, text='取消', width=10, command=popwind.destroy).place(x=410, y=190, anchor='nw')
        
    def snmp_getbulk(self):
        def clearnresult():
            resulttext.delete(0.0, END)

        def writeresult(text):
            resulttext.insert(END, text)
            resulttext.insert(END, '\n')

        def onSumbitClick():
            self.getbulk_dir = {}
            nonrepeaters = str(nonrepeatersval.get())
            maxrepetitions = str(maxrepetitionsval.get())
            temp_config = 1
            self.getbulk_dir = {}
            oid = str(oidval.get())
            instance = str(instanceval.get())
            syntax = str(Syntaxddl.get())
            type = str(typeddl.get())
            key = str(keyval.get())
            check = str(checkval.get())
            if type == '全局':
                if instance != '0':
                    self.popwarningwin('全局类型oid实例必须为0，请确认修改！')
                    temp_config = 0
            else:
                if instance == '0' or instance == '':
                    self.popwarningwin('局部类型oid实例不能为0和空，请确认修改！')
                    temp_config = 0

            if temp_config == 1:
                if oid:
                    self.getbulk_dir['oid'] = oid
                    if instance:
                        self.getbulk_dir['instance'] = instance
                        if syntax:
                            self.getbulk_dir['syntax'] = syntax
                            if check:
                                self.getbulk_dir['check'] = check
                                if key:
                                    self.getbulk_dir['key'] = key
                                    self.getbulk_dir['type'] = type
                                    get_oid = oid + '.' + instance
                                    ip = self.connect_dir.get('ip')
                                    version = str(self.connect_dir.get('version'))
                                    if version == 'v1':
                                        errorStatus, varBinds, errorIndication = self.snmp_operate_getbulk(0, ip, get_oid, nonrepeaters, maxrepetitions)
                                    elif version == 'v2':
                                        errorStatus, varBinds, errorIndication = self.snmp_operate_getbulk(1, ip, get_oid, nonrepeaters, maxrepetitions)
                                    # oid_result = varBinds[0][1]
                                    if errorIndication:
                                        writeresult('获取失败，错误信息如下：')
                                        writeresult(errorIndication)
                                        writeresult('错误码如下：')
                                        writeresult(errorStatus)
                                        writeresult('')
                                    else:
                                        if errorStatus == 0:
                                            self.after_data = self.publicmeth.getconfig(self.filepath)
                                            compare_data = self.publicmeth.compare_list(self.before_data, self.after_data)
                                            if compare_data == 0:
                                                config = ''
                                            else:
                                                config = self.publicmeth.return_config(compare_data)
                                                self.before_data = []
                                                self.before_data = self.after_data
                                                self.after_data = []
                                            writeresult('获取成功，结果如下：')
                                            for varBind in varBinds:
                                                for name, val in varBind:
                                                    text = 'OID:%s = %s' % (name, val)
                                                    writeresult(text)
                                            writeresult('')
                                            get_text = self.create_getnext(self.getbulk_dir, config)
                                            self.writetext(get_text)
                                        else:
                                            writeresult('获取失败，错误码如下：')
                                            writeresult(errorStatus)
                                            writeresult('')
                                else:
                                    self.popwarningwin('请输入命令行返回内容获取值的关键字')
                            else:
                                self.popwarningwin('请输入check值')
                        else:
                            self.popwarningwin('请输入oid数据类型')
                    else:
                        self.popwarningwin('请输入实例')
                else:
                    self.popwarningwin('请输入oid')
            else:
                pass
            
            # print(oid_result)
            # print(errorStatus)
            # get_text = self.create_get(self.getbulk_dir)
            # self.writetext(get_text)

        # 定义弹窗
        popwind = tkinter.Toplevel(self.init_window)
        # popwind = tk.Tk()
        popwind.title("MIB GET_BULK操作")
        popwind.geometry('500x600+386+163')
        popwind["bg"] = "Ivory"

        tkinter.Label(popwind, text='oid:').place(x=40, y=30, anchor='nw')
        tkinter.Label(popwind, text='实例:').place(x=365, y=30, anchor='nw')
        tkinter.Label(popwind, text='类型:').place(x=245, y=30, anchor='nw')
        tkinter.Label(popwind, text='数据类型:').place(x=40, y=90, anchor='nw')
        tkinter.Label(popwind, text='重复:').place(x=240, y=90, anchor='nw')
        tkinter.Label(popwind, text='深度:').place(x=340, y=90, anchor='nw')
        tkinter.Label(popwind, text='结果对应命令行:').place(x=40, y=150, anchor='nw')
        tkinter.Label(popwind, text='关键字:').place(x=290, y=150, anchor='nw')
        tkinter.Label(popwind, text='获取结果').place(x=220, y=270, anchor='nw')

        # 将输入的注册名赋值给变量
        oidval = tkinter.StringVar()
        # oidval.set('1.3.6.1.2.1.31.1.1.1.18')
        instanceval = tkinter.StringVar()
        # instanceval.set('1029')
        # Syntaxval = tkinter.StringVar()
        # Syntaxval.set('Octets')
        checkval = tkinter.StringVar()
        keyval = tkinter.StringVar()
        # checkval.set('dis thi ')
        # checkval.set('v1')
        nonrepeatersval = tkinter.StringVar()
        nonrepeatersval.set('0')
        maxrepetitionsval = tkinter.StringVar()
        maxrepetitionsval.set('25')

        oidentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=oidval)
        oidentry.place(x=85, y=30)
        instanceentry = tkinter.Entry(popwind, highlightbackground='white', width=10, textvariable=instanceval)
        instanceentry.place(x=410, y=30)
        typeddl = tkinter.ttk.Combobox(popwind, state='readonly', width=5)
        typeddl['value'] = ("全局", "局部")
        typeddl.current(0)
        typeddl.pack(side=tkinter.RIGHT, padx=1, pady=1)
        typeddl.place(x=290, y=30)
        nonrepeatersentry = tkinter.Entry(popwind, highlightbackground='white', width=5, textvariable=nonrepeatersval)
        nonrepeatersentry.place(x=285, y=90)
        maxrepetitionsentry = tkinter.Entry(popwind, highlightbackground='white', width=5, textvariable=maxrepetitionsval)
        maxrepetitionsentry.place(x=385, y=90)
        Syntaxddl = tkinter.ttk.Combobox(popwind, state='readonly', width=14)
        Syntaxddl['value'] = ("Octets", "INTEGER", "Integer32","OBJECT IDENTIFIER","NULL","IpAddress","Counter32","Gauge32","Unsigned32","TimeTicks","Opaque","Counter64","Bits")
        Syntaxddl.current(0)
        Syntaxddl.pack(side=tkinter.RIGHT, padx=1, pady=1)
        Syntaxddl.place(x=100, y=90)
        # Syntaxentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=Syntaxval)
        # Syntaxentry.place(x=100, y=90)
        checkentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=checkval)
        checkentry.place(x=135, y=150)
        keyentry = tkinter.Entry(popwind, highlightbackground='white', width=15, textvariable=keyval)
        keyentry.place(x=345, y=150)
        resulttext = Text(popwind, height=20, width=60)
        resulttext.place(x=40, y=300, anchor='nw')
        tkinter.Button(popwind, text='GETBULK', width=10, command=onSumbitClick).place(x=320, y=190, anchor='nw')
        tkinter.Button(popwind, text='取消', width=10, command=popwind.destroy).place(x=410, y=190, anchor='nw')

    def snmp_set(self):

        def clearnresult():
            resulttext.delete(0.0, END)

        def writeresult(text):
            resulttext.insert(END, text)
            resulttext.insert(END, '\n')

        def onSumbitClick():
            self.set_dir = {}
            set = str(setval.get())
            temp_config = 1
            oid = str(oidval.get())
            instance = str(instanceval.get())
            syntax = str(Syntaxddl.get())
            type = str(typeddl.get())
            key = str(keyval.get())
            check = str(checkval.get())
            if type == '全局':
                if instance != '0':
                    self.popwarningwin('全局类型oid实例必须为0，请确认修改！')
                    temp_config = 0
            else:
                if instance == '0' or instance == '':
                    self.popwarningwin('局部类型oid实例不能为0和空，请确认修改！')
                    temp_config = 0

            if temp_config == 1:
                if oid:
                    self.set_dir['oid'] = oid
                    if instance:
                        self.set_dir['instance'] = instance
                        if syntax:
                            self.set_dir['syntax'] = syntax
                            if check:
                                self.set_dir['check'] = check
                                if set:
                                    if key:
                                        self.set_dir['key'] = key
                                        self.set_dir['type'] = type
                                        get_oid = oid + '.' + instance
                                        ip = self.connect_dir.get('ip')
                                        version = str(self.connect_dir.get('version'))
                                        if version == 'v1':
                                            errorStatus, varBinds, errorIndication = self.snmp_operate_set(0, ip, get_oid, set, syntax)
                                        elif version == 'v2':
                                            errorStatus, varBinds, errorIndication = self.snmp_operate_set(1, ip, get_oid, set, syntax)
                                        # oid_result = varBinds[0][1]
                                        if errorIndication:
                                            writeresult('下发失败，错误信息如下：')
                                            writeresult(errorIndication)
                                            writeresult('错误码如下：')
                                            writeresult(errorStatus)
                                            writeresult('')
                                        else:
                                            if errorStatus == 0:
                                                self.after_data = self.publicmeth.getconfig(self.filepath)
                                                compare_data = self.publicmeth.compare_list(self.before_data, self.after_data)
                                                if compare_data == 0:
                                                    config = ''
                                                else:
                                                    config = self.publicmeth.return_config(compare_data)
                                                    self.before_data = []
                                                    self.before_data = self.after_data
                                                    self.after_data = []
                                                writeresult('下发成功，结果如下：')
                                                for varBind in varBinds:
                                                    writeresult(varBind)
                                                writeresult('')
                                                get_text = self.create_set(self.set_dir, config)
                                                self.writetext(get_text)
                                            else:
                                                writeresult('下发失败，错误码如下：')
                                                writeresult(errorStatus)
                                                writeresult('')
                                
                                    else:
                                        self.popwarningwin('请输入命令行返回内容获取值的关键字')
                                else:
                                    self.popwarningwin('请输入需要下发的值')
                            else:
                                self.popwarningwin('请输入check值')
                        else:
                            self.popwarningwin('请输入oid数据类型')
                    else:
                        self.popwarningwin('请输入实例')
                else:
                    self.popwarningwin('请输入oid')
            else:
                pass
            # popwind.destroy()
            
            # print(oid_result)
            # print(errorStatus)
            # get_text = self.create_get(self.set_dir)
            # self.writetext(get_text)

        # 定义弹窗
        popwind = tkinter.Toplevel(self.init_window)
        # popwind = tk.Tk()
        popwind.title("MIB SET操作")
        popwind.geometry('500x600+386+163')
        popwind["bg"] = "Ivory"

        tkinter.Label(popwind, text='oid:').place(x=40, y=30, anchor='nw')
        tkinter.Label(popwind, text='实例:').place(x=365, y=30, anchor='nw')
        tkinter.Label(popwind, text='类型:').place(x=245, y=30, anchor='nw')
        tkinter.Label(popwind, text='数据类型:').place(x=40, y=90, anchor='nw')
        tkinter.Label(popwind, text='下发值:').place(x=280, y=90, anchor='nw')
        tkinter.Label(popwind, text='结果对应命令行:').place(x=40, y=150, anchor='nw')
        tkinter.Label(popwind, text='关键字:').place(x=290, y=150, anchor='nw')
        tkinter.Label(popwind, text='获取结果').place(x=220, y=270, anchor='nw')

        # 将输入的注册名赋值给变量
        oidval = tkinter.StringVar()
        # oidval.set('1.3.6.1.2.1.31.1.1.1.18')
        instanceval = tkinter.StringVar()
        # instanceval.set('1029')
        setval = tkinter.StringVar()
        # Syntaxval = tkinter.StringVar()
        # Syntaxval.set('Octets')
        checkval = tkinter.StringVar()
        keyval = tkinter.StringVar()
        # checkval.set('dis thi ')
        # checkval.set('v1')

        oidentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=oidval)
        oidentry.place(x=85, y=30)
        instanceentry = tkinter.Entry(popwind, highlightbackground='white', width=10, textvariable=instanceval)
        instanceentry.place(x=410, y=30)
        typeddl = tkinter.ttk.Combobox(popwind, state='readonly', width=5)
        typeddl['value'] = ("全局", "局部")
        typeddl.current(0)
        typeddl.pack(side=tkinter.RIGHT, padx=1, pady=1)
        typeddl.place(x=290, y=30)
        setvalentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=setval)
        setvalentry.place(x=340, y=90)
        Syntaxddl = tkinter.ttk.Combobox(popwind, state='readonly', width=14)
        Syntaxddl['value'] = ("Octets", "INTEGER", "Integer32","OBJECT IDENTIFIER","NULL","IpAddress","Counter32","Gauge32","Unsigned32","TimeTicks","Opaque","Counter64","Bits")
        Syntaxddl.current(0)
        Syntaxddl.pack(side=tkinter.RIGHT, padx=1, pady=1)
        Syntaxddl.place(x=100, y=90)
        # Syntaxentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=Syntaxval)
        # Syntaxentry.place(x=100, y=90)
        checkentry = tkinter.Entry(popwind, highlightbackground='white', textvariable=checkval)
        checkentry.place(x=135, y=150)
        keyentry = tkinter.Entry(popwind, highlightbackground='white', width=15, textvariable=keyval)
        keyentry.place(x=345, y=150)
        resulttext = Text(popwind, height=20, width=60)
        resulttext.place(x=40, y=300, anchor='nw')
        tkinter.Button(popwind, text='SET', width=10, command=onSumbitClick).place(x=320, y=190, anchor='nw')
        tkinter.Button(popwind, text='取消', width=10, command=popwind.destroy).place(x=410, y=190, anchor='nw')

    def popwarningwin(self, warningtext):
        root = tkinter.Tk()
        root.withdraw()
        tkinter.messagebox.showinfo(title='Warning', message=warningtext)

    def create_connect(self, connect_dir):
        ip = connect_dir.get('ip')
        version = connect_dir.get('version')
        header = """SET_RUNNING_PARAM if_address 1
<TESTCASE_BEGIN>
    <TESTCASE_HEADER_BEGIN>
        <TITLE>				"魔镜自动生成mib脚本"
        <INDEX>				"自行修改"
        <LEVEL>				"3"
        <WEIGHT>			"3"
        <MODULE>			"SNMP-Agent"
        <TYPE>				"FUNCTION"
        <AUTHOR>            "魔镜脚本开发系统"
        <LIMITATION>        "CmwV7Device"
        <VERSION>           "2.1"
        <DESIGN>			"用户自行修改描述信息"
        <SOURCE>			"SNMP-Agent_20.1.12.21_1.topo"
    <TESTCASE_HEADER_END>

    <TESTCASE_DEVICE_MAP_BEGIN>
    <TESTCASE_DEVICE_MAP_END>
    
#===================================SNMP-Agent初始配置===================================#
        {DUT} removeSnmpLocalEngineId
        
    #=================================配置和检查===================================#
        """.format(DUT=self.dutname)
        if version != 'v3':
            temp_config = '''\
        set read_community "read"                          ;#可读团体名字为read
        set write_community "write"                        ;#可写团体名字为write
        
        set RouterSNMPVersion "{v1}"                         ;#路由器SNMP版本
        set NMSVersion "1"     
        set NMSRetry 10                                    ;#NMS重试次数
        set NMSTimeOut 3000                                ;#NMS超时时间
        set ContactInfo "h3c@h3c.com"                      ;#系统联系信息为"h3c@h3c.com"
        #设置{DUT} SNMPAgent版本为V1
        {DUT} setSnmpState -ver $RouterSNMPVersion
        
        #设置{DUT} SNMP可读团体为名为read
        {DUT} addSnmpCommunity -name $read_community -type read
        #设置{DUT} SNMP可写团体为名为write
        {DUT} addSnmpCommunity -name $write_community -type write
        
        #设置联系信息为ContactInfo
        {DUT} setSnmpSysInfo -contact $ContactInfo -location $LocationInfo
        
        #配置主机参数
        snmp_config -ver $NMSVersion -addr {addr} -readcom $read_community -writecom $write_community -retry $NMSRetry -timeout $NMSTimeOut
            '''.format(v1=version, addr=ip, DUT=self.dutname)
            text = header + temp_config
            return text
        else:
            temp_config = '''\
        set write_community "private"                   ;#可写团体名字为private
        
        set UserName1 "user1"
        set UserName2 "user2"
        set UserName3 "user3"
        
        set MIBTree "mib-2"
        set WriteView "myview"
        
        set GroupName1 "group1"
        set GroupName2 "group2"
        set GroupName3 "group3"
        
        set SysName "NE08"
        set Syntax  "OCTETS"
        
        set agentSecModel  "usm"
        #set agentSecLevel "noauthnopriv"
        set AgentSecLevel "authpriv" 
        
        #这里设置重试次数为1，方便后面对检查
        set NMSRetry 1                                    ;#NMS重试次数
        set NMSTimeOut 3000                                ;#NMS超时时间
        set AuthPassword "abc12345ABC"                     ;#认证密码为 abc12345ABC
        set PrivPassword "abc12345ABC"                     ;#加密密码为 abc12345ABC
        set AgentSecModel  "usm"
        
        #设置错误的认证或加密密码
        set AuthPasswordWrong "abc12345"                     
        set PrivPasswordWrong "abc12345"   
                      
        #设置{DUT} SNMPAgent版本为v3
        {DUT} setSnmpState -ver v3
        
        #添加SNMPv3版本的组
        {DUT} addSnmpGroup -name $GroupName3 -ver v3 -writeView $WriteView
        #添加SNMPv3版本的用户
        {DUT} addSnmpUsmUser -ver v3 -usmUserName $UserName3 -groupName $GroupName3 -passwordMode simple -authMode md5 -authPwd $AuthPassword -privMode des56 -privPwd $PrivPassword
        {DUT} setSnmpMibView -viewName $WriteView -oidTree $MIBTree
         
        #配置主机参数
        snmp_adduser $UserName3 $AuthPassword $PrivPassword md5 des

        snmp_config -ver 3 -addr {addr} -readcom $UserName3 -writecom $UserName3 -retry $NMSRetry -timeout $NMSTimeOut -secmodel $AgentSecModel -seclevel $AgentSecLevel -secName $UserName3
       
            '''.format(addr=ip, DUT=self.dutname)
            text = header + temp_config
            return text

    def create_get(self, get_dir, config):
        oidlist = get_dir.get('oid').split(';')
        instance = get_dir.get('instance')
        syntaxlist = get_dir.get('syntax').split(';')
        checklist = get_dir.get('check').split(';')
        key = get_dir.get('key')
        if len(oidlist) > 1:
            for oid, index in enumerate(oidlist):
                pass
            for oid, index in enumerate(oidlist):
                pass
            for oid, index in enumerate(oidlist):
                pass
        else:
            for index, oid in enumerate(oidlist):
                oid = oid + '.' +instance
                syntax = syntaxlist[index]
                check = checklist[index]
                get_text = '''\
    #STEP1
    <STEP> "snmp get 测试" {{

        <CHECK> description "snmp get 测试"
        <CHECK> type custom
        <CHECK> args {{
        {config}
        set OID "{oid}"
        set Syntax "{syntax}"

        #清空PDU
        snmp_reset_pdu
        #对指定OID并执行GET操作，取得返回值
        snmp_get $OID

        set locationOID ""
        set locationSyntax ""
        set locationValue ""
        #取得返回PDU中的OID
        snmp_get_oid locationOID
        
        #取得返回PDU中的数据类型
        snmp_get_syn locationSyntax
        
        #取得返回PDU中的值
        snmp_get_val locationValue
        
        {DUT} ClearBuffer
        {DUT} Send "{check}"
        set screenInfo [{DUT} GetBuffer]
        #对Current messages进行整形
        set screenInfo [split $screenInfo "\\n"]
        set counter [llength $screenInfo]
        for {{set i 0}} {{$i < $counter}} {{incr i}} {{
                set str1 [lindex $screenInfo $i]
                    if {{[string first "{key}" $str1]!=-1}} {{
                        break
                        }} 
                        }}
                         regsub "{key}" $str1 "" str1
                         regsub -all " " $str1 "" str1
                         set CheckVal $str1
        expr [string equal $OID $locationOID] && [string equal $Syntax $locationSyntax] && [string equal $CheckVal $locationValue]
        }}
        <CHECK> repeat 5 -interval 3
        <CHECK> whenfailed {{PUTSINFO "mib get Value:$locationValue;device get value:$CheckVal; $OID $locationOID; $Syntax $locationSyntax"}}
        <CHECK>
}}
        '''.format(oid=oid, syntax=syntax, check=check, DUT=self.dutname, config=config, key=key)
                return get_text

    def create_getnext(self, get_dir, config):
        oidlist = get_dir.get('oid').split(';')
        instance = get_dir.get('instance')
        syntaxlist = get_dir.get('syntax').split(';')
        checklist = get_dir.get('check').split(';')
        key = get_dir.get('key')
        if len(oidlist) > 1:
            for oid, index in enumerate(oidlist):
                pass
            for oid, index in enumerate(oidlist):
                pass
            for oid, index in enumerate(oidlist):
                pass
        else:
            for index, oid in enumerate(oidlist):
                oid = oid + '.' + instance
                syntax = syntaxlist[index]
                check = checklist[index]
                get_text = '''\
    #STEP1
    <STEP> "snmp get_next 测试" {{

        <CHECK> description "snmp get_next 测试"
        <CHECK> type custom
        <CHECK> args {{
        {config}
        set OID "{oid}"
        set Syntax "{syntax}"

        #清空PDU
        snmp_reset_pdu
        #对指定OID并执行GET操作，取得返回值
        snmp_getnext $OID

        set locationOID ""
        set locationSyntax ""
        set locationValue ""
        #取得返回PDU中的OID
        snmp_get_oid locationOID
        
        #取得返回PDU中的数据类型
        snmp_get_syn locationSyntax
        
        #取得返回PDU中的值
        snmp_get_val locationValue
        
        {DUT} ClearBuffer
        {DUT} Send "{check}"
        set screenInfo [{DUT} GetBuffer]
        #对Current messages进行整形
        set screenInfo [split $screenInfo "\\n"]
        set counter [llength $screenInfo]
        for {{set i 0}} {{$i < $counter}} {{incr i}} {{
                set str1 [lindex $screenInfo $i]
                    if {{[string first "{key}" $str1]!=-1}} {{
                        break
                        }} 
                        }}
                         regsub "{key}" $str1 "" str1
                         regsub -all " " $str1 "" str1
                         set CheckVal $str1
        expr [string equal $OID $locationOID] && [string equal $Syntax $locationSyntax] && [string equal $CheckVal $locationValue]
        }}
        <CHECK> repeat 5 -interval 3
        <CHECK> whenfailed {{PUTSINFO "mib get Value:$locationValue;device get value:$CheckVal; $OID $locationOID; $Syntax $locationSyntax"}}
        <CHECK>
}}
        '''.format(oid=oid, syntax=syntax, check=check, DUT=self.dutname, config=config, key=key)
                return get_text

    def create_getbulk(self, get_dir, nonrepeaters, maxrepetitions):
        oidlist = get_dir.get('oid').split(';')
        instance = get_dir.get('instance')
        syntaxlist = get_dir.get('syntax').split(';')
        checklist = get_dir.get('check').split(';')
        key = get_dir.get('key')
        if len(oidlist) > 1:
            for oid, index in enumerate(oidlist):
                pass
            for oid, index in enumerate(oidlist):
                pass
            for oid, index in enumerate(oidlist):
                pass
        else:
            for index, oid in enumerate(oidlist):
                oid = oid + '.' + instance
                syntax = syntaxlist[index]
                check = checklist[index]
                get_text = '''\
    #STEP1
    <STEP> "snmp get_bulk 测试" {{

        <CHECK> description "snmp get_bulk 测试"
        <CHECK> type custom
        <CHECK> args {{

        set OID "{oid}"
        set Syntax "{syntax}"

        #清空PDU
        snmp_reset_pdu
        #对指定OID并执行GET操作，取得返回值
        snmp_getnext $OID

        set locationOID ""
        set locationSyntax ""
        set locationValue ""
        #取得返回PDU中的OID
        snmp_get_oid locationOID

        #取得返回PDU中的数据类型
        snmp_get_syn locationSyntax

        #取得返回PDU中的值
        snmp_get_val locationValue

        {DUT} ClearBuffer
        {DUT} Send "{check}"
        set screenInfo [{DUT} GetBuffer]
        #对Current messages进行整形
        set screenInfo [split $screenInfo "\\n"]
        set counter [llength $screenInfo]
        for {{set i 0}} {{$i < $counter}} {{incr i}} {{
                set str1 [lindex $screenInfo $i]
                    if {{[string first "{key}" $str1]!=-1}} {{
                        break
                        }} 
                        }}
                         regsub "{key}" $str1 "" str1
                         regsub -all " " $str1 "" str1
                         set CheckVal $str1
        expr [string equal $OID $locationOID] && [string equal $Syntax $locationSyntax] && [string equal $CheckVal $locationValue]
        }}
        <CHECK> repeat 5 -interval 3
        <CHECK> whenfailed {{PUTSINFO "mib get Value:$locationValue;device get value:$CheckVal; $OID $locationOID; $Syntax $locationSyntax"}}
        <CHECK>
}}
        '''.format(oid=oid, syntax=syntax, check=check, DUT=self.dutname, key=key)
                return get_text

    def create_set(self, get_dir, config):
        oidlist = get_dir.get('oid').split(';')
        instance = get_dir.get('instance')
        set = get_dir.get('set')
        syntaxlist = get_dir.get('syntax').split(';')
        checklist = get_dir.get('check').split(';')
        key = get_dir.get('key')
        if len(oidlist) > 1:
            for oid, index in enumerate(oidlist):
                pass
            for oid, index in enumerate(oidlist):
                pass
            for oid, index in enumerate(oidlist):
                pass
        else:
            for index, oid in enumerate(oidlist):
                oid = oid + '.' + instance
                syntax = syntaxlist[index]
                check = checklist[index]
                get_text = '''\
    #STEP1
    <STEP> "snmp set 测试" {{

        <CHECK> description "snmp set 测试"
        <CHECK> type custom
        <CHECK> args {{
        {config}
        set OID "{oid}"
        set Syntax "{syntax}"
        set setval "{set}"

        #清空PDU
        snmp_reset_pdu
        #对指定OID并执行SET操作
        snmp_set $OID $Syntax $setval

        set ErrStatus ""
        set locationOID ""
        set locationSyntax ""
        set locationValue ""
        
        #获取返回错误状态
        snmp_get_errstatus ErrStatus
        #取得返回PDU中的OID
        snmp_get_oid locationOID

        #取得返回PDU中的数据类型
        snmp_get_syn locationSyntax

        #取得返回PDU中的值
        snmp_get_val locationValue

        {DUT} ClearBuffer
        {DUT} Send "{check}"
        set screenInfo [{DUT} GetBuffer]
        #对Current messages进行整形
        set screenInfo [split $screenInfo "\\n"]
        set counter [llength $screenInfo]
        for {{set i 0}} {{$i < $counter}} {{incr i}} {{
                set str1 [lindex $screenInfo $i]
                    if {{[string first "{key}" $str1]!=-1}} {{
                        break
                        }} 
                        }}
                         regsub "{key}" $str1 "" str1
                         regsub -all " " $str1 "" str1
                         set CheckVal $str1
        expr $ErrStatus==0
        }}
        <CHECK> repeat 5 -interval 3
        <CHECK> whenfailed {{PUTSINFO "errorstatus=$ErrStatus"}}
        <CHECK>
}}
        '''.format(oid=oid, syntax=syntax, check=check, set=set, DUT=self.dutname, config=config, key=key)
                return get_text

    def save_file(self):
        file_path = filedialog.asksaveasfilename(title=u'保存⽂件', initialdir='./result', initialfile='tcl', filetypes=[("tcl文件", ".tcl")])
        # print('保存⽂件：', file_path)
        file_text = self.tcltext.get('1.0', tk.END)
        if file_path != '':
            with open(file=file_path, mode='w+', encoding='utf-8') as file:
                file.write(file_text)
                file.close()
                self.tcltext.delete(0.0, END)

    def snmp_operate_get(self, version, ip, oid):
        errorIndication, errorStatus, errorindex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData('snmp-agent', 'public', version),  # 配置community
                   UdpTransportTarget((ip, 161)),  # 配置目的地址和端口号
                   ContextData(),
                   ObjectType(ObjectIdentity(oid))  # 读取的OID，获取主机名
                   )
        )
        return errorStatus, varBinds, errorIndication

    def snmp_operate_getnext(self, version, ip, oid):
        errorIndication, errorStatus, errorindex, varBinds = next(
            nextCmd(SnmpEngine(),
                   CommunityData('snmp-agent', 'public', version),  # 配置community
                   UdpTransportTarget((ip, 161)),  # 配置目的地址和端口号
                   ContextData(),
                   ObjectType(ObjectIdentity(oid))
                   )
        )
        return errorStatus, varBinds, errorIndication

    def snmp_operate_getbulk(self, version, ip, oid, nonrepeaters, maxrepetitions):
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorindex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData('snmp-agent', 'public', version),  # 配置community
            cmdgen.UdpTransportTarget((ip, 161)), 0, 25, oid, )
        # 配置IP地址和端口号；#0为non-repeaters 和  25为max-repetitions(一个数据包中最多25个条目，和显示无关)

        return errorStatus, varBindTable, errorIndication

    def snmp_operate_set(self, version, ip, oid, val, type):
        cmdGen = cmdgen.CommandGenerator()
        if type == 'Octets':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.OctetString(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'INTEGER':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.Integer(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'Integer32':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.Integer32(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'OBJECT IDENTIFIER':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.ObjectIdentifier(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'NULL':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.Null(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'IpAddress':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.IpAddress(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'Counter32':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.Counter32(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'Gauge32':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.Gauge32(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'Unsigned32':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.Unsigned32(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'TimeTicks':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.TimeTicks(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'Opaque':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.Opaque(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'Counter64':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.Counter64(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication
        elif type == 'Bits':
            errorIndication, errorStatus, errorindex, varBinds = cmdGen.setCmd(
                cmdgen.CommunityData('snmp-agent', 'private', version),  # 写入Community
                cmdgen.UdpTransportTarget((ip, 161)),  # IP地址和端口号
                (oid, rfc1902.Bits(val))  # OID和写入的内容，需要进行编码！
            )
            return errorStatus, varBinds, errorIndication


    def end_test(self):
        self.writetext("<TESTCASE_END>")

    # def star(self):
    #     self.init_window = tk.Tk()
    #     ZMJ_PORTAL = MibOperate()
    #     # 设置根窗口默认属性
    #     ZMJ_PORTAL.mib_gui()
    #     self.init_window.mainloop()



# ss = MibOperate('ss','ss')
# ss.snmp_operate_get(2,'192.168.56.88','1.3.6.1.2.1.31.1.1.1.18.1029')
# ss.create_connect()
# ss.mib_gui()
