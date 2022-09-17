# -*- coding: utf-8 -*-
import re
import os
from operatemtputty import Operatemtputty
from operator import itemgetter


class PublicMeth():
    def __init__(self):
        self.operatemtputty = Operatemtputty()

    def rmdup(self, list):
        list_temp = set()
        for data in list:
            list_temp.add(data)
        return list_temp

    def getrelationship2(self, list):
        lst1 = list[0]
        lst2 = list[1]
        if re.compile("\|\s*in").findall(lst1) and re.compile("\|\s*in").findall(lst2):
            lst1_include = re.sub(re.compile(".*\s*\|\s*in[a-z]*\s*"), "", lst1)
            lst1_include = re.sub(re.compile('"'), "", lst1_include)
            lst1_dis = re.sub(re.compile("\s*\|\s*in[a-z]*\s*.*"), "",
                              lst1)
            lst2_include = re.sub(re.compile(".*\s*\|\s*in[a-z]*\s*"), "", lst2)
            lst2_include = re.sub(re.compile('"'), "", lst2_include)
            lst2_dis = re.sub(re.compile("\s*\|\s*in[a-z]*\s*.*"), "",
                              lst2)
            if lst1_dis == lst2_dis and lst1_include != lst2_include:
                return 1
            elif lst1_dis != lst2_dis and lst1_include != lst2_include:
                if re.compile(lst1_include).findall(lst2_include):
                    if re.compile(':').findall(lst1_include):
                        return 3
                    else:
                        return 4
                else:
                    return 99
            else:
                return 99
        elif re.compile("\|\s*in").findall(lst1):
            return 99
        else:
            return 99

    def dealdate(self, data):
        data = data.split(" ")
        if data[0] == "Jan":
            data = '01/' + data[1] + " " + data[2]
            return data
        elif data[0] == "Feb":
            data = '02/' + data[1] + " " + data[2]
            return data
        elif data[0] == "Mar":
            data = '03/' + data[1] + " " + data[2]
            return data
        elif data[0] == "Apr":
            data = '04/' + data[1] + " " + data[2]
            return data
        elif data[0] == "May":
            data = '05/' + data[1] + " " + data[2]
            return data
        elif data[0] == "Jun":
            data = '06/' + data[1] + " " + data[2]
            return data
        elif data[0] == "Jul":
            data = '07/' + data[1] + " " + data[2]
            return data
        elif data[0] == "Aug":
            data = '08/' + data[1] + " " + data[2]
            return data
        elif data[0] == "Sep":
            data = '09/' + data[1] + " " + data[2]
            return data
        elif data[0] == "Oct":
            data = '10/' + data[1] + " " + data[2]
            return data
        elif data[0] == "Nov":
            data = '11/' + data[1] + " " + data[2]
            return data
        elif data[0] == "Dec":
            data = '12/' + data[1] + " " + data[2]
            return data

    def getconfig(self, filepath):
        result_data = []
        for path, dirlist, filelist in os.walk(filepath):
            for filename in filelist:
                txtname = filepath + filename
                filetype_info = re.compile('info.log').findall(filename)
                if filetype_info:
                    comand = open(txtname, encoding='utf-8')
                    lines = comand.read()
                    configlist = re.compile("[a-zA-Z]{3,4}\s*\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}.*Command is.*").findall(lines)
                    if configlist:
                        for config in configlist:
                            date = re.compile("[a-zA-Z]{3,4}\s*\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}").findall(config)[0]
                            date = self.dealdate(date)
                            sysname = re.compile("\d{4}.*%%").findall(config)
                            sysname = re.sub(re.compile('\d{4}'), '', sysname[0])
                            sysname = re.sub(re.compile('%%'), '', sysname)
                            sysname = sysname.strip()
                            command = re.compile("Command is.*").findall(config)
                            command = re.sub(re.compile('Command is'), '', command[0])
                            result_data.append({
                                'sysname': sysname,
                                'dut': sysname,
                                'viewlist_num': 1,
                                'viewlist': 'none',
                                'time': date,
                                'config': command
                            })
                    else:
                        self.operatemtputty.popwarningwin("没有任何配置数据，请检查log文件是否有配置数据")

        result_data.sort(key=itemgetter('time'))
        # print(result_data)
        return result_data

    def compare_list(self, before_list, after_list):
        before_list_len = len(before_list)
        after_list_len = len(after_list)
        # compare_data = []
        # after_list = mat(after_list)
        if before_list_len >= after_list_len:
            return 0
        else:
            print(after_list[before_list_len:])
            compare_data = after_list[before_list_len:]
            return compare_data

    def return_config(self, compare_data):
        return_config = ""
        config_data = []
        dutlist = []
        checkdatelist = []
        checknumlist = []
        checklist = []
        tempconfig_data = {}
        id = 1
        configdate = ''
        if compare_data:
            for i, k in enumerate(compare_data):
                viewlist = k.get('viewlist')
                date = k.get('time')
                dut = k.get('dut')
                viewlist_num = k.get('viewlist_num')
                '''
                check类型配置：check_num = 0 为command check
                check_num = 1 为ping check
                check_num = 2 为packet-capture抓包check
                check_num = 3 为dir查看文件check
                check_num = 4 为tracert查看文件check
                check_num = 5 为校验debug信息
                check_num = 6 为校验trap信息
                check_num = 7 为check联想信息
                check_num = 8 为check syslog信息
                check_num = 9 为check 视图
                check_num = 99 为当前命令为display不带include，下条命令是display带include
                '''
                disItem = re.compile("^dis").findall(k.get("config").lstrip())
                includecheck = re.compile("include").findall(k.get("config"))
                ping_check = re.compile('^ping').findall(k.get('config').lstrip())
                tracert_check = re.compile('tracert').findall(k.get('config'))
                iproot_check = re.compile('peer').findall(k.get('config'))
                capture_check = re.compile('^packet-capture interface').findall(' '.join(k.get('config').split()))
                dir_check = re.compile('^dir').findall(k.get('config').lstrip())
                debug_check = re.compile('^debug').findall(k.get('config').lstrip())

                # 确定是否为check项
                if disItem or ping_check or capture_check or dir_check or tracert_check or debug_check or viewlist_num == 199:
                    # display 显示类信息流程处理
                    if disItem:
                        if re.compile("\|\s*in").findall(k.get("config")) or re.compile("\|\s*ex").findall(k.get("config")):
                            if re.compile("trap:").findall(k.get("config")):
                                dutlist.append(dut)
                                checkdatelist.append(date)
                                checknumlist.append(6)
                                checklist.append(k.get('config'))
                            elif re.compile("\^").findall(k.get("config")):
                                dutlist.append(dut)
                                checkdatelist.append(date)
                                checknumlist.append(7)
                                checklist.append(k.get('config'))
                            elif re.compile("syslog:").findall(k.get("config")):
                                dutlist.append(dut)
                                checkdatelist.append(date)
                                checknumlist.append(8)
                                checklist.append(k.get('config'))
                            elif re.compile("view:").findall(k.get("config")):
                                dutlist.append(dut)
                                checkdatelist.append(date)
                                checknumlist.append(9)
                                checklist.append(k.get('config'))

                            else:
                                # test_in = re.compile("\|\s*in").findall(k.get("config"))
                                # test_ex = re.compile("\|\s*ex").findall(k.get("config"))
                                # print(test_in)
                                # print(test_ex)
                                dutlist.append(dut)
                                checkdatelist.append(date)
                                checknumlist.append(0)
                                checklist.append(k.get('config'))
                        # display不带include命令处理逻辑
                        else:
                            # 判断是不是最后一条命令
                            if len(compare_data) != (i + 1):
                                next_data = compare_data[i + 1]
                                # 判断下一条命令是不是dis 相关
                                if re.compile("^dis").findall(next_data.get("config").lstrip()):
                                    # 下条命令是否带include或者exclude
                                    if re.compile("\|\s*in").findall(next_data.get("config")) or re.compile("\|\s*ex").findall(next_data.get("config")):
                                        dutlist.append(dut)
                                        checkdatelist.append(date)
                                        checknumlist.append(99)
                                        checklist.append(k.get('config'))
                                    # 下条命令不带include或者exclude，是一条正常的display命令
                                    else:
                                        continue
                                # 下条命令不带display
                                else:
                                    continue
                            # 最后一条命令
                            else:
                                continue

                    if dir_check:
                        if re.compile("include").findall(k.get("config")) or re.compile("exclude").findall(k.get("config")):
                            dutlist.append(dut)
                            checkdatelist.append(date)
                            checknumlist.append(3)
                            checklist.append(k.get('config'))
                    if capture_check:
                        dutlist.append(dut)
                        checkdatelist.append(date)
                        checknumlist.append(2)
                        checklist.append(k.get('config'))
                    if ping_check:
                        dutlist.append(dut)
                        checkdatelist.append(date)
                        checknumlist.append(1)
                        checklist.append(k.get('config'))
                    if tracert_check:
                        dutlist.append(dut)
                        checkdatelist.append(date)
                        checknumlist.append(4)
                        checklist.append(k.get('config'))
                    if debug_check:
                        dutlist.append(dut)
                        checkdatelist.append(date)
                        checknumlist.append(5)
                        checklist.append(k.get('config'))

                    if viewlist_num == 199:
                        dutlist.append(dut)
                        checkdatelist.append(date)
                        checknumlist.append(199)
                        checklist.append(k.get('config'))
                # 非check配置逻辑
                else:
                    if checklist:
                        if tempconfig_data:
                            config_data.append({
                                'step': id,
                                'dut': dutlist,
                                'check_num': checknumlist,
                                'checkdate': checkdatelist,
                                'configdate': configdate,
                                'check': checklist,
                                'config_num': 0,
                                'config': tempconfig_data
                            })
                            tempconfig_data = {}
                            dutlist = []
                            checkdatelist = []
                            checknumlist = []
                            checklist = []
                            id = id + 1
                        else:
                            config_data.append({
                                'step': id,
                                'dut': dutlist,
                                'check_num': checknumlist,
                                'checkdate': checkdatelist,
                                'check': checklist
                            })
                            dutlist = []
                            checkdatelist = []
                            checknumlist = []
                            checklist = []
                            id = id + 1
                    configdate = date
                    if (k.get("dut")) in tempconfig_data:
                        # if tempconfig_data.has_key('DUT' + index):   #python2.7用法
                        tempconfig_data[k.get("dut")] = tempconfig_data[k.get("dut")] + '\n' + k.get('config')
                    else:
                        tempconfig_data[k.get("dut")] = k.get("config")

            if checklist:
                if tempconfig_data:
                    config_data.append({
                        'step': id,
                        'dut': dutlist,
                        'check_num': checknumlist,
                        'checkdate': checkdatelist,
                        'configdate': configdate,
                        'check': checklist,
                        'config_num': 0,
                        'config': tempconfig_data
                    })
                    tempconfig_data = {}
                    dutlist = []
                    checkdatelist = []
                    checknumlist = []
                    checklist = []
                    id = id + 1
                else:
                    config_data.append({
                        'step': id,
                        'dut': dutlist,
                        'check_num': checknumlist,
                        'checkdate': checkdatelist,
                        'check': checklist
                    })
                    dutlist = []
                    checkdatelist = []
                    checknumlist = []
                    checklist = []
                    id = id + 1
            # print(config_data)
            if tempconfig_data:
                for key, value in tempconfig_data.items():
                    dutlist.append(dut)
                config_data.append({
                    'step': id,
                    'dut': dutlist,
                    'check_num': [99],
                    'check': ['none'],
                    'config_num': 0,
                    'config': tempconfig_data
                })
                id = id + 1

        for j in config_data:
            temp_step = j.get('step')
            temp_dut = j.get('dut')
            temp_check = j.get('check')
            temp_check_num = j.get('check_num')
            temp_check_date = j.get('checkdate')
            # if j.has_key('config'):  #python2.7用法
            if 'config' in j:
                temp_config = j.get('config')  # 返回是字典
                for key in temp_config:
                    configlist = temp_config.get(key).split('\n')
                    temp_setconfig = ''
                    for setconfig in configlist:
                        #  将install封装成tcl函数
                        if re.compile('install').findall(setconfig):
                            setconfig_list = setconfig.split()
                            installconfig = 'setInstallActivate'
                            if temp_setconfig:
                                config = '{DUT} Config "\n{temconfig}	"\n'.format(
                                    DUT=key, temconfig=temp_setconfig)
                                temp_setconfig = ''
                                for index, value in enumerate(setconfig_list):
                                    if value == "boot":
                                        installconfig = installconfig + '-bootfile' + setconfig_list[index + 1]
                                    if value == "system":
                                        installconfig = installconfig + '-systemfile' + setconfig_list[index + 1]
                                    if value == "feature":
                                        installconfig = installconfig + '-featurefile' + setconfig_list[index + 1]
                                    if value == "patch":
                                        installconfig = installconfig + '-patchfile' + setconfig_list[index + 1]
                                    if value == "slot":
                                        installconfig = installconfig + '-slot' + setconfig_list[index + 1]
                                    if value == "chassis":
                                        installconfig = installconfig + '-chassis' + setconfig_list[index + 1]
                                    if value == "test":
                                        installconfig = installconfig + '-testFlag' + '1'
                                config = '  {DUT} Config "\n{temconfig}	"\n'.format(
                                    DUT=key, temconfig=installconfig)
                            else:
                                for index, value in enumerate(setconfig_list):
                                    if value == "boot":
                                        installconfig = installconfig + '-bootfile' + setconfig_list[index + 1]
                                    if value == "system":
                                        installconfig = installconfig + '-systemfile' + setconfig_list[index + 1]
                                    if value == "feature":
                                        installconfig = installconfig + '-featurefile' + setconfig_list[index + 1]
                                    if value == "patch":
                                        installconfig = installconfig + '-patchfile' + setconfig_list[index + 1]
                                    if value == "slot":
                                        installconfig = installconfig + '-slot' + setconfig_list[index + 1]
                                    if value == "chassis":
                                        installconfig = installconfig + '-chassis' + setconfig_list[index + 1]
                                    if value == "test":
                                        installconfig = installconfig + '-testFlag' + '1'
                                config = '{DUT} Config "\n{temconfig}	"\n'.format(
                                    DUT=key, temconfig=installconfig)
                        else:
                            temp_setconfig = temp_setconfig + '\n' + '\t\t' + setconfig
                    if temp_setconfig:
                        config = '\t{DUT} Config "\n{temconfig}	"\n'.format(
                            DUT=key, temconfig=temp_setconfig)
            return_config = return_config + "\n" + config
        return return_config
