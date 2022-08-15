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
            lst1_include =  re.sub(re.compile('"'), "", lst1_include)
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
        elif data[0] == "Sept":
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
                    configlist = re.compile("\d{1,2}:\d{1,2}:\d{1,2}.*Command is.*").findall(lines)
                    if configlist:
                        for config in configlist:
                            date = re.compile("[a-zA-Z]{3,4}\s*\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}").findall(config)[0]
                            date = self.dealdate(date)
                            sysname = re.compile("\d{4}.*%%").findall(config)
                            sysname =  re.sub(re.compile('\d{4}'), '', sysname[0])
                            sysname = re.sub(re.compile('%%'), '', sysname)
                            sysname =  sysname.strip()
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
        print(result_data)
        return result_data





# ss = PublicMeth()
# ss.getcfgcommand('D:\魔镜脚本开发系统\Git\magic_mirror\configfile')
# ss.getconfig("C:/Users/l18630/AppData/Local/Temp/")