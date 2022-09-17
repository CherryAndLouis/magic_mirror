# -*- coding:utf-8 -*-
import os
import datetime
from public import *
from tkinter import *
from tkinter import Button
from tkinter import messagebox
from tkinter import Entry
from tkinter import StringVar
from tkinter.ttk import *
import requests
from requests.auth import HTTPBasicAuth
import json
from pathlib import Path
import re

import tkinter as tk

from tkinter import Checkbutton
from tkinter import IntVar


class testMasterStreamCreate():
    def __init__(self):

        self.JSON_DIR = Path(__file__).parents[0] / 'json'
        # self.tmtcl = ''
        self.topoPortName = "PORT1"
        self.tm_dir_star = {}

    def set_init_window(self):
        self.init_window_name_tm = tk.Tk()
        self.init_window_name_tm.title("TestMaster_Gui")
        self.init_window_name_tm.geometry('300x500+270+110')
        self.init_window_name_tm["bg"] = "Beige"
        # self.init_window_name_tm.iconbitmap("python.gif")
        self.init_window_name_tm.iconbitmap("logo.png")

        Label_CreateStream = Label(self.init_window_name_tm, text='创建流量')
        Label_CreateStream.pack()
        button_CreateStream_Bound = Button(self.init_window_name_tm, text='Bound Stream', command=self.button_StreamCreate_Bound)
        button_CreateStream_Bound.pack()
        button_CreateStream_Ethernet_Custom = Button(self.init_window_name_tm, text='Ethernet Raw Stream',command=self.button_StreamCreate_Ethernet_Custom)
        button_CreateStream_Ethernet_Custom.pack()
        button_CreateStream_ARP = Button(self.init_window_name_tm, text='ARP Raw Stream', command=self.button_StreamCreate_ARP)
        button_CreateStream_ARP.pack()
        button_CreateStream_IPv4_Custom = Button(self.init_window_name_tm, text='IPv4 Raw Stream', command=self.button_StreamCreate_IPv4_Custom)
        button_CreateStream_IPv4_Custom.pack()
        button_CreateStream_IPv6_Custom = Button(self.init_window_name_tm, text='IPv6 Raw Stream', command=self.button_StreamCreate_IPv6_Custom)
        button_CreateStream_IPv6_Custom.pack()
        button_CreateStream_MPLS = Button(self.init_window_name_tm, text='MPLS Raw Stream', command=self.button_StreamCreate_MPLS)
        button_CreateStream_MPLS.pack()
        button_CreateStream_TCPv4_Custom = Button(self.init_window_name_tm, text='TCPv4 Raw Stream', command=self.button_StreamCreate_TCPv4)
        button_CreateStream_TCPv4_Custom.pack()
        button_CreateStream_TCPv6_Custom = Button(self.init_window_name_tm, text='TCPv6 Raw Stream', command=self.button_StreamCreate_TCPv6)
        button_CreateStream_TCPv6_Custom.pack()
        button_CreateStream_UDPv4_Custom = Button(self.init_window_name_tm, text='UDPv4 Raw Stream', command=self.button_StreamCreate_UDPv4)
        button_CreateStream_UDPv4_Custom.pack()
        button_CreateStream_UDPv6_Custom = Button(self.init_window_name_tm, text='UDPv6 Raw Stream', command=self.button_StreamCreate_UDPv6)
        button_CreateStream_UDPv6_Custom.pack()

        Label_CreateStream = Label(self.init_window_name_tm, text='开始打流')
        Label_CreateStream.pack()
        button_CreateStream_Bound = Button(self.init_window_name_tm, text='Stream Start',command=self.button_StreamStart)
        button_CreateStream_Bound.pack()

        Label_CreateStream = Label(self.init_window_name_tm, text='停止打流')
        Label_CreateStream.pack()
        button_CreateStream_Bound = Button(self.init_window_name_tm, text='Stream Stop',command=self.button_StreamStop)
        button_CreateStream_Bound.pack()

        self.init_window_name_tm.mainloop()


        # Label_Separat1 = Label(self.init_window_name_tm, text='----------最新创建流量信息--------------')
        # Label_Separat1.pack()
        # newStreamText = '最新创建流量信息：'
        # Label_NewCreateStreamInfo = Label(self.init_window_name_tm, text=newStreamText)
        # Label_NewCreateStreamInfo.pack()

        # self.init_window_name_tm.title("创建&操作流量")
        # self.init_window_name_tm.geometry('600x800')
        # self.init_window_name_tm.after(10000, self.refreshNewCreateStreamInfo)
        # self.init_window_name_tm.protocol("WM_DELETE_WINDOW", self.on_closing)

    # 之所以单独弄一个 开始 的函数，就是在点击的时候，写入run 语句，并退出串口，继续设备侧的操作
    def button_StreamStart(self):
        # 写脚本文件
        # topoPortName = reservedPortDict[Combobox_GetInfoPort.get()]["topoPortName"]
        # topoPortName = "PORT1"

        timestart = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')

        tclrun = '\nTestInstrument1.' + self.topoPortName + ' Run'

        startdict = {
            "time": timestart,
            "config": tclrun
        }
        self.init_window_name_tm.destroy()
        print(startdict)
        self.tm_dir_star = startdict
        return startdict

    # 不关注之前怎么操作的，点击该按钮，就返回停止打流的语句，然后根据时间先后进行插入脚本
    def button_StreamStop(self):
        # 写脚本文件
        # topoPortName = reservedPortDict[Combobox_GetInfoPort.get()]["topoPortName"]
        # topoPortName = "PORT1"

        stoptime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        tclstop = '\nTestInstrument1.' + self.topoPortName + ' Stop' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream' + '\nTestInstrument1.' + self.topoPortName + ' resetNetStreamStatistics'

        stopdict = {
            "time": stoptime,
            "tcl": tclstop
        }
        self.init_window_name_tm.destroy()
        print(stopdict)
        return stopdict

    def button_StreamCreate_Bound(self):

        def button_StreamCreate_Bound_Custom():

            if Combobox_GetInfoPort.get() == '':
                messagebox.showinfo("创建流量失败", "未选择创建流量所属接口，请选择接口重试")
            else:
                # 写脚本文件
                # topoPortName = reservedPortDict[Combobox_GetInfoPort.get()]["topoPortName"]
                # topoPortName = "PORT1"

                tmtcltime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                tmtcl = '\n#create Ethernet custom Stream '

                # 先删除测试仪的流
                tmtcl = tmtcl + '\n#先删除测试仪的流' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream'

                if ckVlan_var.get() == "Y":
                    tmtcl = tmtcl + '\nSMB.' + self.topoPortName + ' ETH_SetVlanPkt ' + Entry_FrameLength.get() + ' ' + Entry_VlanID.get() + ' ' + Entry_SrcMacAddr.get() + ' ' + Entry_DestMacAddr.get() + ' ' + Entry_SrcIPv4Addr.get() + ' ' + Entry_DestIPv4Addr.get()

                else:
                    tmtcl = tmtcl + '\nSMB.' + self.topoPortName + ' SetEthIIPkt ' + Entry_FrameLength.get() + ' ' + Entry_SrcMacAddr.get() + ' ' + Entry_DestMacAddr.get() + ' ' + Entry_SrcIPv4Addr.get() + ' ' + Entry_DestIPv4Addr.get()

                if Combobox_SrcMacAddrIsModifier.get():
                    tmtcl = tmtcl + '\nSMB.' + self.topoPortName + ' ETH_SetSrcMac ' + Entry_SrcMacAddr.get() + '$::HVFD_INCR' + Entry_SrcMacAddrModifierCount.get()

                if Combobox_DestMacAddrIsModifier.get():
                    tmtcl = tmtcl + '\nSMB.' + self.topoPortName + ' ETH_SetDstMac ' + Entry_SrcMacAddr.get() + '$::HVFD_INCR' + Entry_SrcMacAddrModifierCount.get()

                tmtcldict = {
                    "time": tmtcltime,
                    "tcl": tmtcl
                }
                print(tmtcldict)
                return tmtcldict


        root40 = Tk()
        reservedPortDict = {}
        intf_jsonfile = Path(self.JSON_DIR) / 'intf_reserved.json'
        with open(intf_jsonfile, 'r') as f:
            intf_json_data = f.read()
            reservedPortDict = json.loads(intf_json_data)
        reservedPortList = []
        reservedPortList = list(reservedPortDict.keys())
        Label_Separat1 = Label(root40, text='----------公共配置--------------')
        Label_Separat1.grid(row=0)
        Label_OperatePort = Label(root40, text='选择创建流量所属接口')
        Label_OperatePort.grid(row=1, column=0)

        Combobox_GetInfoPort = Combobox(root40)
        Combobox_GetInfoPort["value"] = reservedPortList
        Combobox_GetInfoPort.grid(row=1, column=1)

        Label_OperateRcvPort = Label(root40, text='选择流量接收接口，不选择为Any')
        Label_OperateRcvPort.grid(row=1, column=2)

        portVar_getInfoRcv = StringVar()
        Combobox_GetInfoRcvPort = Combobox(root40, textvariable=portVar_getInfoRcv)
        Combobox_GetInfoRcvPort["value"] = reservedPortList
        Combobox_GetInfoRcvPort.grid(row=1, column=3)

        Label_DurationMode = Label(root40, text='端口流量发送Duration模式:')
        Label_DurationMode.grid(row=2, column=0)
        DurationModeList = ["Continuous", "Bursts"]
        DurationModeVar = StringVar()
        Combobox_DurationMode = Combobox(root40, textvariable=DurationModeVar)
        Combobox_DurationMode["value"] = DurationModeList
        Combobox_DurationMode.grid(row=2, column=1)

        Label_FrameLength = Label(root40, text='流量包长:')
        Label_FrameLength.grid(row=3, column=0)
        Entry_FrameLength = Entry(root40)
        Entry_FrameLength.grid(row=3, column=1)
        Entry_FrameLength.delete(0, "end")
        Entry_FrameLength.insert(0, "128")

        Label_LoadUnit = Label(root40, text='Load单位类型:')
        Label_LoadUnit.grid(row=4, column=0)
        LoadUnitList = ["percent", "fps", "bps", "kbps", "mbps"]
        LoadUnitVar = StringVar()
        Combobox_LoadMode = Combobox(root40, textvariable=LoadUnitVar)
        Combobox_LoadMode["value"] = LoadUnitList
        Combobox_LoadMode.grid(row=4, column=1)

        Label_Load = Label(root40, text='Load:')
        Label_Load.grid(row=4, column=2)
        Entry_Load = Entry(root40)
        Entry_Load.grid(row=4, column=3)
        Entry_Load.delete(0, "end")
        Entry_Load.insert(0, "10")

        # Label_Vlan = Label(root40, text='Vlan Encap Info:')
        # Label_Vlan.grid(row=5, column=0)
        # ckVlan_var = IntVar()
        # ckVlan = Checkbutton(root40, text='设备是否需要Vlan封装',variable=ckVlan_var)
        # ckVlan.grid(row=5, column=1)

        Label_Vlan = Label(root40, text='设备是否需要Vlan封装:')
        Label_Vlan.grid(row=5, column=0)
        ckVlan_var = Combobox(root40)
        ckVlan_var["value"] = ["Y","N"]
        ckVlan_var.grid(row=5, column=1)

        Label_VlanID = Label(root40, text='Vlan ID:')
        Label_VlanID.grid(row=5, column=2)
        Entry_VlanID = Entry(root40)
        Entry_VlanID.grid(row=5, column=3)
        Entry_VlanID.delete(0, "end")
        Entry_VlanID.insert(0, "1")

        Label_Separat2 = Label(root40, text='----------IPv4 custom stream参数--------------')
        Label_Separat2.grid(row=6, column=0)
        Label_SrcMacAddr = Label(root40, text='Src Mac Address:')
        Label_SrcMacAddr.grid(row=7, column=0)
        Entry_SrcMacAddr = Entry(root40)
        Entry_SrcMacAddr.grid(row=7, column=1)
        Entry_SrcMacAddr.delete(0, "end")
        Entry_SrcMacAddr.insert(0, "94:29:2F:01:00:0A")
        Label_SrcMacAddrIsModifier = Label(root40, text='Src Mac Address是否可变:')
        Label_SrcMacAddrIsModifier.grid(row=8, column=0)
        EnableList = [True, False]

        Combobox_SrcMacAddrIsModifier = Combobox(root40)
        Combobox_SrcMacAddrIsModifier["value"] = EnableList
        Combobox_SrcMacAddrIsModifier.grid(row=8, column=1)

        Label_SrcMacAddrModifierCount = Label(root40, text='Src Mac Address Modifier Count:')
        Label_SrcMacAddrModifierCount.grid(row=9, column=0)
        Entry_SrcMacAddrModifierCount = Entry(root40)
        Entry_SrcMacAddrModifierCount.grid(row=9, column=1)
        Entry_SrcMacAddrModifierCount.delete(0, "end")
        Entry_SrcMacAddrModifierCount.insert(0, "1")
        Label_SrcMacAddrModifierStep = Label(root40, text='Src Mac Address Modifier Step:')
        Label_SrcMacAddrModifierStep.grid(row=10, column=0)
        Entry_SrcMacAddrModifierStep = Entry(root40)
        Entry_SrcMacAddrModifierStep.grid(row=10, column=1)
        Entry_SrcMacAddrModifierStep.delete(0, "end")
        Entry_SrcMacAddrModifierStep.insert(0, "00:00:00:00:00:01")
        Label_SrcMacAddrModifierMask = Label(root40, text='Src Mac Address Modifier Mask:')
        Label_SrcMacAddrModifierMask.grid(row=11, column=0)
        Entry_SrcMacAddrModifierMask = Entry(root40)
        Entry_SrcMacAddrModifierMask.grid(row=11, column=1)
        Entry_SrcMacAddrModifierMask.delete(0, "end")
        Entry_SrcMacAddrModifierMask.insert(0, "00:0:FF:FF:FF:FF")

        Label_DestMacAddr = Label(root40, text='Dest Mac Address:')
        Label_DestMacAddr.grid(row=12, column=0)
        Entry_DestMacAddr = Entry(root40)
        Entry_DestMacAddr.grid(row=12, column=1)
        Entry_DestMacAddr.delete(0, "end")
        Entry_DestMacAddr.insert(0, "94:29:2F:02:00:0A")
        Label_DestMacAddrIsModifier = Label(root40, text='Dest Mac Address是否可变:')
        Label_DestMacAddrIsModifier.grid(row=13, column=0)

        Combobox_DestMacAddrIsModifier = Combobox(root40)
        Combobox_DestMacAddrIsModifier["value"] = EnableList
        Combobox_DestMacAddrIsModifier.grid(row=13, column=1)

        Label_DestMacAddrModifierCount = Label(root40, text='Dest Mac Address Modifier Count:')
        Label_DestMacAddrModifierCount.grid(row=14, column=0)
        Entry_DestMacAddrModifierCount = Entry(root40)
        Entry_DestMacAddrModifierCount.grid(row=14, column=1)
        Entry_DestMacAddrModifierCount.delete(0, "end")
        Entry_DestMacAddrModifierCount.insert(0, "1")
        Label_DestMacAddrModifierStep = Label(root40, text='Dest Mac Address Modifier Step:')
        Label_DestMacAddrModifierStep.grid(row=15, column=0)
        Entry_DestMacAddrModifierStep = Entry(root40)
        Entry_DestMacAddrModifierStep.grid(row=15, column=1)
        Entry_DestMacAddrModifierStep.delete(0, "end")
        Entry_DestMacAddrModifierStep.insert(0, "00:00:00:00:00:01")
        Label_DestMacAddrModifierMask = Label(root40, text='Dest Mac Address Modifier Mask:')
        Label_DestMacAddrModifierMask.grid(row=16, column=0)
        Entry_DestMacAddrModifierMask = Entry(root40)
        Entry_DestMacAddrModifierMask.grid(row=16, column=1)
        Entry_DestMacAddrModifierMask.delete(0, "end")
        Entry_DestMacAddrModifierMask.insert(0, "00:0:FF:FF:FF:FF")

        Label_SrcIPv4Addr = Label(root40, text='Src IPv4 Address:')
        Label_SrcIPv4Addr.grid(row=17, column=0)
        Entry_SrcIPv4Addr = Entry(root40)
        Entry_SrcIPv4Addr.grid(row=17, column=1)
        Entry_SrcIPv4Addr.delete(0, "end")
        Entry_SrcIPv4Addr.insert(0, "1.1.1.1")
        Label_DestIPv4Addr = Label(root40, text='Dest IPv4 Address:')
        Label_DestIPv4Addr.grid(row=18, column=0)
        Entry_DestIPv4Addr = Entry(root40)
        Entry_DestIPv4Addr.grid(row=18, column=1)
        Entry_DestIPv4Addr.delete(0, "end")
        Entry_DestIPv4Addr.insert(0, "2.2.2.2")
        Label_DestIPv4AddrGateway = Label(root40, text='Dest IPv4 Address Gateway:')
        Label_DestIPv4AddrGateway.grid(row=19, column=0)
        Entry_DestIPv4Gateway = Entry(root40)
        Entry_DestIPv4Gateway.grid(row=19, column=1)
        Entry_DestIPv4Gateway.delete(0, "end")
        Entry_DestIPv4Gateway.insert(0, "2.2.2.2")

        button_createBoundPkt = Button(root40, text='创建IPv4流量', command=button_StreamCreate_Bound_Custom)
        button_createBoundPkt.grid(row=20, column=0)

        root40.title("TestMaster Ethernet Custom流量创建")
        root40.geometry('800x600')

        root40.mainloop()

    def button_StreamCreate_Ethernet_Custom(self):

        def button_StreamCreate_Ethernet_Custom():

            if Combobox_GetInfoPort.get() == '':
                messagebox.showinfo("创建流量失败", "未选择创建流量所属接口，请选择接口重试")
            else:
                # 写脚本文件
                # topoPortName = "PORT1"
                tmtcltime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                tmtcl = '\n#create Ethernet custom Stream '
                # 先删除测试仪的流
                tmtcl = tmtcl + '\n#先删除测试仪的流' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream'
                if ckVlan_var.get() == "Y":
                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' ETH_SetVlanPkt ' + Entry_FrameLength.get() + ' ' + Entry_VlanID.get() + ' ' + Entry_SrcMacAddr.get() + ' ' + Entry_DestMacAddr.get() + ' ' + Entry_SrcIPv4Addr.get() + ' ' + Entry_DestIPv4Addr.get()
                else:
                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetEthIIPkt ' + Entry_FrameLength.get() + ' ' + Entry_SrcMacAddr.get() + ' ' + Entry_DestMacAddr.get() + ' ' + Entry_SrcIPv4Addr.get() + ' ' + Entry_DestIPv4Addr.get()
                if Combobox_SrcMacAddrIsModifier.get():
                    # print("11")
                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 32 -Offset 6 -DataCount ' + Entry_SrcMacAddrModifierCount.get() + ' -Step ' + Entry_SrcMacAddrModifierStep.get()
                if Combobox_DestMacAddrIsModifier.get():
                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 32 -Offset 0 -DataCount ' + Entry_DestMacAddrModifierCount.get() + ' -Step ' + Entry_DestMacAddrModifierStep.get()

                tmtcldict = {
                    "time": tmtcltime,
                    "tcl": tmtcl
                }
                print(tmtcldict)
                return tmtcldict

        root41 = Tk()
        reservedPortDict = {}
        intf_jsonfile = Path(self.JSON_DIR) / 'intf_reserved.json'
        with open(intf_jsonfile, 'r') as f:
            intf_json_data = f.read()
            reservedPortDict = json.loads(intf_json_data)
        reservedPortList = []
        reservedPortList = list(reservedPortDict.keys())
        Label_Separat1 = Label(root41, text='----------公共配置--------------')
        Label_Separat1.grid(row=0)
        Label_OperatePort = Label(root41, text='选择创建流量所属接口')
        Label_OperatePort.grid(row=1, column=0)

        Combobox_GetInfoPort = Combobox(root41)
        Combobox_GetInfoPort["value"] = reservedPortList
        Combobox_GetInfoPort.grid(row=1, column=1)

        Label_OperateRcvPort = Label(root41, text='选择流量接收接口，不选择为Any')
        Label_OperateRcvPort.grid(row=1, column=2)
        portVar_getInfoRcv = StringVar()
        Combobox_GetInfoRcvPort = Combobox(root41, textvariable=portVar_getInfoRcv)
        Combobox_GetInfoRcvPort["value"] = reservedPortList
        Combobox_GetInfoRcvPort.grid(row=1, column=3)
        Label_DurationMode = Label(root41, text='端口流量发送Duration模式:')
        Label_DurationMode.grid(row=2, column=0)
        DurationModeList = ["Continuous", "Bursts"]
        DurationModeVar = StringVar()
        Combobox_DurationMode = Combobox(root41, textvariable=DurationModeVar)
        Combobox_DurationMode["value"] = DurationModeList
        Combobox_DurationMode.grid(row=2, column=1)
        Label_FrameLength = Label(root41, text='流量包长:')
        Label_FrameLength.grid(row=3, column=0)
        Entry_FrameLength = Entry(root41)
        Entry_FrameLength.grid(row=3, column=1)
        Entry_FrameLength.delete(0, "end")
        Entry_FrameLength.insert(0, "128")
        Label_LoadUnit = Label(root41, text='Load单位类型:')
        Label_LoadUnit.grid(row=4, column=0)
        LoadUnitList = ["percent", "fps", "bps", "kbps", "mbps"]
        LoadUnitVar = StringVar()
        Combobox_LoadMode = Combobox(root41, textvariable=LoadUnitVar)
        Combobox_LoadMode["value"] = LoadUnitList
        Combobox_LoadMode.grid(row=4, column=1)
        Label_Load = Label(root41, text='Load:')
        Label_Load.grid(row=4, column=2)
        Entry_Load = Entry(root41)
        Entry_Load.grid(row=4, column=3)
        Entry_Load.delete(0, "end")
        Entry_Load.insert(0, "10")

        # Label_Vlan = Label(root41, text='Vlan Encap Info:')
        # Label_Vlan.grid(row=5, column=0)
        # ckVlan = Checkbutton(root41, text='设备是否需要Vlan封装', onvalue=1, offvalue=0)
        # ckVlan.grid(row=5, column=1)

        Label_Vlan = Label(root41, text='设备是否需要Vlan封装:')
        Label_Vlan.grid(row=5, column=0)
        ckVlan_var = Combobox(root41)
        ckVlan_var["value"] = ["Y","N"]
        ckVlan_var.grid(row=5, column=1)


        Label_VlanID = Label(root41, text='Vlan ID:')
        Label_VlanID.grid(row=5, column=2)
        Entry_VlanID = Entry(root41)
        Entry_VlanID.grid(row=5, column=3)
        Entry_VlanID.delete(0, "end")
        Entry_VlanID.insert(0, "1")
        Label_Separat2 = Label(root41, text='----------IPv4 custom stream参数--------------')
        Label_Separat2.grid(row=6, column=0)
        Label_SrcMacAddr = Label(root41, text='Src Mac Address:')
        Label_SrcMacAddr.grid(row=7, column=0)
        Entry_SrcMacAddr = Entry(root41)
        Entry_SrcMacAddr.grid(row=7, column=1)
        Entry_SrcMacAddr.delete(0, "end")
        Entry_SrcMacAddr.insert(0, "94:29:2F:01:00:0A")
        Label_SrcMacAddrIsModifier = Label(root41, text='Src Mac Address是否可变:')
        Label_SrcMacAddrIsModifier.grid(row=8, column=0)

        EnableList = [True, False]
        Combobox_SrcMacAddrIsModifier = Combobox(root41)
        Combobox_SrcMacAddrIsModifier["value"] = EnableList
        Combobox_SrcMacAddrIsModifier.grid(row=8, column=1)

        Label_SrcMacAddrModifierCount = Label(root41, text='Src Mac Address Modifier Count:')
        Label_SrcMacAddrModifierCount.grid(row=9, column=0)
        Entry_SrcMacAddrModifierCount = Entry(root41)
        Entry_SrcMacAddrModifierCount.grid(row=9, column=1)
        Entry_SrcMacAddrModifierCount.delete(0, "end")
        Entry_SrcMacAddrModifierCount.insert(0, "1")
        Label_SrcMacAddrModifierStep = Label(root41, text='Src Mac Address Modifier Step:')
        Label_SrcMacAddrModifierStep.grid(row=10, column=0)
        Entry_SrcMacAddrModifierStep = Entry(root41)
        Entry_SrcMacAddrModifierStep.grid(row=10, column=1)
        Entry_SrcMacAddrModifierStep.delete(0, "end")
        Entry_SrcMacAddrModifierStep.insert(0, "00:00:00:00:00:01")
        Label_SrcMacAddrModifierMask = Label(root41, text='Src Mac Address Modifier Mask:')
        Label_SrcMacAddrModifierMask.grid(row=11, column=0)
        Entry_SrcMacAddrModifierMask = Entry(root41)
        Entry_SrcMacAddrModifierMask.grid(row=11, column=1)
        Entry_SrcMacAddrModifierMask.delete(0, "end")
        Entry_SrcMacAddrModifierMask.insert(0, "00:0:FF:FF:FF:FF")

        Label_DestMacAddr = Label(root41, text='Dest Mac Address:')
        Label_DestMacAddr.grid(row=12, column=0)
        Entry_DestMacAddr = Entry(root41)
        Entry_DestMacAddr.grid(row=12, column=1)
        Entry_DestMacAddr.delete(0, "end")
        Entry_DestMacAddr.insert(0, "94:29:2F:02:00:0A")
        Label_DestMacAddrIsModifier = Label(root41, text='Dest Mac Address是否可变:')
        Label_DestMacAddrIsModifier.grid(row=13, column=0)

        Combobox_DestMacAddrIsModifier = Combobox(root41)
        Combobox_DestMacAddrIsModifier["value"] = EnableList
        Combobox_DestMacAddrIsModifier.grid(row=13, column=1)
        Label_DestMacAddrModifierCount = Label(root41, text='Dest Mac Address Modifier Count:')
        Label_DestMacAddrModifierCount.grid(row=14, column=0)
        Entry_DestMacAddrModifierCount = Entry(root41)
        Entry_DestMacAddrModifierCount.grid(row=14, column=1)
        Entry_DestMacAddrModifierCount.delete(0, "end")
        Entry_DestMacAddrModifierCount.insert(0, "1")
        Label_DestMacAddrModifierStep = Label(root41, text='Dest Mac Address Modifier Step:')
        Label_DestMacAddrModifierStep.grid(row=15, column=0)
        Entry_DestMacAddrModifierStep = Entry(root41)
        Entry_DestMacAddrModifierStep.grid(row=15, column=1)
        Entry_DestMacAddrModifierStep.delete(0, "end")
        Entry_DestMacAddrModifierStep.insert(0, "00:00:00:00:00:01")
        Label_DestMacAddrModifierMask = Label(root41, text='Dest Mac Address Modifier Mask:')
        Label_DestMacAddrModifierMask.grid(row=16, column=0)
        Entry_DestMacAddrModifierMask = Entry(root41)
        Entry_DestMacAddrModifierMask.grid(row=16, column=1)
        Entry_DestMacAddrModifierMask.delete(0, "end")
        Entry_DestMacAddrModifierMask.insert(0, "00:0:FF:FF:FF:FF")

        Label_SrcIPv4Addr = Label(root41, text='Src IPv4 Address:')
        Label_SrcIPv4Addr.grid(row=17, column=0)
        Entry_SrcIPv4Addr = Entry(root41)
        Entry_SrcIPv4Addr.grid(row=17, column=1)
        Entry_SrcIPv4Addr.delete(0, "end")
        Entry_SrcIPv4Addr.insert(0, "1.1.1.1")
        Label_DestIPv4Addr = Label(root41, text='Dest IPv4 Address:')
        Label_DestIPv4Addr.grid(row=18, column=0)
        Entry_DestIPv4Addr = Entry(root41)
        Entry_DestIPv4Addr.grid(row=18, column=1)
        Entry_DestIPv4Addr.delete(0, "end")
        Entry_DestIPv4Addr.insert(0, "2.2.2.2")
        Label_DestIPv4AddrGateway = Label(root41, text='Dest IPv4 Address Gateway:')
        Label_DestIPv4AddrGateway.grid(row=19, column=0)
        Entry_DestIPv4Gateway = Entry(root41)
        Entry_DestIPv4Gateway.grid(row=19, column=1)
        Entry_DestIPv4Gateway.delete(0, "end")
        Entry_DestIPv4Gateway.insert(0, "2.2.2.2")

        button_createEthernetPkt = Button(root41, text='创建Ethernet流量', command=button_StreamCreate_Ethernet_Custom)
        button_createEthernetPkt.grid(row=20, column=0)

        root41.title("TestMaster Ethernet Custom流量创建")
        root41.geometry('800x600')

        root41.mainloop()

    def button_StreamCreate_ARP(self):

        def button_StreamCreate_ARP_Custom():

            if Combobox_GetInfoPort.get() == '':
                messagebox.showinfo("创建流量失败", "未选择创建流量所属接口，请选择接口重试")
            else:

                # 写脚本文件
                tmtcltime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                tmtcl = '\n#create ARP custom Stream '
                # ARPTypeList = ["ARP-Req", "ARP-Reply", "RARP-Req", "RARP-Reply"]

                # 先删除测试仪的流
                tmtcl = tmtcl + '\n#先删除测试仪的流' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream'
                if ckVlan_var.get() == "Y":
                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetArpPkt -PacketLen ' + Entry_FrameLength.get() + ' -VlanID ' + Entry_VlanID.get() + ' -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -ArpType ' + Combobox_ARPType.get()  + ' -ArpSrcMac ' + Entry_SrcHardwareAddr.get() + ' -ArpDesMac ' + Entry_DestHardwareAddr.get() + ' -ArpSrcIP ' + Entry_SrcIPv4Addr.get() + ' -ArpDesIP ' + Entry_DestIPv4Addr.get()
                else:
                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetArpPkt -PacketLen ' + Entry_FrameLength.get() + ' -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -ArpType ' + Combobox_ARPType.get()  + ' -ArpSrcMac ' + Entry_SrcHardwareAddr.get() + ' -ArpDesMac ' + Entry_DestHardwareAddr.get() + ' -ArpSrcIP ' + Entry_SrcIPv4Addr.get() + ' -ArpDesIP ' + Entry_DestIPv4Addr.get()

                tmtcldict = {
                    "time": tmtcltime,
                    "tcl": tmtcl
                }
                print(tmtcldict)
                return tmtcldict

        root42 = Tk()
        reservedPortDict = {}
        intf_jsonfile = Path(self.JSON_DIR) / 'intf_reserved.json'
        with open(intf_jsonfile, 'r') as f:
            intf_json_data = f.read()
            reservedPortDict = json.loads(intf_json_data)
        reservedPortList = []
        reservedPortList = list(reservedPortDict.keys())
        Label_Separat1 = Label(root42, text='----------公共配置--------------')
        Label_Separat1.grid(row=0)
        Label_OperatePort = Label(root42, text='选择创建流量所属接口')
        Label_OperatePort.grid(row=1, column=0)


        Combobox_GetInfoPort = Combobox(root42)
        Combobox_GetInfoPort["value"] = reservedPortList
        Combobox_GetInfoPort.grid(row=1, column=1)

        Label_OperateRcvPort = Label(root42, text='选择流量接收接口，不选择为Any')
        Label_OperateRcvPort.grid(row=1, column=2)
        portVar_getInfoRcv = StringVar()
        Combobox_GetInfoRcvPort = Combobox(root42, textvariable=portVar_getInfoRcv)
        Combobox_GetInfoRcvPort["value"] = reservedPortList
        Combobox_GetInfoRcvPort.grid(row=1, column=3)
        Label_DurationMode = Label(root42, text='端口流量发送Duration模式:')
        Label_DurationMode.grid(row=2, column=0)
        DurationModeList = ["Continuous", "Bursts"]
        DurationModeVar = StringVar()
        Combobox_DurationMode = Combobox(root42, textvariable=DurationModeVar)
        Combobox_DurationMode["value"] = DurationModeList
        Combobox_DurationMode.grid(row=2, column=1)
        Label_FrameLength = Label(root42, text='流量包长:')
        Label_FrameLength.grid(row=3, column=0)
        Entry_FrameLength = Entry(root42)
        Entry_FrameLength.grid(row=3, column=1)
        Entry_FrameLength.delete(0, "end")
        Entry_FrameLength.insert(0, "128")
        Label_LoadUnit = Label(root42, text='Load单位类型:')
        Label_LoadUnit.grid(row=4, column=0)
        LoadUnitList = ["percent", "fps", "bps", "kbps", "mbps"]
        LoadUnitVar = StringVar()
        Combobox_LoadMode = Combobox(root42, textvariable=LoadUnitVar)
        Combobox_LoadMode["value"] = LoadUnitList
        Combobox_LoadMode.grid(row=4, column=1)
        Label_Load = Label(root42, text='Load:')
        Label_Load.grid(row=4, column=2)
        Entry_Load = Entry(root42)
        Entry_Load.grid(row=4, column=3)
        Entry_Load.delete(0, "end")
        Entry_Load.insert(0, "10")

        # Label_Vlan = Label(root42, text='Vlan Encap Info:')
        # Label_Vlan.grid(row=5, column=0)
        # ckVlan_var = IntVar()
        # ckVlan = Checkbutton(root42, text='设备是否需要Vlan封装', variable=ckVlan_var)
        # ckVlan.grid(row=5, column=1)

        Label_Vlan = Label(root42, text='设备是否需要Vlan封装:')
        Label_Vlan.grid(row=5, column=0)
        ckVlan_var = Combobox(root42)
        ckVlan_var["value"] = ["Y","N"]
        ckVlan_var.grid(row=5, column=1)
        ckVlan_var.delete(0, "end")
        ckVlan_var.insert(0, "Y")

        Label_VlanID = Label(root42, text='Vlan ID:')
        Label_VlanID.grid(row=5, column=2)
        Entry_VlanID = Entry(root42)
        Entry_VlanID.grid(row=5, column=3)
        Entry_VlanID.delete(0, "end")
        Entry_VlanID.insert(0, "1")
        Label_Separat2 = Label(root42, text='----------ARPv4 custom stream参数--------------')
        Label_Separat2.grid(row=6, column=0)
        Label_SrcMacAddr = Label(root42, text='Src Mac Address:')
        Label_SrcMacAddr.grid(row=7, column=0)
        Entry_SrcMacAddr = Entry(root42)
        Entry_SrcMacAddr.grid(row=7, column=1)
        Entry_SrcMacAddr.delete(0, "end")
        Entry_SrcMacAddr.insert(0, "94:29:2F:01:00:0A")

        Label_DestMacAddr = Label(root42, text='Dest Mac Address:')
        Label_DestMacAddr.grid(row=8, column=0)
        Entry_DestMacAddr = Entry(root42)
        Entry_DestMacAddr.grid(row=8, column=1)
        Entry_DestMacAddr.delete(0, "end")
        Entry_DestMacAddr.insert(0, "94:29:2F:02:00:0A")

        ARPTypeList = ["ARP-Req", "ARP-Reply", "RARP-Req", "RARP-Reply"]
        # ARPTypeVar = StringVar()
        # ARPTypeVar.set("ARP-Req")
        Label_ARPType = Label(root42, text='ARP Type:')
        Label_ARPType.grid(row=9, column=0)
        Combobox_ARPType = Combobox(root42)
        Combobox_ARPType["value"] = ARPTypeList
        Combobox_ARPType.grid(row=9, column=1)
        Combobox_ARPType.delete(0, "end")
        Combobox_ARPType.insert(0, "ARP-Req")

        Label_SrcHardwareAddr = Label(root42, text='Sender Hardware Address:')
        Label_SrcHardwareAddr.grid(row=10, column=0)
        Entry_SrcHardwareAddr = Entry(root42)
        Entry_SrcHardwareAddr.grid(row=10, column=1)
        Entry_SrcHardwareAddr.delete(0, "end")
        Entry_SrcHardwareAddr.insert(0, "94:29:2F:01:00:0A")

        Label_SrcHardwareAddrIsModifier = Label(root42, text='Sender Hardware Address是否可变:')
        Label_SrcHardwareAddrIsModifier.grid(row=11, column=0)
        EnableList = [True, False]
        SrcHardwareAddrIsModifierVar = StringVar()
        Combobox_SrcHardwareAddrIsModifier = Combobox(root42, textvariable=SrcHardwareAddrIsModifierVar)
        Combobox_SrcHardwareAddrIsModifier["value"] = EnableList
        Combobox_SrcHardwareAddrIsModifier.grid(row=11, column=1)
        Label_SrcHardwareAddrModifierCount = Label(root42, text='Sender Hardware Address Modifier Count:')
        Label_SrcHardwareAddrModifierCount.grid(row=12, column=0)
        Entry_SrcHardwareAddrModifierCount = Entry(root42)
        Entry_SrcHardwareAddrModifierCount.grid(row=12, column=1)
        Entry_SrcHardwareAddrModifierCount.delete(0, "end")
        Entry_SrcHardwareAddrModifierCount.insert(0, "1")
        Label_SrcHardwareAddrModifierStep = Label(root42, text='Sender Hardware Address Modifier Step:')
        Label_SrcHardwareAddrModifierStep.grid(row=13, column=0)
        Entry_SrcHardwareAddrModifierStep = Entry(root42)
        Entry_SrcHardwareAddrModifierStep.grid(row=13, column=1)
        Entry_SrcHardwareAddrModifierStep.delete(0, "end")
        Entry_SrcHardwareAddrModifierStep.insert(0, "00:00:00:00:00:01")
        Label_SrcHardwareAddrModifierMask = Label(root42, text='Sender Hardware Address Modifier Mask:')
        Label_SrcHardwareAddrModifierMask.grid(row=14, column=0)
        Entry_SrcHardwareAddrModifierMask = Entry(root42)
        Entry_SrcHardwareAddrModifierMask.grid(row=14, column=1)
        Entry_SrcHardwareAddrModifierMask.delete(0, "end")
        Entry_SrcHardwareAddrModifierMask.insert(0, "00:0:FF:FF:FF:FF")

        Label_DestHardwareAddr = Label(root42, text='Target Hardware Address:')
        Label_DestHardwareAddr.grid(row=15, column=0)
        Entry_DestHardwareAddr = Entry(root42)
        Entry_DestHardwareAddr.grid(row=15, column=1)
        Entry_DestHardwareAddr.delete(0, "end")
        Entry_DestHardwareAddr.insert(0, "94:29:2F:02:00:0A")

        Label_DestHardwareAddrIsModifier = Label(root42, text='Target Hardware Address是否可变:')
        Label_DestHardwareAddrIsModifier.grid(row=16, column=0)
        DestHardwareAddrIsModifierVar = StringVar()
        Combobox_DestHardwareAddrIsModifier = Combobox(root42, textvariable=DestHardwareAddrIsModifierVar)
        Combobox_DestHardwareAddrIsModifier["value"] = EnableList
        Combobox_DestHardwareAddrIsModifier.grid(row=16, column=1)
        Label_DestHardwareAddrModifierCount = Label(root42, text='Target Hardware Address Modifier Count:')
        Label_DestHardwareAddrModifierCount.grid(row=17, column=0)
        Entry_DestHardwareAddrModifierCount = Entry(root42)
        Entry_DestHardwareAddrModifierCount.grid(row=17, column=1)
        Entry_DestHardwareAddrModifierCount.delete(0, "end")
        Entry_DestHardwareAddrModifierCount.insert(0, "1")
        Label_DestHardwareAddrModifierStep = Label(root42, text='Target Hardware Address Modifier Step:')
        Label_DestHardwareAddrModifierStep.grid(row=18, column=0)
        Entry_DestHardwareAddrModifierStep = Entry(root42)
        Entry_DestHardwareAddrModifierStep.grid(row=18, column=1)
        Entry_DestHardwareAddrModifierStep.delete(0, "end")
        Entry_DestHardwareAddrModifierStep.insert(0, "00:00:00:00:00:01")
        Label_DestHardwareAddrModifierMask = Label(root42, text='Target Hardware Address Modifier Mask:')
        Label_DestHardwareAddrModifierMask.grid(row=19, column=0)
        Entry_DestHardwareAddrModifierMask = Entry(root42)
        Entry_DestHardwareAddrModifierMask.grid(row=19, column=1)
        Entry_DestHardwareAddrModifierMask.delete(0, "end")
        Entry_DestHardwareAddrModifierMask.insert(0, "00:0:FF:FF:FF:FF")

        Label_SrcIPv4Addr = Label(root42, text='Sender Protocol Address:')
        Label_SrcIPv4Addr.grid(row=20, column=0)
        Entry_SrcIPv4Addr = Entry(root42)
        Entry_SrcIPv4Addr.grid(row=20, column=1)
        Entry_SrcIPv4Addr.delete(0, "end")
        Entry_SrcIPv4Addr.insert(0, "1.1.1.1")

        Label_SrcIPv4AddrIsModifier = Label(root42, text='Sender Protocol Address是否可变:')
        Label_SrcIPv4AddrIsModifier.grid(row=21, column=0)
        EnableList = [True, False]
        SrcIPv4AddrIsModifierVar = StringVar()
        Combobox_SrcIPv4AddrIsModifier = Combobox(root42, textvariable=SrcIPv4AddrIsModifierVar)
        Combobox_SrcIPv4AddrIsModifier["value"] = EnableList
        Combobox_SrcIPv4AddrIsModifier.grid(row=21, column=1)
        Label_SrcIPv4AddrModifierCount = Label(root42, text='Sender Protocol Address Modifier Count:')
        Label_SrcIPv4AddrModifierCount.grid(row=22, column=0)
        Entry_SrcIPv4AddrModifierCount = Entry(root42)
        Entry_SrcIPv4AddrModifierCount.grid(row=22, column=1)
        Entry_SrcIPv4AddrModifierCount.delete(0, "end")
        Entry_SrcIPv4AddrModifierCount.insert(0, "1")
        Label_SrcIPv4AddrModifierStep = Label(root42, text='Sender Protocol Address Modifier Step:')
        Label_SrcIPv4AddrModifierStep.grid(row=23, column=0)
        Entry_SrcIPv4AddrModifierStep = Entry(root42)
        Entry_SrcIPv4AddrModifierStep.grid(row=23, column=1)
        Entry_SrcIPv4AddrModifierStep.delete(0, "end")
        Entry_SrcIPv4AddrModifierStep.insert(0, "0.0.0.1")
        Label_SrcIPv4AddrModifierMask = Label(root42, text='Sender Protocol Address Modifier Mask:')
        Label_SrcIPv4AddrModifierMask.grid(row=24, column=0)
        Entry_SrcIPv4AddrModifierMask = Entry(root42)
        Entry_SrcIPv4AddrModifierMask.grid(row=24, column=1)
        Entry_SrcIPv4AddrModifierMask.delete(0, "end")
        Entry_SrcIPv4AddrModifierMask.insert(0, "255.255.255.255")

        Label_DestIPv4Addr = Label(root42, text='Target Protocol Address:')
        Label_DestIPv4Addr.grid(row=25, column=0)
        Entry_DestIPv4Addr = Entry(root42)
        Entry_DestIPv4Addr.grid(row=25, column=1)
        Entry_DestIPv4Addr.delete(0, "end")
        Entry_DestIPv4Addr.insert(0, "2.2.2.2")

        Label_DestIPv4AddrIsModifier = Label(root42, text='Target Protocol Address是否可变:')
        Label_DestIPv4AddrIsModifier.grid(row=26, column=0)
        DestIPv4AddrIsModifierVar = StringVar()
        Combobox_DestIPv4AddrIsModifier = Combobox(root42, textvariable=DestIPv4AddrIsModifierVar)
        Combobox_DestIPv4AddrIsModifier["value"] = EnableList
        Combobox_DestIPv4AddrIsModifier.grid(row=26, column=1)
        Label_DestIPv4AddrModifierCount = Label(root42, text='Target Protocol Address Modifier Count:')
        Label_DestIPv4AddrModifierCount.grid(row=27, column=0)
        Entry_DestIPv4AddrModifierCount = Entry(root42)
        Entry_DestIPv4AddrModifierCount.grid(row=27, column=1)
        Entry_DestIPv4AddrModifierCount.delete(0, "end")
        Entry_DestIPv4AddrModifierCount.insert(0, "1")
        Label_DestIPv4AddrModifierStep = Label(root42, text='Target Protocol Address Modifier Step:')
        Label_DestIPv4AddrModifierStep.grid(row=28, column=0)
        Entry_DestIPv4AddrModifierStep = Entry(root42)
        Entry_DestIPv4AddrModifierStep.grid(row=28, column=1)
        Entry_DestIPv4AddrModifierStep.delete(0, "end")
        Entry_DestIPv4AddrModifierStep.insert(0, "0.0.0.1")
        Label_DestIPv4AddrModifierMask = Label(root42, text='Target Protocol Address Modifier Mask:')
        Label_DestIPv4AddrModifierMask.grid(row=29, column=0)
        Entry_DestIPv4AddrModifierMask = Entry(root42)
        Entry_DestIPv4AddrModifierMask.grid(row=29, column=1)
        Entry_DestIPv4AddrModifierMask.delete(0, "end")
        Entry_DestIPv4AddrModifierMask.insert(0, "255.255.255.255")

        button_createARPPkt = Button(root42, text='创建ARP流量', command=button_StreamCreate_ARP_Custom)
        button_createARPPkt.grid(row=30, column=0)

        root42.title("TestMaster ARP Custom流量创建")
        root42.geometry('800x750')

        root42.mainloop()

    def button_StreamCreate_IPv4_Custom(self):

        def button_StreamCreate_IPv4_Custom():

            if Combobox_GetInfoPort.get() == '':
                messagebox.showinfo("创建流量失败", "未选择创建流量所属接口，请选择接口重试")
            else:
                # 写脚本文件
                tmtcltime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                tmtcl = '\n#create Ethernet custom Stream '
                # 先删除测试仪的流
                tmtcl = tmtcl + '\n#先删除测试仪的流' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream'
                if ckVlan_var.get() == "Y":

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' ETH_SetVlanPkt ' + Entry_FrameLength.get() + ' ' + Entry_VlanID.get() + ' ' + Entry_SrcMacAddr.get() + ' ' + Entry_DestMacAddr.get() + ' ' + Entry_SrcIPv4Addr.get() + ' ' + Entry_DestIPv4Addr.get()

                    if Combobox_SrcIPv4AddrIsModifier.get():
                       tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 32 -Offset 30 -DataCount ' + Entry_SrcIPv4AddrModifierCount.get() + ' -Step ' + Entry_SrcIPv4AddrModifierStep.get()
                    if Combobox_DestIPv4AddrIsModifier.get():
                       tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 32 -Offset 34 -DataCount ' + Entry_DestIPv4AddrModifierCount.get() + ' -Step ' + Entry_DestIPv4AddrModifierStep.get()
                else:

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetEthIIPkt ' + Entry_FrameLength.get() + ' ' + Entry_SrcMacAddr.get() + ' ' + Entry_DestMacAddr.get() + ' ' + Entry_SrcIPv4Addr.get() + ' ' + Entry_DestIPv4Addr.get()
                    if Combobox_SrcIPv4AddrIsModifier.get():
                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 32 -Offset 26 -DataCount ' + Entry_SrcIPv4AddrModifierCount.get() + ' -Step ' + Entry_SrcIPv4AddrModifierStep.get()
                    if Combobox_DestIPv4AddrIsModifier.get():
                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 32 -Offset 30 -DataCount ' + Entry_DestIPv4AddrModifierCount.get() + ' -Step ' + Entry_DestIPv4AddrModifierStep.get()
                tmtcldict = {
                    "time": tmtcltime,
                    "tcl": tmtcl
                }
                print(tmtcldict)
                return tmtcldict


        root44 = Tk()
        reservedPortDict = {}
        intf_jsonfile = Path(self.JSON_DIR) / 'intf_reserved.json'
        with open(intf_jsonfile, 'r') as f:
            intf_json_data = f.read()
            reservedPortDict = json.loads(intf_json_data)
        reservedPortList = []
        reservedPortList = list(reservedPortDict.keys())
        Label_Separat1 = Label(root44, text='----------公共配置--------------')
        Label_Separat1.grid(row=0)
        Label_OperatePort = Label(root44, text='选择创建流量所属接口')
        Label_OperatePort.grid(row=1, column=0)

        Combobox_GetInfoPort = Combobox(root44)
        Combobox_GetInfoPort["value"] = reservedPortList
        Combobox_GetInfoPort.grid(row=1, column=1)
        Label_OperateRcvPort = Label(root44, text='选择流量接收接口，不选择为Any')
        Label_OperateRcvPort.grid(row=1, column=2)

        Combobox_GetInfoRcvPort = Combobox(root44)
        Combobox_GetInfoRcvPort["value"] = reservedPortList
        Combobox_GetInfoRcvPort.grid(row=1, column=3)
        Label_DurationMode = Label(root44, text='端口流量发送Duration模式:')
        Label_DurationMode.grid(row=2, column=0)
        DurationModeList = ["Continuous", "Bursts"]
        DurationModeVar = StringVar()
        Combobox_DurationMode = Combobox(root44, textvariable=DurationModeVar)
        Combobox_DurationMode["value"] = DurationModeList
        Combobox_DurationMode.grid(row=2, column=1)
        Label_FrameLength = Label(root44, text='流量包长:')
        Label_FrameLength.grid(row=3, column=0)
        Entry_FrameLength = Entry(root44)
        Entry_FrameLength.grid(row=3, column=1)
        Entry_FrameLength.delete(0, "end")
        Entry_FrameLength.insert(0, "128")
        Label_LoadUnit = Label(root44, text='Load单位类型:')
        Label_LoadUnit.grid(row=4, column=0)
        LoadUnitList = ["percent", "fps", "bps", "kbps", "mbps"]
        LoadUnitVar = StringVar()
        Combobox_LoadMode = Combobox(root44, textvariable=LoadUnitVar)
        Combobox_LoadMode["value"] = LoadUnitList
        Combobox_LoadMode.grid(row=4, column=1)
        Label_Load = Label(root44, text='Load:')
        Label_Load.grid(row=4, column=2)
        Entry_Load = Entry(root44)
        Entry_Load.grid(row=4, column=3)
        Entry_Load.delete(0, "end")
        Entry_Load.insert(0, "10")

        # Label_Vlan = Label(root44, text='Vlan Encap Info:')
        # Label_Vlan.grid(row=5, column=0)
        # ckVlan_var = IntVar()
        # ckVlan = Checkbutton(root44, text='设备是否需要Vlan封装', variable=ckVlan_var)
        # ckVlan.grid(row=5, column=1)

        Label_Vlan = Label(root44, text='设备是否需要Vlan封装:')
        Label_Vlan.grid(row=5, column=0)
        ckVlan_var = Combobox(root44)
        ckVlan_var["value"] = ["Y","N"]
        ckVlan_var.grid(row=5, column=1)
        ckVlan_var.delete(0, "end")
        ckVlan_var.insert(0, "Y")

        Label_VlanID = Label(root44, text='Vlan ID:')
        Label_VlanID.grid(row=5, column=2)
        Entry_VlanID = Entry(root44)
        Entry_VlanID.grid(row=5, column=3)
        Entry_VlanID.delete(0, "end")
        Entry_VlanID.insert(0, "1")
        Label_Separat2 = Label(root44, text='----------IPv4 custom stream参数--------------')
        Label_Separat2.grid(row=6, column=0)
        Label_SrcMacAddr = Label(root44, text='Src Mac Address:')
        Label_SrcMacAddr.grid(row=7, column=0)
        Entry_SrcMacAddr = Entry(root44)
        Entry_SrcMacAddr.grid(row=7, column=1)
        Entry_SrcMacAddr.delete(0, "end")
        Entry_SrcMacAddr.insert(0, "94:29:2F:01:00:0A")

        Label_DestMacAddr = Label(root44, text='Dest Mac Address:')
        Label_DestMacAddr.grid(row=8, column=0)
        Entry_DestMacAddr = Entry(root44)
        Entry_DestMacAddr.grid(row=8, column=1)
        Entry_DestMacAddr.delete(0, "end")
        Entry_DestMacAddr.insert(0, "94:29:2F:02:00:0A")

        Label_SrcIPv4Addr = Label(root44, text='Src IPv4 Address:')
        Label_SrcIPv4Addr.grid(row=9, column=0)
        Entry_SrcIPv4Addr = Entry(root44)
        Entry_SrcIPv4Addr.grid(row=9, column=1)
        Entry_SrcIPv4Addr.delete(0, "end")
        Entry_SrcIPv4Addr.insert(0, "1.1.1.1")

        Label_SrcIPv4AddrIsModifier = Label(root44, text='Src IPv4 Address是否可变:')
        Label_SrcIPv4AddrIsModifier.grid(row=10, column=0)
        EnableList = [True, False]

        Combobox_SrcIPv4AddrIsModifier = Combobox(root44)
        Combobox_SrcIPv4AddrIsModifier["value"] = EnableList
        Combobox_SrcIPv4AddrIsModifier.grid(row=10, column=1)
        Label_SrcIPv4AddrModifierCount = Label(root44, text='Src IPv4 Address Modifier Count:')
        Label_SrcIPv4AddrModifierCount.grid(row=11, column=0)
        Entry_SrcIPv4AddrModifierCount = Entry(root44)
        Entry_SrcIPv4AddrModifierCount.grid(row=11, column=1)
        Entry_SrcIPv4AddrModifierCount.delete(0, "end")
        Entry_SrcIPv4AddrModifierCount.insert(0, "1")
        Label_SrcIPv4AddrModifierStep = Label(root44, text='Src IPv4 Address Modifier Step:')
        Label_SrcIPv4AddrModifierStep.grid(row=12, column=0)
        Entry_SrcIPv4AddrModifierStep = Entry(root44)
        Entry_SrcIPv4AddrModifierStep.grid(row=12, column=1)
        Entry_SrcIPv4AddrModifierStep.delete(0, "end")
        Entry_SrcIPv4AddrModifierStep.insert(0, "0.0.0.1")
        Label_SrcIPv4AddrModifierMask = Label(root44, text='Src IPv4 Address Modifier Mask:')
        Label_SrcIPv4AddrModifierMask.grid(row=13, column=0)
        Entry_SrcIPv4AddrModifierMask = Entry(root44)
        Entry_SrcIPv4AddrModifierMask.grid(row=13, column=1)
        Entry_SrcIPv4AddrModifierMask.delete(0, "end")
        Entry_SrcIPv4AddrModifierMask.insert(0, "255.255.255.255")

        Label_DestIPv4Addr = Label(root44, text='Dest IPv4 Address:')
        Label_DestIPv4Addr.grid(row=14, column=0)
        Entry_DestIPv4Addr = Entry(root44)
        Entry_DestIPv4Addr.grid(row=14, column=1)
        Entry_DestIPv4Addr.delete(0, "end")
        Entry_DestIPv4Addr.insert(0, "2.2.2.2")

        Label_DestIPv4AddrIsModifier = Label(root44, text='Dest IPv4 Address是否可变:')
        Label_DestIPv4AddrIsModifier.grid(row=15, column=0)

        Combobox_DestIPv4AddrIsModifier = Combobox(root44)
        Combobox_DestIPv4AddrIsModifier["value"] = EnableList
        Combobox_DestIPv4AddrIsModifier.grid(row=15, column=1)
        Label_DestIPv4AddrModifierCount = Label(root44, text='Dest IPv4 Address Modifier Count:')
        Label_DestIPv4AddrModifierCount.grid(row=16, column=0)
        Entry_DestIPv4AddrModifierCount = Entry(root44)
        Entry_DestIPv4AddrModifierCount.grid(row=16, column=1)
        Entry_DestIPv4AddrModifierCount.delete(0, "end")
        Entry_DestIPv4AddrModifierCount.insert(0, "1")
        Label_DestIPv4AddrModifierStep = Label(root44, text='Dest IPv4 Address Modifier Step:')
        Label_DestIPv4AddrModifierStep.grid(row=17, column=0)
        Entry_DestIPv4AddrModifierStep = Entry(root44)
        Entry_DestIPv4AddrModifierStep.grid(row=17, column=1)
        Entry_DestIPv4AddrModifierStep.delete(0, "end")
        Entry_DestIPv4AddrModifierStep.insert(0, "0.0.0.1")
        Label_DestIPv4AddrModifierMask = Label(root44, text='Dest IPv4 Address Modifier Mask:')
        Label_DestIPv4AddrModifierMask.grid(row=18, column=0)
        Entry_DestIPv4AddrModifierMask = Entry(root44)
        Entry_DestIPv4AddrModifierMask.grid(row=18, column=1)
        Entry_DestIPv4AddrModifierMask.delete(0, "end")
        Entry_DestIPv4AddrModifierMask.insert(0, "255.255.255.255")

        Label_DestIPv4AddrGateway = Label(root44, text='Dest IPv4 Address Gateway:')
        Label_DestIPv4AddrGateway.grid(row=19, column=0)
        Entry_DestIPv4Gateway = Entry(root44)
        Entry_DestIPv4Gateway.grid(row=19, column=1)
        Entry_DestIPv4Gateway.delete(0, "end")
        Entry_DestIPv4Gateway.insert(0, "2.2.2.2")

        button_createIPv4Pkt = Button(root44, text='创建IPv4流量', command=button_StreamCreate_IPv4_Custom)
        button_createIPv4Pkt.grid(row=20, column=0)

        root44.title("TestMaster IPv4 Custom流量创建")
        root44.geometry('800x600')

        root44.mainloop()

    def button_StreamCreate_IPv6_Custom(self):

        def button_StreamCreate_IPv6_Custom():

            if Combobox_GetInfoPort.get() == '':
                messagebox.showinfo("创建流量失败", "未选择创建流量所属接口，请选择接口重试")
            else:
                # 写脚本文件
                tmtcltime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                tmtcl = '\n#create IPv6 custom Stream '

                # 先删除测试仪的流
                tmtcl = tmtcl + '\n#先删除测试仪的流' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream'
                if ckVlan_var.get() == "Y":
                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' CreateIPv6Stream -FrameLen  ' + Entry_FrameLength.get() + ' -Utilization ' + Entry_Load.get() + ' -TxMode $::L3_CONTINUOUS_MODE -VlanID ' + Entry_VlanID.get() + ' -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -SrcIP ' + Entry_SrcIPv6Addr.get() + ' -DesIP ' + Entry_DestIPv6Addr.get()
                    if Combobox_SrcIPv6AddrIsModifier.get():
                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 32 -Offset 26 -DataCount ' + Entry_SrcIPv6AddrModifierCount.get() + ' -Step ' + Entry_SrcIPv6AddrModifierStep.get()
                    if Combobox_DestIPv6AddrIsModifier.get():
                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 32 -Offset 42 -DataCount ' + Entry_DestIPv6AddrModifierCount.get() + ' -Step ' + Entry_DestIPv6AddrModifierStep.get()
                else:
                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' CreateIPv6Stream -FrameLen  ' + Entry_FrameLength.get() + ' -Utilization ' + Entry_Load.get() + ' -TxMode $::L3_CONTINUOUS_MODE -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -SrcIP ' + Entry_SrcIPv6Addr.get() + ' -DesIP ' + Entry_DestIPv6Addr.get()
                    if Combobox_SrcIPv6AddrIsModifier.get():
                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 32 -Offset 22 -DataCount ' + Entry_SrcIPv6AddrModifierCount.get() + ' -Step ' + Entry_SrcIPv6AddrModifierStep.get()
                    if Combobox_DestIPv6AddrIsModifier.get():
                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 32 -Offset 38 -DataCount ' + Entry_DestIPv6AddrModifierCount.get() + ' -Step ' + Entry_DestIPv6AddrModifierStep.get()

                tmtcldict = {
                    "time": tmtcltime,
                    "tcl": tmtcl
                }
                print(tmtcldict)
                return tmtcldict

        root45 = Tk()
        reservedPortDict = {}
        intf_jsonfile = Path(self.JSON_DIR) / 'intf_reserved.json'
        with open(intf_jsonfile, 'r') as f:
            intf_json_data = f.read()
            reservedPortDict = json.loads(intf_json_data)
        reservedPortList = []
        reservedPortList = list(reservedPortDict.keys())
        Label_Separat1 = Label(root45, text='----------公共配置--------------')
        Label_Separat1.grid(row=0)
        Label_OperatePort = Label(root45, text='选择创建流量所属接口')
        Label_OperatePort.grid(row=1, column=0)

        Combobox_GetInfoPort = Combobox(root45)
        Combobox_GetInfoPort["value"] = reservedPortList
        Combobox_GetInfoPort.grid(row=1, column=1)
        Label_OperateRcvPort = Label(root45, text='选择流量接收接口，不选择为Any')
        Label_OperateRcvPort.grid(row=1, column=2)
        portVar_getInfoRcv = StringVar()
        Combobox_GetInfoRcvPort = Combobox(root45, textvariable=portVar_getInfoRcv)
        Combobox_GetInfoRcvPort["value"] = reservedPortList
        Combobox_GetInfoRcvPort.grid(row=1, column=3)
        Label_DurationMode = Label(root45, text='端口流量发送Duration模式:')
        Label_DurationMode.grid(row=2, column=0)
        DurationModeList = ["Continuous", "Bursts"]
        DurationModeVar = StringVar()
        Combobox_DurationMode = Combobox(root45, textvariable=DurationModeVar)
        Combobox_DurationMode["value"] = DurationModeList
        Combobox_DurationMode.grid(row=2, column=1)
        Label_FrameLength = Label(root45, text='流量包长:')
        Label_FrameLength.grid(row=3, column=0)
        Entry_FrameLength = Entry(root45)
        Entry_FrameLength.grid(row=3, column=1)
        Entry_FrameLength.delete(0, "end")
        Entry_FrameLength.insert(0, "128")
        Label_LoadUnit = Label(root45, text='Load单位类型:')
        Label_LoadUnit.grid(row=4, column=0)
        LoadUnitList = ["percent", "fps", "bps", "kbps", "mbps"]
        LoadUnitVar = StringVar()
        Combobox_LoadMode = Combobox(root45, textvariable=LoadUnitVar)
        Combobox_LoadMode["value"] = LoadUnitList
        Combobox_LoadMode.grid(row=4, column=1)
        Label_Load = Label(root45, text='Load:')
        Label_Load.grid(row=4, column=2)
        Entry_Load = Entry(root45)
        Entry_Load.grid(row=4, column=3)
        Entry_Load.delete(0, "end")
        Entry_Load.insert(0, "10")

        # Label_Vlan = Label(root45, text='Vlan Encap Info:')
        # Label_Vlan.grid(row=5, column=0)
        # ckVlan_var = IntVar()
        # ckVlan = Checkbutton(root45, text='设备是否需要Vlan封装', variable=ckVlan_var)
        # ckVlan.grid(row=5, column=1)

        Label_Vlan = Label(root45, text='设备是否需要Vlan封装:')
        Label_Vlan.grid(row=5, column=0)
        ckVlan_var = Combobox(root45)
        ckVlan_var["value"] = ["Y","N"]
        ckVlan_var.grid(row=5, column=1)
        ckVlan_var.delete(0, "end")
        ckVlan_var.insert(0, "Y")

        Label_VlanID = Label(root45, text='Vlan ID:')
        Label_VlanID.grid(row=5, column=2)
        Entry_VlanID = Entry(root45)
        Entry_VlanID.grid(row=5, column=3)
        Entry_VlanID.delete(0, "end")
        Entry_VlanID.insert(0, "1")
        Label_Separat2 = Label(root45, text='----------IPv6 custom stream参数--------------')
        Label_Separat2.grid(row=6, column=0)
        Label_SrcMacAddr = Label(root45, text='Src Mac Address:')
        Label_SrcMacAddr.grid(row=7, column=0)
        Entry_SrcMacAddr = Entry(root45)
        Entry_SrcMacAddr.grid(row=7, column=1)
        Entry_SrcMacAddr.delete(0, "end")
        Entry_SrcMacAddr.insert(0, "94:29:2F:01:00:0A")

        Label_DestMacAddr = Label(root45, text='Dest Mac Address:')
        Label_DestMacAddr.grid(row=8, column=0)
        Entry_DestMacAddr = Entry(root45)
        Entry_DestMacAddr.grid(row=8, column=1)
        Entry_DestMacAddr.delete(0, "end")
        Entry_DestMacAddr.insert(0, "94:29:2F:02:00:0A")

        Label_SrcIPv6Addr = Label(root45, text='Src IPv6 Address:')
        Label_SrcIPv6Addr.grid(row=9, column=0)
        Entry_SrcIPv6Addr = Entry(root45)
        Entry_SrcIPv6Addr.grid(row=9, column=1)
        Entry_SrcIPv6Addr.delete(0, "end")
        Entry_SrcIPv6Addr.insert(0, "2000::2")

        Label_SrcIPv6AddrIsModifier = Label(root45, text='Src IPv6 Address是否可变:')
        Label_SrcIPv6AddrIsModifier.grid(row=10, column=0)
        EnableList = [True, False]

        Combobox_SrcIPv6AddrIsModifier = Combobox(root45)
        Combobox_SrcIPv6AddrIsModifier["value"] = EnableList
        Combobox_SrcIPv6AddrIsModifier.grid(row=10, column=1)
        Label_SrcIPv6AddrModifierCount = Label(root45, text='Src IPv6 Address Modifier Count:')
        Label_SrcIPv6AddrModifierCount.grid(row=11, column=0)
        Entry_SrcIPv6AddrModifierCount = Entry(root45)
        Entry_SrcIPv6AddrModifierCount.grid(row=11, column=1)
        Entry_SrcIPv6AddrModifierCount.delete(0, "end")
        Entry_SrcIPv6AddrModifierCount.insert(0, "1")
        Label_SrcIPv6AddrModifierStep = Label(root45, text='Src IPv6 Address Modifier Step:')
        Label_SrcIPv6AddrModifierStep.grid(row=12, column=0)
        Entry_SrcIPv6AddrModifierStep = Entry(root45)
        Entry_SrcIPv6AddrModifierStep.grid(row=12, column=1)
        Entry_SrcIPv6AddrModifierStep.delete(0, "end")
        Entry_SrcIPv6AddrModifierStep.insert(0, "::1")
        Label_SrcIPv6AddrModifierMask = Label(root45, text='Src IPv6 Address Modifier Mask:')
        Label_SrcIPv6AddrModifierMask.grid(row=13, column=0)
        Entry_SrcIPv6AddrModifierMask = Entry(root45)
        Entry_SrcIPv6AddrModifierMask.grid(row=13, column=1)
        Entry_SrcIPv6AddrModifierMask.delete(0, "end")
        Entry_SrcIPv6AddrModifierMask.insert(0, "::FFFF:FFFF")

        Label_DestIPv6Addr = Label(root45, text='Dest IPv6 Address:')
        Label_DestIPv6Addr.grid(row=14, column=0)
        Entry_DestIPv6Addr = Entry(root45)
        Entry_DestIPv6Addr.grid(row=14, column=1)
        Entry_DestIPv6Addr.delete(0, "end")
        Entry_DestIPv6Addr.insert(0, "2000::1")

        Label_DestIPv6AddrIsModifier = Label(root45, text='Dest IPv6 Address是否可变:')
        Label_DestIPv6AddrIsModifier.grid(row=15, column=0)

        Combobox_DestIPv6AddrIsModifier = Combobox(root45)
        Combobox_DestIPv6AddrIsModifier["value"] = EnableList
        Combobox_DestIPv6AddrIsModifier.grid(row=15, column=1)
        Label_DestIPv6AddrModifierCount = Label(root45, text='Dest IPv6 Address Modifier Count:')
        Label_DestIPv6AddrModifierCount.grid(row=16, column=0)
        Entry_DestIPv6AddrModifierCount = Entry(root45)
        Entry_DestIPv6AddrModifierCount.grid(row=16, column=1)
        Entry_DestIPv6AddrModifierCount.delete(0, "end")
        Entry_DestIPv6AddrModifierCount.insert(0, "1")
        Label_DestIPv6AddrModifierStep = Label(root45, text='Dest IPv6 Address Modifier Step:')
        Label_DestIPv6AddrModifierStep.grid(row=17, column=0)
        Entry_DestIPv6AddrModifierStep = Entry(root45)
        Entry_DestIPv6AddrModifierStep.grid(row=17, column=1)
        Entry_DestIPv6AddrModifierStep.delete(0, "end")
        Entry_DestIPv6AddrModifierStep.insert(0, "::1")
        Label_DestIPv6AddrModifierMask = Label(root45, text='Dest IPv6 Address Modifier Mask:')
        Label_DestIPv6AddrModifierMask.grid(row=18, column=0)
        Entry_DestIPv6AddrModifierMask = Entry(root45)
        Entry_DestIPv6AddrModifierMask.grid(row=18, column=1)
        Entry_DestIPv6AddrModifierMask.delete(0, "end")
        Entry_DestIPv6AddrModifierMask.insert(0, "::FFFF:FFFF")

        Label_DestIPv6AddrGateway = Label(root45, text='Dest IPv6 Address Gateway:')
        Label_DestIPv6AddrGateway.grid(row=19, column=0)
        Entry_DestIPv6Gateway = Entry(root45)
        Entry_DestIPv6Gateway.grid(row=19, column=1)
        Entry_DestIPv6Gateway.delete(0, "end")
        Entry_DestIPv6Gateway.insert(0, "2000::1")

        button_createIPv6Pkt = Button(root45, text='创建IPv6流量', command=button_StreamCreate_IPv6_Custom)
        button_createIPv6Pkt.grid(row=20, column=0)

        root45.title("TestMaster IPv6 Custom流量创建")
        root45.geometry('800x600')

        root45.mainloop()

    def button_StreamCreate_MPLS(self):

        def button_StreamCreate_MPLS_Custom():

            if Combobox_GetInfoPort.get() == '':
                messagebox.showinfo("创建流量失败", "未选择创建流量所属接口，请选择接口重试")
            else:
                # 写脚本文件
                tmtcltime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                tmtcl = '\n#create MPLS custom Stream '
                # 先删除测试仪的流
                tmtcl = tmtcl + '\n#先删除测试仪的流' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream'
                if ckVlan_var.get() == "Y":

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetMplsPkt -PacketLen' + Entry_FrameLength.get() + ' -VlanID ' + Entry_VlanID.get() + ' -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -Label ' + Entry_MPLSLabel.get() + ' -SrcIp ' + Entry_SrcIPv4Addr.get() + ' -DesIp ' + Entry_DestIPv4Addr.get()
                else:

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetMplsPkt -PacketLen' + Entry_FrameLength.get() + ' -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -Label ' + Entry_MPLSLabel.get() + ' -SrcIp ' + Entry_SrcIPv4Addr.get() + ' -DesIp ' + Entry_DestIPv4Addr.get()
                if Combobox_MPLSLabelIsModifier.get():

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 16 -Offset 18 -DataCount ' + Entry_MPLSLabelModifierCount.get() + ' -Step ' + Entry_MPLSLabelModifierStep.get()

                tmtcldict = {
                "time": tmtcltime,
                "tcl": tmtcl
                }
                print(tmtcldict)
                return tmtcldict

        root43 = Tk()
        reservedPortDict = {}
        intf_jsonfile = Path(self.JSON_DIR) / 'intf_reserved.json'
        with open(intf_jsonfile, 'r') as f:
            intf_json_data = f.read()
            reservedPortDict = json.loads(intf_json_data)
        reservedPortList = []
        reservedPortList = list(reservedPortDict.keys())
        Label_Separat1 = Label(root43, text='----------公共配置--------------')
        Label_Separat1.grid(row=0)
        Label_OperatePort = Label(root43, text='选择创建流量所属接口')
        Label_OperatePort.grid(row=1, column=0)

        Combobox_GetInfoPort = Combobox(root43)
        Combobox_GetInfoPort["value"] = reservedPortList
        Combobox_GetInfoPort.grid(row=1, column=1)
        Label_OperateRcvPort = Label(root43, text='选择流量接收接口，不选择为Any')
        Label_OperateRcvPort.grid(row=1, column=2)
        portVar_getInfoRcv = StringVar()
        Combobox_GetInfoRcvPort = Combobox(root43, textvariable=portVar_getInfoRcv)
        Combobox_GetInfoRcvPort["value"] = reservedPortList
        Combobox_GetInfoRcvPort.grid(row=1, column=3)
        Label_DurationMode = Label(root43, text='端口流量发送Duration模式:')
        Label_DurationMode.grid(row=2, column=0)
        DurationModeList = ["Continuous", "Bursts"]
        DurationModeVar = StringVar()
        Combobox_DurationMode = Combobox(root43, textvariable=DurationModeVar)
        Combobox_DurationMode["value"] = DurationModeList
        Combobox_DurationMode.grid(row=2, column=1)
        Label_FrameLength = Label(root43, text='流量包长:')
        Label_FrameLength.grid(row=3, column=0)
        Entry_FrameLength = Entry(root43)
        Entry_FrameLength.grid(row=3, column=1)
        Entry_FrameLength.delete(0, "end")
        Entry_FrameLength.insert(0, "128")
        Label_LoadUnit = Label(root43, text='Load单位类型:')
        Label_LoadUnit.grid(row=4, column=0)
        LoadUnitList = ["percent", "fps", "bps", "kbps", "mbps"]
        LoadUnitVar = StringVar()
        Combobox_LoadMode = Combobox(root43, textvariable=LoadUnitVar)
        Combobox_LoadMode["value"] = LoadUnitList
        Combobox_LoadMode.grid(row=4, column=1)
        Label_Load = Label(root43, text='Load:')
        Label_Load.grid(row=4, column=2)
        Entry_Load = Entry(root43)
        Entry_Load.grid(row=4, column=3)
        Entry_Load.delete(0, "end")
        Entry_Load.insert(0, "10")

        # Label_Vlan = Label(root43, text='Vlan Encap Info:')
        # Label_Vlan.grid(row=5, column=0)
        # ckVlan_var = IntVar()
        # ckVlan = Checkbutton(root43, text='设备是否需要Vlan封装', variable=ckVlan_var)
        # ckVlan.grid(row=5, column=1)

        Label_Vlan = Label(root43, text='设备是否需要Vlan封装:')
        Label_Vlan.grid(row=5, column=0)
        ckVlan_var = Combobox(root43)
        ckVlan_var["value"] = ["Y","N"]
        ckVlan_var.grid(row=5, column=1)
        ckVlan_var.delete(0, "end")
        ckVlan_var.insert(0, "Y")

        Label_VlanID = Label(root43, text='Vlan ID:')
        Label_VlanID.grid(row=5, column=2)
        Entry_VlanID = Entry(root43)
        Entry_VlanID.grid(row=5, column=3)
        Entry_VlanID.delete(0, "end")
        Entry_VlanID.insert(0, "1")
        Label_Separat2 = Label(root43, text='----------MPLS custom stream参数--------------')
        Label_Separat2.grid(row=6, column=0)
        Label_SrcMacAddr = Label(root43, text='Src Mac Address:')
        Label_SrcMacAddr.grid(row=7, column=0)
        Entry_SrcMacAddr = Entry(root43)
        Entry_SrcMacAddr.grid(row=7, column=1)
        Entry_SrcMacAddr.delete(0, "end")
        Entry_SrcMacAddr.insert(0, "94:29:2F:01:00:0A")

        Label_DestMacAddr = Label(root43, text='Dest Mac Address:')
        Label_DestMacAddr.grid(row=8, column=0)
        Entry_DestMacAddr = Entry(root43)
        Entry_DestMacAddr.grid(row=8, column=1)
        Entry_DestMacAddr.delete(0, "end")
        Entry_DestMacAddr.insert(0, "94:29:2F:02:00:0A")

        Label_MPLSLabel = Label(root43, text='MPLS Label:')
        Label_MPLSLabel.grid(row=9, column=0)
        Entry_MPLSLabel = Entry(root43)
        Entry_MPLSLabel.grid(row=9, column=1)
        Entry_MPLSLabel.delete(0, "end")
        Entry_MPLSLabel.insert(0, "1024")

        Label_MPLSLabelIsModifier = Label(root43, text='MPLS Label是否可变:')
        Label_MPLSLabelIsModifier.grid(row=13, column=0)
        EnableList = [True, False]

        Combobox_MPLSLabelIsModifier = Combobox(root43)
        Combobox_MPLSLabelIsModifier["value"] = EnableList
        Combobox_MPLSLabelIsModifier.grid(row=13, column=1)
        Label_MPLSLabelModifierCount = Label(root43, text='MPLS Label Modifier Count:')
        Label_MPLSLabelModifierCount.grid(row=14, column=0)
        Entry_MPLSLabelModifierCount = Entry(root43)
        Entry_MPLSLabelModifierCount.grid(row=14, column=1)
        Entry_MPLSLabelModifierCount.delete(0, "end")
        Entry_MPLSLabelModifierCount.insert(0, "1")
        Label_MPLSLabelModifierStep = Label(root43, text='MPLS Label Modifier Step:')
        Label_MPLSLabelModifierStep.grid(row=15, column=0)
        Entry_MPLSLabelModifierStep = Entry(root43)
        Entry_MPLSLabelModifierStep.grid(row=15, column=1)
        Entry_MPLSLabelModifierStep.delete(0, "end")
        Entry_MPLSLabelModifierStep.insert(0, "1")
        Label_MPLSLabelModifierMask = Label(root43, text='MPLS Label Modifier Mask:')
        Label_MPLSLabelModifierMask.grid(row=16, column=0)
        Entry_MPLSLabelModifierMask = Entry(root43)
        Entry_MPLSLabelModifierMask.grid(row=16, column=1)
        Entry_MPLSLabelModifierMask.delete(0, "end")
        Entry_MPLSLabelModifierMask.insert(0, "1048575")

        Label_SrcIPv4Addr = Label(root43, text='Src IPv4 Address:')
        Label_SrcIPv4Addr.grid(row=17, column=0)
        Entry_SrcIPv4Addr = Entry(root43)
        Entry_SrcIPv4Addr.grid(row=17, column=1)
        Entry_SrcIPv4Addr.delete(0, "end")
        Entry_SrcIPv4Addr.insert(0, "1.1.1.1")
        Label_DestIPv4Addr = Label(root43, text='Dest IPv4 Address:')
        Label_DestIPv4Addr.grid(row=18, column=0)
        Entry_DestIPv4Addr = Entry(root43)
        Entry_DestIPv4Addr.grid(row=18, column=1)
        Entry_DestIPv4Addr.delete(0, "end")
        Entry_DestIPv4Addr.insert(0, "2.2.2.2")
        Label_DestIPv4AddrGateway = Label(root43, text='Dest IPv4 Address Gateway:')
        Label_DestIPv4AddrGateway.grid(row=19, column=0)
        Entry_DestIPv4Gateway = Entry(root43)
        Entry_DestIPv4Gateway.grid(row=19, column=1)
        Entry_DestIPv4Gateway.delete(0, "end")
        Entry_DestIPv4Gateway.insert(0, "2.2.2.2")

        button_createMPLSPkt = Button(root43, text='创建MPLS流量', command=button_StreamCreate_MPLS_Custom)
        button_createMPLSPkt.grid(row=20, column=0)

        root43.title("TestMaster MPLS Custom流量创建")
        root43.geometry('800x600')

        root43.mainloop()

    def button_StreamCreate_TCPv4(self):

        def button_StreamCreate_TCPv4_Custom():

            if Combobox_GetInfoPort.get() == '':
                messagebox.showinfo("创建流量失败", "未选择创建流量所属接口，请选择接口重试")
            else:
                # 写脚本文件
                tmtcltime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                tmtcl = '\n#create TCPv4 custom Stream '
                # 先删除测试仪的流
                tmtcl = tmtcl + '\n#先删除测试仪的流' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream'
                if ckVlan_var.get() == "Y":

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' CreateTCPStream -FrameLen  ' + Entry_FrameLength.get() + ' -Utilization ' + Entry_Load.get() + ' -TxMode $::L3_CONTINUOUS_MODE -VlanID ' + Entry_VlanID.get() + ' -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -SrcIP ' + Entry_SrcIPv4Addr.get() + ' -DesIP ' + Entry_DestIPv4Addr.get() + ' -SrcPort ' + Entry_SrcTCPPort.get() + ' -DesPort ' + Entry_DestTCPPort.get()
                    if Combobox_SrcTCPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 16 -Offset 38 -DataCount ' + Entry_SrcTCPPortModifierCount.get() + ' -Step ' + Entry_SrcTCPPortModifierStep.get()
                    if Combobox_DestTCPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 16 -Offset 40 -DataCount ' + Entry_DestTCPPortModifierCount.get() + ' -Step ' + Entry_DestTCPPortModifierStep.get()
                else:

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' CreateTCPStream -FrameLen  ' + Entry_FrameLength.get() + ' -Utilization ' + Entry_Load.get() + ' -TxMode $::L3_CONTINUOUS_MODE -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -SrcIP ' + Entry_SrcIPv4Addr.get() + ' -DesIP ' + Entry_DestIPv4Addr.get() + ' -SrcPort ' + Entry_SrcTCPPort.get() + ' -DesPort ' + Entry_DestTCPPort.get()
                    if Combobox_SrcTCPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 16 -Offset 34 -DataCount ' + Entry_SrcTCPPortModifierCount.get() + ' -Step ' + Entry_SrcTCPPortModifierStep.get()
                    if Combobox_DestTCPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 16 -Offset 36 -DataCount ' + Entry_DestTCPPortModifierCount.get() + ' -Step ' + Entry_DestTCPPortModifierStep.get()

                    tmtcldict = {
                    "time": tmtcltime,
                    "tcl": tmtcl
                    }
                    print(tmtcldict)
                    return tmtcldict

        root46 = Tk()
        reservedPortDict = {}
        intf_jsonfile = Path(self.JSON_DIR) / 'intf_reserved.json'
        with open(intf_jsonfile, 'r') as f:
            intf_json_data = f.read()
            reservedPortDict = json.loads(intf_json_data)
        reservedPortList = []
        reservedPortList = list(reservedPortDict.keys())
        Label_Separat1 = Label(root46, text='----------公共配置--------------')
        Label_Separat1.grid(row=0)
        Label_OperatePort = Label(root46, text='选择创建流量所属接口')
        Label_OperatePort.grid(row=1, column=0)

        Combobox_GetInfoPort = Combobox(root46)
        Combobox_GetInfoPort["value"] = reservedPortList
        Combobox_GetInfoPort.grid(row=1, column=1)
        Label_OperateRcvPort = Label(root46, text='选择流量接收接口，不选择为Any')
        Label_OperateRcvPort.grid(row=1, column=2)
        portVar_getInfoRcv = StringVar()
        Combobox_GetInfoRcvPort = Combobox(root46, textvariable=portVar_getInfoRcv)
        Combobox_GetInfoRcvPort["value"] = reservedPortList
        Combobox_GetInfoRcvPort.grid(row=1, column=3)
        Label_DurationMode = Label(root46, text='端口流量发送Duration模式:')
        Label_DurationMode.grid(row=2, column=0)
        DurationModeList = ["Continuous", "Bursts"]
        DurationModeVar = StringVar()
        Combobox_DurationMode = Combobox(root46, textvariable=DurationModeVar)
        Combobox_DurationMode["value"] = DurationModeList
        Combobox_DurationMode.grid(row=2, column=1)
        Label_FrameLength = Label(root46, text='流量包长:')
        Label_FrameLength.grid(row=3, column=0)
        Entry_FrameLength = Entry(root46)
        Entry_FrameLength.grid(row=3, column=1)
        Entry_FrameLength.delete(0, "end")
        Entry_FrameLength.insert(0, "128")
        Label_LoadUnit = Label(root46, text='Load单位类型:')
        Label_LoadUnit.grid(row=4, column=0)
        LoadUnitList = ["percent", "fps", "bps", "kbps", "mbps"]
        LoadUnitVar = StringVar()
        Combobox_LoadMode = Combobox(root46, textvariable=LoadUnitVar)
        Combobox_LoadMode["value"] = LoadUnitList
        Combobox_LoadMode.grid(row=4, column=1)
        Label_Load = Label(root46, text='Load:')
        Label_Load.grid(row=4, column=2)
        Entry_Load = Entry(root46)
        Entry_Load.grid(row=4, column=3)
        Entry_Load.delete(0, "end")
        Entry_Load.insert(0, "10")

        # Label_Vlan = Label(root46, text='Vlan Encap Info:')
        # Label_Vlan.grid(row=5, column=0)
        # ckVlan_var = IntVar()
        # ckVlan = Checkbutton(root46, text='设备是否需要Vlan封装', variable=ckVlan_var)
        # ckVlan.grid(row=5, column=1)

        Label_Vlan = Label(root46, text='设备是否需要Vlan封装:')
        Label_Vlan.grid(row=5, column=0)
        ckVlan_var = Combobox(root46)
        ckVlan_var["value"] = ["Y","N"]
        ckVlan_var.grid(row=5, column=1)
        ckVlan_var.delete(0, "end")
        ckVlan_var.insert(0, "Y")

        Label_VlanID = Label(root46, text='Vlan ID:')
        Label_VlanID.grid(row=5, column=2)
        Entry_VlanID = Entry(root46)
        Entry_VlanID.grid(row=5, column=3)
        Entry_VlanID.delete(0, "end")
        Entry_VlanID.insert(0, "1")
        Label_Separat2 = Label(root46, text='----------TCPv4 custom stream参数--------------')
        Label_Separat2.grid(row=6, column=0)
        Label_SrcMacAddr = Label(root46, text='Src Mac Address:')
        Label_SrcMacAddr.grid(row=7, column=0)
        Entry_SrcMacAddr = Entry(root46)
        Entry_SrcMacAddr.grid(row=7, column=1)
        Entry_SrcMacAddr.delete(0, "end")
        Entry_SrcMacAddr.insert(0, "94:29:2F:01:00:0A")

        Label_DestMacAddr = Label(root46, text='Dest Mac Address:')
        Label_DestMacAddr.grid(row=8, column=0)
        Entry_DestMacAddr = Entry(root46)
        Entry_DestMacAddr.grid(row=8, column=1)
        Entry_DestMacAddr.delete(0, "end")
        Entry_DestMacAddr.insert(0, "94:29:2F:02:00:0A")

        Label_SrcIPv4Addr = Label(root46, text='Src IPv4 Address:')
        Label_SrcIPv4Addr.grid(row=9, column=0)
        Entry_SrcIPv4Addr = Entry(root46)
        Entry_SrcIPv4Addr.grid(row=9, column=1)
        Entry_SrcIPv4Addr.delete(0, "end")
        Entry_SrcIPv4Addr.insert(0, "1.1.1.1")
        Label_DestIPv4Addr = Label(root46, text='Dest IPv4 Address:')
        Label_DestIPv4Addr.grid(row=10, column=0)
        Entry_DestIPv4Addr = Entry(root46)
        Entry_DestIPv4Addr.grid(row=10, column=1)
        Entry_DestIPv4Addr.delete(0, "end")
        Entry_DestIPv4Addr.insert(0, "2.2.2.2")
        Label_DestIPv4AddrGateway = Label(root46, text='Dest IPv4 Address Gateway:')
        Label_DestIPv4AddrGateway.grid(row=11, column=0)
        Entry_DestIPv4Gateway = Entry(root46)
        Entry_DestIPv4Gateway.grid(row=11, column=1)
        Entry_DestIPv4Gateway.delete(0, "end")
        Entry_DestIPv4Gateway.insert(0, "2.2.2.2")

        Label_SrcTCPPort = Label(root46, text='Src TCP Port:')
        Label_SrcTCPPort.grid(row=12, column=0)
        Entry_SrcTCPPort = Entry(root46)
        Entry_SrcTCPPort.grid(row=12, column=1)
        Entry_SrcTCPPort.delete(0, "end")
        Entry_SrcTCPPort.insert(0, "1024")

        Label_SrcTCPPortIsModifier = Label(root46, text='Src TCP Port是否可变:')
        Label_SrcTCPPortIsModifier.grid(row=13, column=0)
        EnableList = [True, False]

        Combobox_SrcTCPPortIsModifier = Combobox(root46)
        Combobox_SrcTCPPortIsModifier["value"] = EnableList
        Combobox_SrcTCPPortIsModifier.grid(row=13, column=1)
        Label_SrcTCPPortModifierCount = Label(root46, text='Src TCP Port Modifier Count:')
        Label_SrcTCPPortModifierCount.grid(row=14, column=0)
        Entry_SrcTCPPortModifierCount = Entry(root46)
        Entry_SrcTCPPortModifierCount.grid(row=14, column=1)
        Entry_SrcTCPPortModifierCount.delete(0, "end")
        Entry_SrcTCPPortModifierCount.insert(0, "1")
        Label_SrcTCPPortModifierStep = Label(root46, text='Src TCP Port Modifier Step:')
        Label_SrcTCPPortModifierStep.grid(row=15, column=0)
        Entry_SrcTCPPortModifierStep = Entry(root46)
        Entry_SrcTCPPortModifierStep.grid(row=15, column=1)
        Entry_SrcTCPPortModifierStep.delete(0, "end")
        Entry_SrcTCPPortModifierStep.insert(0, "1")
        Label_SrcTCPPortModifierMask = Label(root46, text='Src TCP Port Modifier Mask:')
        Label_SrcTCPPortModifierMask.grid(row=16, column=0)
        Entry_SrcTCPPortModifierMask = Entry(root46)
        Entry_SrcTCPPortModifierMask.grid(row=16, column=1)
        Entry_SrcTCPPortModifierMask.delete(0, "end")
        Entry_SrcTCPPortModifierMask.insert(0, "65535")

        Label_DestTCPPort = Label(root46, text='Dest TCP Port:')
        Label_DestTCPPort.grid(row=17, column=0)
        Entry_DestTCPPort = Entry(root46)
        Entry_DestTCPPort.grid(row=17, column=1)
        Entry_DestTCPPort.delete(0, "end")
        Entry_DestTCPPort.insert(0, "1024")

        Label_DestTCPPortIsModifier = Label(root46, text='Dest TCP Port是否可变:')
        Label_DestTCPPortIsModifier.grid(row=18, column=0)

        Combobox_DestTCPPortIsModifier = Combobox(root46)
        Combobox_DestTCPPortIsModifier["value"] = EnableList
        Combobox_DestTCPPortIsModifier.grid(row=18, column=1)
        Label_DestTCPPortModifierCount = Label(root46, text='Dest TCP Port Modifier Count:')
        Label_DestTCPPortModifierCount.grid(row=19, column=0)
        Entry_DestTCPPortModifierCount = Entry(root46)
        Entry_DestTCPPortModifierCount.grid(row=19, column=1)
        Entry_DestTCPPortModifierCount.delete(0, "end")
        Entry_DestTCPPortModifierCount.insert(0, "1")
        Label_DestTCPPortModifierStep = Label(root46, text='Dest TCP Port Modifier Step:')
        Label_DestTCPPortModifierStep.grid(row=20, column=0)
        Entry_DestTCPPortModifierStep = Entry(root46)
        Entry_DestTCPPortModifierStep.grid(row=20, column=1)
        Entry_DestTCPPortModifierStep.delete(0, "end")
        Entry_DestTCPPortModifierStep.insert(0, "1")
        Label_DestTCPPortModifierMask = Label(root46, text='Dest TCP Port Modifier Mask:')
        Label_DestTCPPortModifierMask.grid(row=21, column=0)
        Entry_DestTCPPortModifierMask = Entry(root46)
        Entry_DestTCPPortModifierMask.grid(row=21, column=1)
        Entry_DestTCPPortModifierMask.delete(0, "end")
        Entry_DestTCPPortModifierMask.insert(0, "65535")

        button_createTCPv4Pkt = Button(root46, text='创建TCPv4流量', command=button_StreamCreate_TCPv4_Custom)
        button_createTCPv4Pkt.grid(row=22, column=0)

        root46.title("TestMaster TCPv4 Custom流量创建")
        root46.geometry('800x600')

        root46.mainloop()

    def button_StreamCreate_TCPv6(self):

        def button_StreamCreate_TCPv6_Custom():

            if Combobox_GetInfoPort.get() == '':
                messagebox.showinfo("创建流量失败", "未选择创建流量所属接口，请选择接口重试")
            else:
                # 写脚本文件
                tmtcltime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                tmtcl = '\n#create TCPv6 custom Stream '
                # 先删除测试仪的流
                tmtcl = tmtcl + '\n#先删除测试仪的流' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream'
                if ckVlan_var.get() == "Y":

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' CreateIPv6TCPStream -FrameLen  ' + Entry_FrameLength.get() + ' -Utilization ' + Entry_Load.get() + ' -TxMode $::L3_CONTINUOUS_MODE -VlanID ' + Entry_VlanID.get() + ' -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -SrcIP ' + Entry_SrcIPv6Addr.get() + ' -DesIP ' + Entry_DestIPv6Addr.get() + ' -SrcPort ' + Entry_SrcTCPPort.get() + ' -DesPort ' + Entry_DestTCPPort.get()
                    if Combobox_SrcTCPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 16 -Offset 62 -DataCount ' + Entry_SrcTCPPortModifierCount.get() + ' -Step ' + Entry_SrcTCPPortModifierStep.get()
                    if Combobox_DestTCPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 16 -Offset 64 -DataCount ' + Entry_DestTCPPortModifierCount.get() + ' -Step ' + Entry_DestTCPPortModifierStep.get()
                else:

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' CreateIPv6TCPStream -FrameLen  ' + Entry_FrameLength.get() + ' -Utilization ' + Entry_Load.get() + ' -TxMode $::L3_CONTINUOUS_MODE -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -SrcIP ' + Entry_SrcIPv6Addr.get() + ' -DesIP ' + Entry_DestIPv6Addr.get() + ' -SrcPort ' + Entry_SrcTCPPort.get() + ' -DesPort ' + Entry_DestTCPPort.get()
                    if Combobox_SrcTCPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 16 -Offset 58 -DataCount ' + Entry_SrcTCPPortModifierCount.get() + ' -Step ' + Entry_SrcTCPPortModifierStep.get()
                    if Combobox_DestTCPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 16 -Offset 60 -DataCount ' + Entry_DestTCPPortModifierCount.get() + ' -Step ' + Entry_DestTCPPortModifierStep.get()

                    tmtcldict = {
                        "time": tmtcltime,
                        "tcl": tmtcl
                    }
                    print(tmtcldict)
                    return tmtcldict

        root47 = Tk()
        reservedPortDict = {}
        intf_jsonfile = Path(self.JSON_DIR) / 'intf_reserved.json'
        with open(intf_jsonfile, 'r') as f:
            intf_json_data = f.read()
            reservedPortDict = json.loads(intf_json_data)
        reservedPortList = []
        reservedPortList = list(reservedPortDict.keys())
        Label_Separat1 = Label(root47, text='----------公共配置--------------')
        Label_Separat1.grid(row=0)
        Label_OperatePort = Label(root47, text='选择创建流量所属接口')
        Label_OperatePort.grid(row=1, column=0)

        Combobox_GetInfoPort = Combobox(root47)
        Combobox_GetInfoPort["value"] = reservedPortList
        Combobox_GetInfoPort.grid(row=1, column=1)
        Label_OperateRcvPort = Label(root47, text='选择流量接收接口，不选择为Any')
        Label_OperateRcvPort.grid(row=1, column=2)
        portVar_getInfoRcv = StringVar()
        Combobox_GetInfoRcvPort = Combobox(root47, textvariable=portVar_getInfoRcv)
        Combobox_GetInfoRcvPort["value"] = reservedPortList
        Combobox_GetInfoRcvPort.grid(row=1, column=3)
        Label_DurationMode = Label(root47, text='端口流量发送Duration模式:')
        Label_DurationMode.grid(row=2, column=0)
        DurationModeList = ["Continuous", "Bursts"]
        DurationModeVar = StringVar()
        Combobox_DurationMode = Combobox(root47, textvariable=DurationModeVar)
        Combobox_DurationMode["value"] = DurationModeList
        Combobox_DurationMode.grid(row=2, column=1)
        Label_FrameLength = Label(root47, text='流量包长:')
        Label_FrameLength.grid(row=3, column=0)
        Entry_FrameLength = Entry(root47)
        Entry_FrameLength.grid(row=3, column=1)
        Entry_FrameLength.delete(0, "end")
        Entry_FrameLength.insert(0, "128")
        Label_LoadUnit = Label(root47, text='Load单位类型:')
        Label_LoadUnit.grid(row=4, column=0)
        LoadUnitList = ["percent", "fps", "bps", "kbps", "mbps"]
        LoadUnitVar = StringVar()
        Combobox_LoadMode = Combobox(root47, textvariable=LoadUnitVar)
        Combobox_LoadMode["value"] = LoadUnitList
        Combobox_LoadMode.grid(row=4, column=1)
        Label_Load = Label(root47, text='Load:')
        Label_Load.grid(row=4, column=2)
        Entry_Load = Entry(root47)
        Entry_Load.grid(row=4, column=3)
        Entry_Load.delete(0, "end")
        Entry_Load.insert(0, "10")

        # Label_Vlan = Label(root47, text='Vlan Encap Info:')
        # Label_Vlan.grid(row=5, column=0)
        # ckVlan_var = IntVar()
        # ckVlan = Checkbutton(root47, text='设备是否需要Vlan封装', variable=ckVlan_var)
        # ckVlan.grid(row=5, column=1)

        Label_Vlan = Label(root47, text='设备是否需要Vlan封装:')
        Label_Vlan.grid(row=5, column=0)
        ckVlan_var = Combobox(root47)
        ckVlan_var["value"] = ["Y","N"]
        ckVlan_var.grid(row=5, column=1)
        ckVlan_var.delete(0, "end")
        ckVlan_var.insert(0, "Y")

        Label_VlanID = Label(root47, text='Vlan ID:')
        Label_VlanID.grid(row=5, column=2)
        Entry_VlanID = Entry(root47)
        Entry_VlanID.grid(row=5, column=3)
        Entry_VlanID.delete(0, "end")
        Entry_VlanID.insert(0, "1")
        Label_Separat2 = Label(root47, text='----------TCPv6 custom stream参数--------------')
        Label_Separat2.grid(row=6, column=0)
        Label_SrcMacAddr = Label(root47, text='Src Mac Address:')
        Label_SrcMacAddr.grid(row=7, column=0)
        Entry_SrcMacAddr = Entry(root47)
        Entry_SrcMacAddr.grid(row=7, column=1)
        Entry_SrcMacAddr.delete(0, "end")
        Entry_SrcMacAddr.insert(0, "94:29:2F:01:00:0A")

        Label_DestMacAddr = Label(root47, text='Dest Mac Address:')
        Label_DestMacAddr.grid(row=8, column=0)
        Entry_DestMacAddr = Entry(root47)
        Entry_DestMacAddr.grid(row=8, column=1)
        Entry_DestMacAddr.delete(0, "end")
        Entry_DestMacAddr.insert(0, "94:29:2F:02:00:0A")

        Label_SrcIPv6Addr = Label(root47, text='Src IPv6 Address:')
        Label_SrcIPv6Addr.grid(row=9, column=0)
        Entry_SrcIPv6Addr = Entry(root47)
        Entry_SrcIPv6Addr.grid(row=9, column=1)
        Entry_SrcIPv6Addr.delete(0, "end")
        Entry_SrcIPv6Addr.insert(0, "2000::2")
        Label_DestIPv6Addr = Label(root47, text='Dest IPv6 Address:')
        Label_DestIPv6Addr.grid(row=10, column=0)
        Entry_DestIPv6Addr = Entry(root47)
        Entry_DestIPv6Addr.grid(row=10, column=1)
        Entry_DestIPv6Addr.delete(0, "end")
        Entry_DestIPv6Addr.insert(0, "2000::1")
        Label_DestIPv6AddrGateway = Label(root47, text='Dest IPv6 Address Gateway:')
        Label_DestIPv6AddrGateway.grid(row=11, column=0)
        Entry_DestIPv6Gateway = Entry(root47)
        Entry_DestIPv6Gateway.grid(row=11, column=1)
        Entry_DestIPv6Gateway.delete(0, "end")
        Entry_DestIPv6Gateway.insert(0, "2000::1")

        Label_SrcTCPPort = Label(root47, text='Src TCP Port:')
        Label_SrcTCPPort.grid(row=12, column=0)
        Entry_SrcTCPPort = Entry(root47)
        Entry_SrcTCPPort.grid(row=12, column=1)
        Entry_SrcTCPPort.delete(0, "end")
        Entry_SrcTCPPort.insert(0, "1024")

        Label_SrcTCPPortIsModifier = Label(root47, text='Src TCP Port是否可变:')
        Label_SrcTCPPortIsModifier.grid(row=13, column=0)
        EnableList = [True, False]


        Combobox_SrcTCPPortIsModifier = Combobox(root47)
        Combobox_SrcTCPPortIsModifier["value"] = EnableList
        Combobox_SrcTCPPortIsModifier.grid(row=13, column=1)

        Label_SrcTCPPortModifierCount = Label(root47, text='Src TCP Port Modifier Count:')
        Label_SrcTCPPortModifierCount.grid(row=14, column=0)
        Entry_SrcTCPPortModifierCount = Entry(root47)
        Entry_SrcTCPPortModifierCount.grid(row=14, column=1)
        Entry_SrcTCPPortModifierCount.delete(0, "end")
        Entry_SrcTCPPortModifierCount.insert(0, "1")
        Label_SrcTCPPortModifierStep = Label(root47, text='Src TCP Port Modifier Step:')
        Label_SrcTCPPortModifierStep.grid(row=15, column=0)
        Entry_SrcTCPPortModifierStep = Entry(root47)
        Entry_SrcTCPPortModifierStep.grid(row=15, column=1)
        Entry_SrcTCPPortModifierStep.delete(0, "end")
        Entry_SrcTCPPortModifierStep.insert(0, "1")
        Label_SrcTCPPortModifierMask = Label(root47, text='Src TCP Port Modifier Mask:')
        Label_SrcTCPPortModifierMask.grid(row=16, column=0)
        Entry_SrcTCPPortModifierMask = Entry(root47)
        Entry_SrcTCPPortModifierMask.grid(row=16, column=1)
        Entry_SrcTCPPortModifierMask.delete(0, "end")
        Entry_SrcTCPPortModifierMask.insert(0, "65535")

        Label_DestTCPPort = Label(root47, text='Dest TCP Port:')
        Label_DestTCPPort.grid(row=17, column=0)
        Entry_DestTCPPort = Entry(root47)
        Entry_DestTCPPort.grid(row=17, column=1)
        Entry_DestTCPPort.delete(0, "end")
        Entry_DestTCPPort.insert(0, "1024")

        Label_DestTCPPortIsModifier = Label(root47, text='Dest TCP Port是否可变:')
        Label_DestTCPPortIsModifier.grid(row=18, column=0)


        Combobox_DestTCPPortIsModifier = Combobox(root47)
        Combobox_DestTCPPortIsModifier["value"] = EnableList
        Combobox_DestTCPPortIsModifier.grid(row=18, column=1)

        Label_DestTCPPortModifierCount = Label(root47, text='Dest TCP Port Modifier Count:')
        Label_DestTCPPortModifierCount.grid(row=19, column=0)
        Entry_DestTCPPortModifierCount = Entry(root47)
        Entry_DestTCPPortModifierCount.grid(row=19, column=1)
        Entry_DestTCPPortModifierCount.delete(0, "end")
        Entry_DestTCPPortModifierCount.insert(0, "1")
        Label_DestTCPPortModifierStep = Label(root47, text='Dest TCP Port Modifier Step:')
        Label_DestTCPPortModifierStep.grid(row=20, column=0)
        Entry_DestTCPPortModifierStep = Entry(root47)
        Entry_DestTCPPortModifierStep.grid(row=20, column=1)
        Entry_DestTCPPortModifierStep.delete(0, "end")
        Entry_DestTCPPortModifierStep.insert(0, "1")
        Label_DestTCPPortModifierMask = Label(root47, text='Dest TCP Port Modifier Mask:')
        Label_DestTCPPortModifierMask.grid(row=21, column=0)
        Entry_DestTCPPortModifierMask = Entry(root47)
        Entry_DestTCPPortModifierMask.grid(row=21, column=1)
        Entry_DestTCPPortModifierMask.delete(0, "end")
        Entry_DestTCPPortModifierMask.insert(0, "65535")

        button_createTCPv6Pkt = Button(root47, text='创建TCPv6流量', command=button_StreamCreate_TCPv6_Custom)
        button_createTCPv6Pkt.grid(row=22, column=0)

        root47.title("TestMaster TCPv6 Custom流量创建")
        root47.geometry('800x600')

        root47.mainloop()

    def button_StreamCreate_UDPv4(self):

        def button_StreamCreate_UDPv4_Custom():

            if Combobox_GetInfoPort.get() == '':
                messagebox.showinfo("创建流量失败", "未选择创建流量所属接口，请选择接口重试")
            else:
                # 写脚本文件
                tmtcltime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                tmtcl = '\n#create UDPv4 custom Stream '
                # 先删除测试仪的流
                tmtcl = tmtcl + '\n#先删除测试仪的流' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream'
                if ckVlan_var.get() == "Y":

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' CreateUDPStream -FrameLen  ' + Entry_FrameLength.get() + ' -Utilization ' + Entry_Load.get() + ' -TxMode $::L3_CONTINUOUS_MODE -VlanID ' + Entry_VlanID.get() + ' -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -SrcIP ' + Entry_SrcIPv4Addr.get() + ' -DesIP ' + Entry_DestIPv4Addr.get() + ' -SrcPort ' + Entry_SrcUDPPort.get() + ' -DesPort ' + Entry_DestUDPPort.get()
                    if Combobox_SrcUDPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 16 -Offset 38 -DataCount ' + Entry_SrcUDPPortModifierCount.get() + ' -Step ' + Entry_SrcUDPPortModifierStep.get()
                    if Combobox_DestUDPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 16 -Offset 40 -DataCount ' + Entry_DestUDPPortModifierCount.get() + ' -Step ' + Entry_DestUDPPortModifierStep.get()
                else:

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' CreateUDPStream -FrameLen  ' + Entry_FrameLength.get() + ' -Utilization ' + Entry_Load.get() + ' -TxMode $::L3_CONTINUOUS_MODE -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -SrcIP ' + Entry_SrcIPv4Addr.get() + ' -DesIP ' + Entry_DestIPv4Addr.get() + ' -SrcPort ' + Entry_SrcUDPPort.get() + ' -DesPort ' + Entry_DestUDPPort.get()
                    if Combobox_SrcUDPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 16 -Offset 34 -DataCount ' + Entry_SrcUDPPortModifierCount.get() + ' -Step ' + Entry_SrcUDPPortModifierStep.get()
                    if Combobox_DestUDPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 16 -Offset 36 -DataCount ' + Entry_DestUDPPortModifierCount.get() + ' -Step ' + Entry_DestUDPPortModifierStep.get()

                tmtcldict = {
                    "time": tmtcltime,
                    "tcl": tmtcl
                }
                print(tmtcldict)
                return tmtcldict

        root48 = Tk()
        reservedPortDict = {}
        intf_jsonfile = Path(self.JSON_DIR) / 'intf_reserved.json'
        with open(intf_jsonfile, 'r') as f:
            intf_json_data = f.read()
            reservedPortDict = json.loads(intf_json_data)
        reservedPortList = []
        reservedPortList = list(reservedPortDict.keys())
        Label_Separat1 = Label(root48, text='----------公共配置--------------')
        Label_Separat1.grid(row=0)
        Label_OperatePort = Label(root48, text='选择创建流量所属接口')
        Label_OperatePort.grid(row=1, column=0)

        Combobox_GetInfoPort = Combobox(root48)
        Combobox_GetInfoPort["value"] = reservedPortList
        Combobox_GetInfoPort.grid(row=1, column=1)
        Label_OperateRcvPort = Label(root48, text='选择流量接收接口，不选择为Any')
        Label_OperateRcvPort.grid(row=1, column=2)
        portVar_getInfoRcv = StringVar()
        Combobox_GetInfoRcvPort = Combobox(root48, textvariable=portVar_getInfoRcv)
        Combobox_GetInfoRcvPort["value"] = reservedPortList
        Combobox_GetInfoRcvPort.grid(row=1, column=3)
        Label_DurationMode = Label(root48, text='端口流量发送Duration模式:')
        Label_DurationMode.grid(row=2, column=0)
        DurationModeList = ["Continuous", "Bursts"]
        DurationModeVar = StringVar()
        Combobox_DurationMode = Combobox(root48, textvariable=DurationModeVar)
        Combobox_DurationMode["value"] = DurationModeList
        Combobox_DurationMode.grid(row=2, column=1)
        Label_FrameLength = Label(root48, text='流量包长:')
        Label_FrameLength.grid(row=3, column=0)
        Entry_FrameLength = Entry(root48)
        Entry_FrameLength.grid(row=3, column=1)
        Entry_FrameLength.delete(0, "end")
        Entry_FrameLength.insert(0, "128")
        Label_LoadUnit = Label(root48, text='Load单位类型:')
        Label_LoadUnit.grid(row=4, column=0)
        LoadUnitList = ["percent", "fps", "bps", "kbps", "mbps"]
        LoadUnitVar = StringVar()
        Combobox_LoadMode = Combobox(root48, textvariable=LoadUnitVar)
        Combobox_LoadMode["value"] = LoadUnitList
        Combobox_LoadMode.grid(row=4, column=1)
        Label_Load = Label(root48, text='Load:')
        Label_Load.grid(row=4, column=2)
        Entry_Load = Entry(root48)
        Entry_Load.grid(row=4, column=3)
        Entry_Load.delete(0, "end")
        Entry_Load.insert(0, "10")

        # Label_Vlan = Label(root48, text='Vlan Encap Info:')
        # Label_Vlan.grid(row=5, column=0)
        # ckVlan_var = IntVar()
        # ckVlan = Checkbutton(root48, text='设备是否需要Vlan封装', variable=ckVlan_var)
        # ckVlan.grid(row=5, column=1)

        Label_Vlan = Label(root48, text='设备是否需要Vlan封装:')
        Label_Vlan.grid(row=5, column=0)
        ckVlan_var = Combobox(root48)
        ckVlan_var["value"] = ["Y","N"]
        ckVlan_var.grid(row=5, column=1)
        ckVlan_var.delete(0, "end")
        ckVlan_var.insert(0, "Y")

        Label_VlanID = Label(root48, text='Vlan ID:')
        Label_VlanID.grid(row=5, column=2)
        Entry_VlanID = Entry(root48)
        Entry_VlanID.grid(row=5, column=3)
        Entry_VlanID.delete(0, "end")
        Entry_VlanID.insert(0, "1")
        Label_Separat2 = Label(root48, text='----------UDPv4 custom stream参数--------------')
        Label_Separat2.grid(row=6, column=0)
        Label_SrcMacAddr = Label(root48, text='Src Mac Address:')
        Label_SrcMacAddr.grid(row=7, column=0)
        Entry_SrcMacAddr = Entry(root48)
        Entry_SrcMacAddr.grid(row=7, column=1)
        Entry_SrcMacAddr.delete(0, "end")
        Entry_SrcMacAddr.insert(0, "94:29:2F:01:00:0A")

        Label_DestMacAddr = Label(root48, text='Dest Mac Address:')
        Label_DestMacAddr.grid(row=8, column=0)
        Entry_DestMacAddr = Entry(root48)
        Entry_DestMacAddr.grid(row=8, column=1)
        Entry_DestMacAddr.delete(0, "end")
        Entry_DestMacAddr.insert(0, "94:29:2F:02:00:0A")

        Label_SrcIPv4Addr = Label(root48, text='Src IPv4 Address:')
        Label_SrcIPv4Addr.grid(row=9, column=0)
        Entry_SrcIPv4Addr = Entry(root48)
        Entry_SrcIPv4Addr.grid(row=9, column=1)
        Entry_SrcIPv4Addr.delete(0, "end")
        Entry_SrcIPv4Addr.insert(0, "1.1.1.1")
        Label_DestIPv4Addr = Label(root48, text='Dest IPv4 Address:')
        Label_DestIPv4Addr.grid(row=10, column=0)
        Entry_DestIPv4Addr = Entry(root48)
        Entry_DestIPv4Addr.grid(row=10, column=1)
        Entry_DestIPv4Addr.delete(0, "end")
        Entry_DestIPv4Addr.insert(0, "2.2.2.2")
        Label_DestIPv4AddrGateway = Label(root48, text='Dest IPv4 Address Gateway:')
        Label_DestIPv4AddrGateway.grid(row=11, column=0)
        Entry_DestIPv4Gateway = Entry(root48)
        Entry_DestIPv4Gateway.grid(row=11, column=1)
        Entry_DestIPv4Gateway.delete(0, "end")
        Entry_DestIPv4Gateway.insert(0, "2.2.2.2")

        Label_SrcUDPPort = Label(root48, text='Src UDP Port:')
        Label_SrcUDPPort.grid(row=12, column=0)
        Entry_SrcUDPPort = Entry(root48)
        Entry_SrcUDPPort.grid(row=12, column=1)
        Entry_SrcUDPPort.delete(0, "end")
        Entry_SrcUDPPort.insert(0, "1024")

        Label_SrcUDPPortIsModifier = Label(root48, text='Src UDP Port是否可变:')
        Label_SrcUDPPortIsModifier.grid(row=13, column=0)
        EnableList = [True, False]

        Combobox_SrcUDPPortIsModifier = Combobox(root48)
        Combobox_SrcUDPPortIsModifier["value"] = EnableList
        Combobox_SrcUDPPortIsModifier.grid(row=13, column=1)
        Label_SrcUDPPortModifierCount = Label(root48, text='Src UDP Port Modifier Count:')
        Label_SrcUDPPortModifierCount.grid(row=14, column=0)
        Entry_SrcUDPPortModifierCount = Entry(root48)
        Entry_SrcUDPPortModifierCount.grid(row=14, column=1)
        Entry_SrcUDPPortModifierCount.delete(0, "end")
        Entry_SrcUDPPortModifierCount.insert(0, "1")
        Label_SrcUDPPortModifierStep = Label(root48, text='Src UDP Port Modifier Step:')
        Label_SrcUDPPortModifierStep.grid(row=15, column=0)
        Entry_SrcUDPPortModifierStep = Entry(root48)
        Entry_SrcUDPPortModifierStep.grid(row=15, column=1)
        Entry_SrcUDPPortModifierStep.delete(0, "end")
        Entry_SrcUDPPortModifierStep.insert(0, "1")
        Label_SrcUDPPortModifierMask = Label(root48, text='Src UDP Port Modifier Mask:')
        Label_SrcUDPPortModifierMask.grid(row=16, column=0)
        Entry_SrcUDPPortModifierMask = Entry(root48)
        Entry_SrcUDPPortModifierMask.grid(row=16, column=1)
        Entry_SrcUDPPortModifierMask.delete(0, "end")
        Entry_SrcUDPPortModifierMask.insert(0, "65535")

        Label_DestUDPPort = Label(root48, text='Dest UDP Port:')
        Label_DestUDPPort.grid(row=17, column=0)
        Entry_DestUDPPort = Entry(root48)
        Entry_DestUDPPort.grid(row=17, column=1)
        Entry_DestUDPPort.delete(0, "end")
        Entry_DestUDPPort.insert(0, "1024")

        Label_DestUDPPortIsModifier = Label(root48, text='Dest UDP Port是否可变:')
        Label_DestUDPPortIsModifier.grid(row=18, column=0)

        Combobox_DestUDPPortIsModifier = Combobox(root48)
        Combobox_DestUDPPortIsModifier["value"] = EnableList
        Combobox_DestUDPPortIsModifier.grid(row=18, column=1)
        Label_DestUDPPortModifierCount = Label(root48, text='Dest UDP Port Modifier Count:')
        Label_DestUDPPortModifierCount.grid(row=19, column=0)
        Entry_DestUDPPortModifierCount = Entry(root48)
        Entry_DestUDPPortModifierCount.grid(row=19, column=1)
        Entry_DestUDPPortModifierCount.delete(0, "end")
        Entry_DestUDPPortModifierCount.insert(0, "1")
        Label_DestUDPPortModifierStep = Label(root48, text='Dest UDP Port Modifier Step:')
        Label_DestUDPPortModifierStep.grid(row=20, column=0)
        Entry_DestUDPPortModifierStep = Entry(root48)
        Entry_DestUDPPortModifierStep.grid(row=20, column=1)
        Entry_DestUDPPortModifierStep.delete(0, "end")
        Entry_DestUDPPortModifierStep.insert(0, "1")
        Label_DestUDPPortModifierMask = Label(root48, text='Dest UDP Port Modifier Mask:')
        Label_DestUDPPortModifierMask.grid(row=21, column=0)
        Entry_DestUDPPortModifierMask = Entry(root48)
        Entry_DestUDPPortModifierMask.grid(row=21, column=1)
        Entry_DestUDPPortModifierMask.delete(0, "end")
        Entry_DestUDPPortModifierMask.insert(0, "65535")

        button_createUDPv4Pkt = Button(root48, text='创建UDPv4流量', command=button_StreamCreate_UDPv4_Custom)
        button_createUDPv4Pkt.grid(row=22, column=0)

        root48.title("TestMaster UDPv4 Custom流量创建")
        root48.geometry('800x600')

        root48.mainloop()

    def button_StreamCreate_UDPv6(self):

        def button_StreamCreate_UDPv6_Custom():

            if Combobox_GetInfoPort.get() == '':
                messagebox.showinfo("创建流量失败", "未选择创建流量所属接口，请选择接口重试")
            else:
                # 写脚本文件
                tmtcltime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
                tmtcl = '\n#create UDPv6 custom Stream '
                # 先删除测试仪的流
                tmtcl = tmtcl + '\n#先删除测试仪的流' + '\nTestInstrument1.' + self.topoPortName + ' DeleteAllStream'
                if ckVlan_var.get() == "Y":

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' CreateIPv6UDPStream -FrameLen  ' + Entry_FrameLength.get() + ' -Utilization ' + Entry_Load.get() + ' -TxMode $::L3_CONTINUOUS_MODE -VlanID ' + Entry_VlanID.get() + ' -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -SrcIP ' + Entry_SrcIPv6Addr.get() + ' -DesIP ' + Entry_DestIPv6Addr.get() + ' -SrcPort ' + Entry_SrcUDPPort.get() + ' -DesPort ' + Entry_DestUDPPort.get()
                    if Combobox_SrcUDPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 16 -Offset 62 -DataCount ' + Entry_SrcUDPPortModifierCount.get() + ' -Step ' + Entry_SrcUDPPortModifierStep.get()
                    if Combobox_DestUDPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 16 -Offset 64 -DataCount ' + Entry_DestUDPPortModifierCount.get() + ' -Step ' + Entry_DestUDPPortModifierStep.get()
                else:

                    tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' CreateIPv6UDPStream -FrameLen  ' + Entry_FrameLength.get() + ' -Utilization ' + Entry_Load.get() + ' -TxMode $::L3_CONTINUOUS_MODE -SrcMac ' + Entry_SrcMacAddr.get() + ' -DesMac ' + Entry_DestMacAddr.get() + ' -SrcIP ' + Entry_SrcIPv6Addr.get() + ' -DesIP ' + Entry_DestIPv6Addr.get() + ' -SrcPort ' + Entry_SrcUDPPort.get() + ' -DesPort ' + Entry_DestUDPPort.get()
                    if Combobox_SrcUDPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 1 -Mode 2 -Range 16 -Offset 58 -DataCount ' + Entry_SrcUDPPortModifierCount.get() + ' -Step ' + Entry_SrcUDPPortModifierStep.get()
                    if Combobox_DestUDPPortIsModifier.get():

                        tmtcl = tmtcl + '\nTestInstrument1.' + self.topoPortName + ' SetCustomVFD -id 2 - Mode 2 -Range 16 -Offset 60 -DataCount ' + Entry_DestUDPPortModifierCount.get() + ' -Step ' + Entry_DestUDPPortModifierStep.get()

                tmtcldict = {
                    "time": tmtcltime,
                    "tcl": tmtcl
                }
                print(tmtcldict)
                return tmtcldict


        root49 = Tk()
        reservedPortDict = {}
        intf_jsonfile = Path(self.JSON_DIR) / 'intf_reserved.json'
        with open(intf_jsonfile, 'r') as f:
            intf_json_data = f.read()
            reservedPortDict = json.loads(intf_json_data)
        reservedPortList = []
        reservedPortList = list(reservedPortDict.keys())
        Label_Separat1 = Label(root49, text='----------公共配置--------------')
        Label_Separat1.grid(row=0)
        Label_OperatePort = Label(root49, text='选择创建流量所属接口')
        Label_OperatePort.grid(row=1, column=0)
        portVar_getInfo = StringVar()
        Combobox_GetInfoPort = Combobox(root49, textvariable=portVar_getInfo)
        Combobox_GetInfoPort["value"] = reservedPortList
        Combobox_GetInfoPort.grid(row=1, column=1)
        Label_OperateRcvPort = Label(root49, text='选择流量接收接口，不选择为Any')
        Label_OperateRcvPort.grid(row=1, column=2)

        Combobox_GetInfoRcvPort = Combobox(root49)
        Combobox_GetInfoRcvPort["value"] = reservedPortList
        Combobox_GetInfoRcvPort.grid(row=1, column=3)
        Label_DurationMode = Label(root49, text='端口流量发送Duration模式:')
        Label_DurationMode.grid(row=2, column=0)
        DurationModeList = ["Continuous", "Bursts"]
        DurationModeVar = StringVar()
        Combobox_DurationMode = Combobox(root49, textvariable=DurationModeVar)
        Combobox_DurationMode["value"] = DurationModeList
        Combobox_DurationMode.grid(row=2, column=1)
        Label_FrameLength = Label(root49, text='流量包长:')
        Label_FrameLength.grid(row=3, column=0)
        Entry_FrameLength = Entry(root49)
        Entry_FrameLength.grid(row=3, column=1)
        Entry_FrameLength.delete(0, "end")
        Entry_FrameLength.insert(0, "128")
        Label_LoadUnit = Label(root49, text='Load单位类型:')
        Label_LoadUnit.grid(row=4, column=0)
        LoadUnitList = ["percent", "fps", "bps", "kbps", "mbps"]
        LoadUnitVar = StringVar()
        Combobox_LoadMode = Combobox(root49, textvariable=LoadUnitVar)
        Combobox_LoadMode["value"] = LoadUnitList
        Combobox_LoadMode.grid(row=4, column=1)
        Label_Load = Label(root49, text='Load:')
        Label_Load.grid(row=4, column=2)
        Entry_Load = Entry(root49)
        Entry_Load.grid(row=4, column=3)
        Entry_Load.delete(0, "end")
        Entry_Load.insert(0, "10")

        # Label_Vlan = Label(root49, text='Vlan Encap Info:')
        # Label_Vlan.grid(row=5, column=0)
        # ckVlan_var = IntVar()
        # ckVlan = Checkbutton(root49, text='设备是否需要Vlan封装', variable=ckVlan_var)
        # ckVlan.grid(row=5, column=1)

        Label_Vlan = Label(root49, text='设备是否需要Vlan封装:')
        Label_Vlan.grid(row=5, column=0)
        ckVlan_var = Combobox(root49)
        ckVlan_var["value"] = ["Y","N"]
        ckVlan_var.grid(row=5, column=1)
        ckVlan_var.delete(0, "end")
        ckVlan_var.insert(0, "Y")

        Label_VlanID = Label(root49, text='Vlan ID:')
        Label_VlanID.grid(row=5, column=2)
        Entry_VlanID = Entry(root49)
        Entry_VlanID.grid(row=5, column=3)
        Entry_VlanID.delete(0, "end")
        Entry_VlanID.insert(0, "1")
        Label_Separat2 = Label(root49, text='----------UDPv6 custom stream参数--------------')
        Label_Separat2.grid(row=6, column=0)
        Label_SrcMacAddr = Label(root49, text='Src Mac Address:')
        Label_SrcMacAddr.grid(row=7, column=0)
        Entry_SrcMacAddr = Entry(root49)
        Entry_SrcMacAddr.grid(row=7, column=1)
        Entry_SrcMacAddr.delete(0, "end")
        Entry_SrcMacAddr.insert(0, "94:29:2F:01:00:0A")

        Label_DestMacAddr = Label(root49, text='Dest Mac Address:')
        Label_DestMacAddr.grid(row=8, column=0)
        Entry_DestMacAddr = Entry(root49)
        Entry_DestMacAddr.grid(row=8, column=1)
        Entry_DestMacAddr.delete(0, "end")
        Entry_DestMacAddr.insert(0, "94:29:2F:02:00:0A")

        Label_SrcIPv6Addr = Label(root49, text='Src IPv6 Address:')
        Label_SrcIPv6Addr.grid(row=9, column=0)
        Entry_SrcIPv6Addr = Entry(root49)
        Entry_SrcIPv6Addr.grid(row=9, column=1)
        Entry_SrcIPv6Addr.delete(0, "end")
        Entry_SrcIPv6Addr.insert(0, "2000::2")
        Label_DestIPv6Addr = Label(root49, text='Dest IPv6 Address:')
        Label_DestIPv6Addr.grid(row=10, column=0)
        Entry_DestIPv6Addr = Entry(root49)
        Entry_DestIPv6Addr.grid(row=10, column=1)
        Entry_DestIPv6Addr.delete(0, "end")
        Entry_DestIPv6Addr.insert(0, "2000::1")
        Label_DestIPv6AddrGateway = Label(root49, text='Dest IPv6 Address Gateway:')
        Label_DestIPv6AddrGateway.grid(row=11, column=0)
        Entry_DestIPv6Gateway = Entry(root49)
        Entry_DestIPv6Gateway.grid(row=11, column=1)
        Entry_DestIPv6Gateway.delete(0, "end")
        Entry_DestIPv6Gateway.insert(0, "2000::1")

        Label_SrcUDPPort = Label(root49, text='Src UDP Port:')
        Label_SrcUDPPort.grid(row=12, column=0)
        Entry_SrcUDPPort = Entry(root49)
        Entry_SrcUDPPort.grid(row=12, column=1)
        Entry_SrcUDPPort.delete(0, "end")
        Entry_SrcUDPPort.insert(0, "1024")

        Label_SrcUDPPortIsModifier = Label(root49, text='Src UDP Port是否可变:')
        Label_SrcUDPPortIsModifier.grid(row=13, column=0)
        EnableList = [True, False]

        Combobox_SrcUDPPortIsModifier = Combobox(root49)
        Combobox_SrcUDPPortIsModifier["value"] = EnableList
        Combobox_SrcUDPPortIsModifier.grid(row=13, column=1)
        Label_SrcUDPPortModifierCount = Label(root49, text='Src UDP Port Modifier Count:')
        Label_SrcUDPPortModifierCount.grid(row=14, column=0)
        Entry_SrcUDPPortModifierCount = Entry(root49)
        Entry_SrcUDPPortModifierCount.grid(row=14, column=1)
        Entry_SrcUDPPortModifierCount.delete(0, "end")
        Entry_SrcUDPPortModifierCount.insert(0, "1")
        Label_SrcUDPPortModifierStep = Label(root49, text='Src UDP Port Modifier Step:')
        Label_SrcUDPPortModifierStep.grid(row=15, column=0)
        Entry_SrcUDPPortModifierStep = Entry(root49)
        Entry_SrcUDPPortModifierStep.grid(row=15, column=1)
        Entry_SrcUDPPortModifierStep.delete(0, "end")
        Entry_SrcUDPPortModifierStep.insert(0, "1")
        Label_SrcUDPPortModifierMask = Label(root49, text='Src UDP Port Modifier Mask:')
        Label_SrcUDPPortModifierMask.grid(row=16, column=0)
        Entry_SrcUDPPortModifierMask = Entry(root49)
        Entry_SrcUDPPortModifierMask.grid(row=16, column=1)
        Entry_SrcUDPPortModifierMask.delete(0, "end")
        Entry_SrcUDPPortModifierMask.insert(0, "65535")

        Label_DestUDPPort = Label(root49, text='Dest UDP Port:')
        Label_DestUDPPort.grid(row=17, column=0)
        Entry_DestUDPPort = Entry(root49)
        Entry_DestUDPPort.grid(row=17, column=1)
        Entry_DestUDPPort.delete(0, "end")
        Entry_DestUDPPort.insert(0, "1024")

        Label_DestUDPPortIsModifier = Label(root49, text='Dest UDP Port是否可变:')
        Label_DestUDPPortIsModifier.grid(row=18, column=0)

        Combobox_DestUDPPortIsModifier = Combobox(root49)
        Combobox_DestUDPPortIsModifier["value"] = EnableList
        Combobox_DestUDPPortIsModifier.grid(row=18, column=1)
        Label_DestUDPPortModifierCount = Label(root49, text='Dest UDP Port Modifier Count:')
        Label_DestUDPPortModifierCount.grid(row=19, column=0)
        Entry_DestUDPPortModifierCount = Entry(root49)
        Entry_DestUDPPortModifierCount.grid(row=19, column=1)
        Entry_DestUDPPortModifierCount.delete(0, "end")
        Entry_DestUDPPortModifierCount.insert(0, "1")
        Label_DestUDPPortModifierStep = Label(root49, text='Dest UDP Port Modifier Step:')
        Label_DestUDPPortModifierStep.grid(row=20, column=0)
        Entry_DestUDPPortModifierStep = Entry(root49)
        Entry_DestUDPPortModifierStep.grid(row=20, column=1)
        Entry_DestUDPPortModifierStep.delete(0, "end")
        Entry_DestUDPPortModifierStep.insert(0, "1")
        Label_DestUDPPortModifierMask = Label(root49, text='Dest UDP Port Modifier Mask:')
        Label_DestUDPPortModifierMask.grid(row=21, column=0)
        Entry_DestUDPPortModifierMask = Entry(root49)
        Entry_DestUDPPortModifierMask.grid(row=21, column=1)
        Entry_DestUDPPortModifierMask.delete(0, "end")
        Entry_DestUDPPortModifierMask.insert(0, "65535")

        button_createUDPv6Pkt = Button(root49, text='创建UDPv6流量', command=button_StreamCreate_UDPv6_Custom)
        button_createUDPv6Pkt.grid(row=22, column=0)

        root49.title("TestMaster UDPv6 Custom流量创建")
        root49.geometry('800x600')

        root49.mainloop()

    # def star(self):
    #     init_window = tk.Tk()  # 实例化出一个父窗口
    #     mirror_gui = testMasterStreamCreate(init_window)
    #     mirror_gui.set_init_window()
    #     init_window.mainloop()

# if __name__ == '__main__':
#     init_window = tk.Tk()  # 实例化出一个父窗口
#     mirror_gui = testMasterStreamCreate(init_window)
#     mirror_gui.set_init_window()
#     init_window.mainloop()

# test = testMasterStreamCreate()
#
# ss = test.set_init_window()
# print(ss)

