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


        self.button1 = Button(self.init_window, text="连接设备", background="lightblue", foreground='black', width=10, command=self.ss)
        self.button1.place(x=100, y=100, anchor='nw', )
        self.button2 = Button(self.init_window, text='连接测试仪', background="lightblue", foreground='black', width=10, command=self.ss)
        self.button2.place(x=100, y=180, anchor='nw')
        self.button3 = Button(self.init_window, text='HOST连接', background="lightblue", foreground='black', width=10, command=self.ss)
        self.button3.place(x=100, y=260, anchor='nw')
        self.button4 = Button(self.init_window, text=' 开始录制 ', background="lightblue", foreground='black', width=10, command=self.ss)
        self.button4.place(x=100, y=340, anchor='nw')
        self.button5 = Button(self.init_window, text=' 结束录制 ', background="lightblue", foreground='black', width=10, command=self.ss)
        self.button5.place(x=100, y=420, anchor='nw')
        self.button6 = Button(self.init_window, text=' 生成脚本 ', background="lightblue", foreground='black', width=10, command=self.ss)
        self.button6.place(x=100, y=500, anchor='nw')
        self.button7 = Button(self.init_window, text='log路径设置', background="lightblue", foreground='black', width=10, command=self.ss)
        self.button7.place(x=350, y=20, anchor='nw')
        self.button8 = Button(self.init_window, text='生成路径设置', background="lightblue", foreground='black', width=10, command=self.ss)
        self.button8.place(x=550, y=20, anchor='nw')
        self.button9 = Button(self.init_window, text='保存', background="lightblue", foreground='black', width=5, command=self.ss)
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


ss = MibOperate()
ss.mib_gui()