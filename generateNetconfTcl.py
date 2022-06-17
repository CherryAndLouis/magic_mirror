# -*- coding: utf-8 -*-
#修改考虑一次性给多个log，输出多个脚本
import re
import os.path
from operator import itemgetter
from operatemtputty import Operatemtputty

class generateNetconfTcl:


    #def bianli():


    def __init__(self, filepath="./log/", result_file="./Scheduler_ScheduleRepeats.tcl"):
        self.filepath = filepath
        self.result_file = result_file
        self.operatemtputty = Operatemtputty()
        self.operatemtputty.del_notutf_8('./log')

    # 获取log名称中相关信息
    def getmodelname(self, modename='no_modename', tablename='no_tablename'):
        for path, dirlist, filelist in os.walk(self.filepath):

            for filename in filelist:
                #txtname = self.filepath + filename
                filetype_l = re.compile('.log').findall(filename)
                #filetype_t = re.compile('.topo').findall(filename)
                print(filename)
                if filetype_l:
                    if re.compile('_').findall(filename):
                        a = filename.split("_")
                        modename = a[0]
                        tablename = a[1]

        return modename, tablename


    # 处理日志
    def disposelog(self):
        result_data = []
        print_data = []
        configreturn = []
        partten_norule = "\[\d{4}(?:-|\/|.)\d{1,2}(?:-|\/|.)\d{1,2}\s\d{1,2}\:\d{1,2}\:\d{1,2}\]\s.*"
        patten_allitem = re.compile("\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]\s[<\[]{1}.*[>\]]{1}.*")
        patten_sysnameitem = re.compile("[<\[>\]]{1}")
        #('%[A-Za-z]*\s*\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3}\s\d{4}\sH3C\sXMLSOAP.*') 原先是H3C，考虑到sysname有其他名，直接模糊匹配
        # partten_print = re.compile('%[A-Za-z]*\s*\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3}\s\d{4}\s*.*\s*XMLSOAP.*') #grep xmlsoap 标签
        partten_print = re.compile('%[A-Za-z]*\s*\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3}\s\d{4}\s*.*')
        partten_mainitem = re.compile("\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]\s[<\[]{1}.*[>\]]{1}")
        for path, dirlist, filelist in os.walk(self.filepath):
            for filename in filelist:
                txtname = self.filepath + filename
                filetype_l = re.compile('.log').findall(filename)
                if filetype_l:
                    comand = open(txtname, encoding='utf-8')
                    lines = comand.read()
                    logbufferitem = re.compile("\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]\s%.*;\sCommand\sis\s.*").findall(lines)
                    logbufferlist = []
                    for logbuffer in logbufferitem:
                        logbufferlist.append(
                            re.sub(re.compile("\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]\s%.*;\sCommand\sis\s"), "", logbuffer))
                    noruleItem = re.compile(partten_norule).findall(lines)
                    allItem = patten_allitem.findall(lines)
                    sysName_f = re.compile("^[A-Za-z0-9\-]*").findall(filename)
                    sysName = re.sub(patten_sysnameitem, '', re.sub(re.compile(
                        "\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]"), "", partten_mainitem.findall(allItem[0])[0]))
                    #print(sysName)
                    for item in noruleItem:
                        incSysname = patten_allitem.findall(item)
                        printItem = partten_print.findall(item)

                        date = re.sub(re.compile('[\[\]]{1}'), "", re.compile(
                            "\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]").findall(
                            item)[
                            0])
                        if not printItem:
                            if incSysname:
                                allItem_1 = re.sub(partten_mainitem, "",
                                                   incSysname[0])
                                if allItem_1:
                                    ques_item = re.compile('\?').findall(allItem_1)
                                    if not ques_item:
                                        if logbufferlist:
                                            if ' '.join(allItem_1.split()) in logbufferlist:
                                                viewlist = re.sub(
                                                    re.compile('[\[<>\]]{1}'), '',
                                                    re.compile(
                                                        '[<\[]{1}.*[>\]]{1}').findall(
                                                        re.sub(re.compile(
                                                            "\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]"),
                                                            '', item))[0]).split("-")
                                                if re.compile(
                                                        '[\[]{1}.*[]]{1}').findall(
                                                    re.sub(re.compile(
                                                        "\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]"),
                                                        '', item)):
                                                    # print(viewlist)
                                                    result_data.append({
                                                        'sysname': sysName,
                                                        'dut': sysName_f[0],
                                                        'viewlist_num': 1,
                                                        'viewlist': viewlist,
                                                        'time': date,
                                                        'config': allItem_1
                                                    })
                                                else:
                                                    result_data.append({
                                                        'sysname': sysName,
                                                        'dut': sysName_f[0],
                                                        'viewlist_num': 0,
                                                        'viewlist': viewlist,
                                                        'time': date,
                                                        'config': allItem_1
                                                    })
                                            # 此逻辑为不在logbuffer中命令
                                            else:
                                                continue
                                        # 此逻辑为没有logbuffer相关命令行
                                        else:
                                            # self.operatemtputty.popwarningwin('Log Winthout Logbuffer Config')
                                            # print('Log Winthout Logbuffer Config')
                                            viewlist = re.sub(
                                                re.compile('[\[<>\]]{1}'), '',
                                                re.compile(
                                                    '[<\[]{1}.*[>\]]{1}').findall(
                                                    re.sub(re.compile(
                                                        "\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]"),
                                                        '', item))[0]).split("-")
                                            # print(viewlist)
                                            if re.compile(
                                                    '[\[]{1}.*[]]{1}').findall(
                                                re.sub(re.compile(
                                                    "\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]"),
                                                    '', item)):
                                                # print(viewlist)
                                                result_data.append({
                                                    'sysname': sysName,
                                                    'dut': sysName_f[0],
                                                    'viewlist_num': 1,
                                                    'viewlist': viewlist,
                                                    'time': date,
                                                    'config': allItem_1
                                                })
                                            else:
                                                result_data.append({
                                                    'sysname': sysName,
                                                    'dut': sysName_f[0],
                                                    'viewlist_num': 0,
                                                    'viewlist': viewlist,
                                                    'time': date,
                                                    'config': allItem_1
                                                })
                                    # 保留，此逻辑为带？联想命令行
                                    else:
                                        continue
                                else:
                                    continue
                            # 不带视图日志操作
                            else:
                                mainItem = re.sub(
                                    re.compile(
                                        '\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]\s'),
                                    "",
                                    item)
                                bashItem = re.compile('[$#]{1}').findall(mainItem)
                                if bashItem:
                                    bashconfig = re.sub(re.compile('[$#]{1}\s'),
                                                        "", mainItem)
                                    if re.sub(re.compile('[$#]{1}'),
                                              "", mainItem):
                                        result_data.append({
                                            'sysname': sysName,
                                            'dut': sysName_f[0],
                                            'viewlist_num': 99,
                                            'viewlist': ['bash'],
                                            'time': date,
                                            'config': bashconfig
                                        })
                                # 保留，此逻辑为命令行返回的信息
                                else:
                                    configreturn.append({
                                        'sysname': sysName,
                                        'dut': sysName_f[0],
                                        'viewlist_num': 98,
                                        'viewlist': ['configreturn'],
                                        'time': date,
                                        'config': mainItem
                                    })
                                    continue
                        # 保留，此逻辑为打印信息
                        else:
                            print_data.append({
                                #'sysname': sysName,
                                #'dut': sysName_f[0],
                                #'viewlist_num': 99,
                                #'viewlist': ['print'],
                                'time': date,
                                'config': printItem[0]
                            })
                    comand.close()
        result_data.sort(key=itemgetter('time'))
        print_data.sort(key=itemgetter('time'))

        return result_data, print_data, configreturn

    def getnetconflog(self):
        netconfdata = []
        # patten_netconflog = re.compile("%[A-Za-z]*\s*\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3}\s\d{4}\s*([^%]*)</rpc>")
        patten_netconflog = re.compile("(?:\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}]\s*[[<\[]*.*[>\]]*]*%[A-Za-z]*\s*\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3}\s\d{4}\s*)(?:[^%]*)(?:</rpc>)")
        # patten_netconflog = re.compile(
            # "\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}]\s*[[<\[]*.*[>\]]*]*%[A-Za-z]*\s*\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3}\s\d{4}\s*")
        for path, dirlist, filelist in os.walk(self.filepath):
            for filename in filelist:
                txtname = self.filepath + filename
                filetype_l = re.compile('.log').findall(filename)
                if filetype_l:
                    comand = open(txtname, encoding='utf-8')
                    lines = comand.read()
                    netconflog = patten_netconflog.findall(lines)
                    if netconflog:
                        for log in netconflog:
                            # log = log[0]+log[1]+log[2]
                            date = re.sub(re.compile('[\[\]]{1}'), "", re.compile(
                                "\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]").findall(
                                log)[
                                0])
                            log = ''.join(log.split('\n'))
                            log = re.sub(re.compile('\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}]\s*'), '', log)
                            netconfdata.append({
                                'time': date,
                                'config': log
                            })
                    comand.close()
        netconfdata.sort(key=itemgetter('time'))
        return netconfdata

    def creattcl(self):
        print_data = self.getnetconflog()
        # print(print_data)
        modename, tablename = self.getmodelname()
        result_file_o = open(self.result_file, mode='w+')
        header = 'SET_RUNNING_PARAM if_address 1 open_mode 1\n<TESTCASE_BEGIN>\n<TESTCASE_HEADER_BEGIN>\n    <TITLE>      "自动化生成脚本"\n    <INDEX>      "x.x.x"\n    <LEVEL>      "2"\n    <WEIGHT>     "4"\n    <MODULE>     "{mode}"\n    <TYPE>       "NETCONF"\n    <AUTHOR>     "Automatic Generation"\n    <LIMITATION> "CmwV7Device"\n    <VERSION>    "2.1"\n    <DESIGN>     "netconf自动化脚本"\n    <SOURCE>     "netconf_rpc_1.topo"\n<TESTCASE_HEADER_END>\n\n<TESTCASE_DEVICE_MAP_BEGIN>\n\n<TESTCASE_DEVICE_MAP_END>\n'.format(
            mode=modename)
        # header = 'SET_RUNNING_PARAM if_address 1 open_mode 1\n<TESTCASE_BEGIN>\n<TESTCASE_HEADER_BEGIN>\n    <TITLE>      "自动化生成脚本"\n    <INDEX>      "x.x.x"\n    <LEVEL>      "2"\n    <WEIGHT>     "4"\n    <MODULE>     "mode"\n    <TYPE>       "NETCONF"\n    <AUTHOR>     "Automatic Generation"\n    <LIMITATION> "CmwV7Device"\n    <VERSION>    "2.1"\n    <DESIGN>     "netconf自动化脚本"\n    <SOURCE>     "netconf_rpc_1.topo"\n<TESTCASE_HEADER_END>\n\n<TESTCASE_DEVICE_MAP_BEGIN>\n\n<TESTCASE_DEVICE_MAP_END>\n'

        xmlhellorpc = '"<hello xmlns=\\"urn:ietf:params:xml:ns:netconf:base:1.0\\"><capabilities><capability>urn:ietf:params:netconf:base:1.0</capability></capabilities></hello>\]\]>\]\]>"'
        xmlcloserpc = '"<rpc message-id=\\"100\\" xmlns=\\"urn:ietf:params:xml:ns:netconf:base:1.0\\"><close-session/></rpc>\]\]>\]\]>"'
        preconfig = '\tset xmlhello ' + xmlhellorpc + '\n\tset xmlclose ' + xmlcloserpc + '\n\tDUT1 Config "telnet server enable \n\tnetconf ssh server enable\n\tline vty 0 63\n\tauthentication-mode none\n\tuser-role network-admin\n\tidle-timeout 0 0\n\tquit\n\tpassword-recovery enable\n\tundo password-control composition enable\n\tpassword-control length 4\n\tundo password-control complexity user-name check\n\tlocal-user admin class manage\n\tpassword simple admin\n\tservice-type ssh telnet http https\n\tauthorization-attribute user-role network-admin\n\tauthorization-attribute user-role network-operator\n\tquit\n\tquit"\n\tOpenTerm -name netconf -type telnet -addr $addr(DUT1,PORT1) -port 23\n\tafter 3000\n\n\n\t##########部分对象须提前命令行配置的请在此处下发############\n\tDUT1 Config ""\n\n'
        ender = '\n<TESTCASE_END>'

        stepstartofget = '<STEP> "验证netconf get功能" {\n'
        stepstartofgetbulk = '<STEP> "验证netconf getbulk功能" {\n'
        stepstartofgetconfig = '<STEP> "验证netconf getconfig功能" {\n'
        stepstartofgetbulkconfig = '<STEP> "验证netconf getbulkconfig功能" {\n'
        stepstartofmerge = '<STEP> "验证netconf merge功能" {\n'
        stepstartofcreate = '<STEP> "验证netconf create功能" {\n'
        stepstartofremove = '<STEP> "验证netconf remove功能" {\n'
        stepstartofdelete = '<STEP> "验证netconf delete功能" {\n'
        stepstartofreplace = '<STEP> "验证netconf replace功能" {\n'
        stepstartofaction = '<STEP> "验证netconf action功能" {\n'
        stepstartofcandidate = '<STEP> "验证netconf candidate功能" {\n'

        checkend = "\n}\n<CHECK>\n"
        stepend = "}\n"

        # 拼接脚本头和预配置
        result_file_o.write(header)
        result_file_o.write(preconfig)

        # 获取模块名  表名，考虑后不使用该方式获取模块名 表名，暂时注释
        '''for line in print_data:
            temp = line.get("config")
            if re.match('.*XML_REQUEST.*', temp) != None and re.match('.*operation="merge".*', temp) != None:
                rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                rpcxml = "".join(rpcxmltemp)

                startindex = rpcxml.index('"merge"><')
                endindex = rpcxml.index("></top>")
                tmp = rpcxml[startindex:endindex].split("></")
                feature = tmp[-1]
                tablename = tmp[-2]
            else:
                continue'''

        stepnum = 1
        tempxml = ""
        # 将print_data遍历 组织成测试步骤
        for line in print_data:
            # 获取键值
            temp = line.get("config")
            # print(temp)

            if re.match('.*XML_REQUEST.*', temp) != None and re.match('.*<candidate/>.*', temp) == None:

                # 提前转换成rpc报文进行重复检查，这样才能精确除重连续报文
                rpccheck = re.findall('<rpc.*rpc>', temp)
                # 剔除相连重复报文
                if tempxml == rpccheck:
                    continue
                tempxml = rpccheck
                # print(rpccheck)

                # 定义一个过滤字段，后续可以直接引用，修改时，只需修改此处即可
                # 20220601 新增 @._- 过滤
                filterField = ">[0-9a-zA-Z/@._-]+<"

                # 拼装running测试报文
                if re.match('.*<get>.*', temp) != None:
                    checkstart = '<CHECK> description "' + modename + '/' + tablename + ' get表操作"\n<CHECK> type custom\n<CHECK> args {\n'
                    rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                    rpcxml = "".join(rpcxmltemp)

                    a = str(stepnum)
                    result_file_o.write("#STEP" + a + "\n")
                    stepnum += 1

                    result_file_o.write(stepstartofget)
                    result_file_o.write(checkstart)

                    # 目前针对数字　字符　范围内的列值
                    sublist = re.compile(filterField).findall(rpcxml)
                    # c count t1 t2 ...都是作为中间变量 l lenth
                    c = 1
                    for i in sublist:
                        t1 = re.findall(filterField, i)
                        t2 = t1[-1]
                        l = len(t2)
                        t3 = t2[1:l - 1]

                        rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml, 1)
                        t4 = "part_{c}".format(c=c)
                        c = c + 1
                        result_file_o.write("\tset " + t4 + " " + t3 + "\n")

                    c = c - 1
                    list1 = "set lst " + '"' + "默认值 " + "$part_{c}".format(c=c) + '"'
                    rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"', '\\"')
                    checkbody0 = "\n\t#get类只校验默认值和合法值，若lst列表中出现$part_0，说明soap下发的报文没有携带过滤条件，所有列均为空下发。建议手工测试带过滤值。\n\t#$part_1 $part_2 $part_3等 为下发报文中的过滤值，现将其提取并放入对应变量中，缺省校验最后一个列值，可以自行调整。\n\t#因无法获知默认值情况，请修改以下 默认值 为实际默认值"

                    checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i } {\n\t\tset pass [lindex $lst $i]"

                    checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset getrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 <data></data>\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset getrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 <data></data>\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    # checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset getrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'

                    checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'

                    result_file_o.write(str(checkbody0))
                    result_file_o.write(str(checkbody1))
                    result_file_o.write(str(checkbody2))
                    result_file_o.write(str(checkbody3))
                    # result_file_o.write(str(checkbody4))
                    result_file_o.write(str(checkbody5))
                    result_file_o.write(checkend)
                    result_file_o.write(stepend)
                    result_file_o.write("\n\n\n")

                elif re.match('.*<get-bulk>.*', temp) != None:
                    checkstart = '<CHECK> description "' + modename + '/' + tablename + ' get-bulk表操作"\n<CHECK> type custom\n<CHECK> args {\n'
                    rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                    rpcxml = "".join(rpcxmltemp)

                    a = str(stepnum)
                    result_file_o.write("#STEP" + a + "\n")
                    stepnum += 1

                    result_file_o.write(stepstartofgetbulk)

                    result_file_o.write(checkstart)

                    # 目前针对数字　字符　范围内的列值
                    sublist = re.compile(filterField).findall(rpcxml)
                    # c count t1 t2 ...都是作为中间变量 l lenth
                    c = 1
                    for i in sublist:
                        t1 = re.findall(filterField, i)
                        t2 = t1[-1]
                        l = len(t2)
                        t3 = t2[1:l - 1]

                        rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml, 1)
                        t4 = "part_{c}".format(c=c)
                        c = c + 1
                        result_file_o.write("\tset " + t4 + " " + t3 + "\n")

                    c = c - 1
                    list1 = "set lst " + '"' + "默认值 " + "$part_{c}".format(c=c) + '"'
                    rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"', '\\"')

                    checkbody0 = "\n\t#get类只校验默认值和合法值，若lst列表中出现$part_0，说明soap下发的报文没有携带过滤条件，所有列均为空下发。建议手工测试带过滤值。\n\t#$part_1 $part_2 $part_3等 为下发报文中的过滤值，现将其提取并放入对应变量中，缺省校验最后一个列值，可以自行调整。\n\t#因无法获知默认值情况，请修改以下 默认值 为实际默认值"

                    checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i } {\n\t\tset pass [lindex $lst $i]"

                    checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset getbulkrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 <data></data>\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset getbulkrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 <data></data>\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    # checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset getbulkrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'

                    checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'

                    result_file_o.write(str(checkbody0))
                    result_file_o.write(str(checkbody1))
                    result_file_o.write(str(checkbody2))
                    result_file_o.write(str(checkbody3))
                    # result_file_o.write(str(checkbody4))
                    result_file_o.write(str(checkbody5))

                    result_file_o.write(checkend)
                    result_file_o.write(stepend)
                    result_file_o.write("\n\n\n")

                elif re.match('.*<get-config>.*', temp) != None:
                    checkstart = '<CHECK> description "' + modename + '/' + tablename + ' get-config表操作"\n<CHECK> type custom\n<CHECK> args {\n'
                    rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                    rpcxml = "".join(rpcxmltemp)

                    a = str(stepnum)
                    result_file_o.write("#STEP" + a + "\n")
                    stepnum += 1

                    result_file_o.write(stepstartofgetconfig)

                    result_file_o.write(checkstart)

                    # 目前针对数字　字符　范围内的列值
                    sublist = re.compile(filterField).findall(rpcxml)
                    # c count t1 t2 ...都是作为中间变量 l lenth
                    c = 1
                    for i in sublist:
                        t1 = re.findall(filterField, i)
                        t2 = t1[-1]
                        l = len(t2)
                        t3 = t2[1:l - 1]

                        rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml, 1)
                        t4 = "part_{c}".format(c=c)
                        c = c + 1
                        result_file_o.write("\tset " + t4 + " " + t3 + "\n")

                    c = c - 1
                    list1 = "set lst " + '"' + "默认值 " + "$part_{c}".format(c=c) + '"'
                    rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"', '\\"')

                    checkbody0 = "\n\t#get类只校验默认值和合法值，若lst列表中出现$part_0，说明soap下发的报文没有携带过滤条件，所有列均为空下发。建议手工测试带过滤值。\n\t#$part_1 $part_2 $part_3等 为下发报文中的过滤值，现将其提取并放入对应变量中，缺省校验最后一个列值，可以自行调整。\n\t#因无法获知默认值情况，请修改以下 默认值 为实际默认值"

                    checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i } {\n\t\tset pass [lindex $lst $i]"

                    checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset getconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 <data></data>\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset getconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 <data></data>\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    # checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset getconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'

                    checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'

                    result_file_o.write(str(checkbody0))
                    result_file_o.write(str(checkbody1))
                    result_file_o.write(str(checkbody2))
                    result_file_o.write(str(checkbody3))
                    # result_file_o.write(str(checkbody4))
                    result_file_o.write(str(checkbody5))

                    result_file_o.write(checkend)
                    result_file_o.write(stepend)
                    result_file_o.write("\n\n\n")

                elif re.match('.*<get-bulk-config>.*', temp) != None:
                    checkstart = '<CHECK> description "' + modename + '/' + tablename + ' get-bulk-config表操作"\n<CHECK> type custom\n<CHECK> args {\n'
                    rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                    rpcxml = "".join(rpcxmltemp)

                    a = str(stepnum)
                    result_file_o.write("#STEP" + a + "\n")
                    stepnum += 1

                    result_file_o.write(stepstartofgetbulkconfig)

                    result_file_o.write(checkstart)

                    # 目前针对数字　字符　范围内的列值
                    sublist = re.compile(filterField).findall(rpcxml)
                    # c count t1 t2 ...都是作为中间变量 l lenth
                    c = 1
                    for i in sublist:
                        t1 = re.findall(filterField, i)
                        t2 = t1[-1]
                        l = len(t2)
                        t3 = t2[1:l - 1]

                        rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml, 1)
                        t4 = "part_{c}".format(c=c)
                        c = c + 1
                        result_file_o.write("\tset " + t4 + " " + t3 + "\n")

                    c = c - 1
                    list1 = "set lst " + '"' + "默认值 " + "$part_{c}".format(c=c) + '"'
                    rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"', '\\"')

                    checkbody0 = "\n\t#get类只校验默认值和合法值，若lst列表中出现$part_0，说明soap下发的报文没有携带过滤条件，所有列均为空下发。建议手工测试带过滤值。\n\t#$part_1 $part_2 $part_3等 为下发报文中的过滤值，现将其提取并放入对应变量中，缺省校验最后一个列值，可以自行调整。\n\t#因无法获知默认值情况，请修改以下 默认值 为实际默认值"

                    checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i } {\n\t\tset pass [lindex $lst $i]"

                    checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset getbulkconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 <data></data>\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset getbulkconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 <data></data>\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    # checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset getbulkconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'

                    checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'

                    result_file_o.write(str(checkbody0))
                    result_file_o.write(str(checkbody1))
                    result_file_o.write(str(checkbody2))
                    result_file_o.write(str(checkbody3))
                    # result_file_o.write(str(checkbody4))
                    result_file_o.write(str(checkbody5))

                    result_file_o.write(checkend)
                    result_file_o.write(stepend)
                    result_file_o.write("\n\n\n")

                elif re.match('.*operation="merge".*', temp) != None:
                    checkstart = '<CHECK> description "' + modename + '/' + tablename + ' merge表操作"\n<CHECK> type custom\n<CHECK> args {\n'
                    rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                    rpcxml = "".join(rpcxmltemp)

                    a = str(stepnum)
                    result_file_o.write("#STEP" + a + "\n")
                    stepnum += 1

                    result_file_o.write(stepstartofmerge)

                    result_file_o.write(checkstart)

                    # 目前针对数字　字符　范围内的列值
                    sublist = re.compile(filterField).findall(rpcxml)
                    # c count t1 t2 ...都是作为中间变量 l lenth
                    c = 1
                    for i in sublist:
                        t1 = re.findall(filterField, i)
                        t2 = t1[-1]
                        l = len(t2)
                        t3 = t2[1:l - 1]

                        rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml, 1)
                        t4 = "part_{c}".format(c=c)
                        c = c + 1
                        result_file_o.write("\tset " + t4 + " " + t3 + "\n")

                    c = c - 1
                    list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
                    rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"', '\\"')
                    checkbody0 = "\n\t#$part_1 $part_2 $part_3等 为下发报文中的过滤值，现将其提取并放入对应变量中，缺省校验最后一个列值，可以自行调整。"
                    checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i } {\n\t\tset pass [lindex $lst $i]"

                    checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset mergegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $mergegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset mergegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $mergegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset mergegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $mergegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'

                    checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'

                    result_file_o.write(str(checkbody0))
                    result_file_o.write(str(checkbody1))
                    result_file_o.write(str(checkbody2))
                    result_file_o.write(str(checkbody3))
                    result_file_o.write(str(checkbody4))
                    result_file_o.write(str(checkbody5))

                    result_file_o.write(checkend)
                    result_file_o.write(stepend)
                    result_file_o.write("\n\n\n")

                elif re.match('.*operation="create".*', temp) != None:
                    checkstart = '<CHECK> description "' + modename + '/' + tablename + ' create表操作"\n<CHECK> type custom\n<CHECK> args {\n'
                    rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                    rpcxml = "".join(rpcxmltemp)

                    a = str(stepnum)
                    result_file_o.write("#STEP" + a + "\n")
                    stepnum += 1

                    result_file_o.write(stepstartofcreate)

                    result_file_o.write(checkstart)

                    # 目前针对数字　字符　范围内的列值
                    sublist = re.compile(filterField).findall(rpcxml)
                    # c count t1 t2 ...都是作为中间变量 l lenth
                    c = 1
                    for i in sublist:
                        t1 = re.findall(filterField, i)
                        t2 = t1[-1]
                        l = len(t2)
                        t3 = t2[1:l - 1]

                        rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml, 1)
                        t4 = "part_{c}".format(c=c)
                        c = c + 1
                        result_file_o.write("\tset " + t4 + " " + t3 + "\n")

                    c = c - 1
                    list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
                    rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"', '\\"')
                    checkbody0 = "\n\t#$part_1 $part_2 $part_3等 为下发报文中的过滤值，现将其提取并放入对应变量中，缺省校验最后一个列值，可以自行调整。"
                    checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i } {\n\t\tset pass [lindex $lst $i]"

                    checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset creategrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $creategrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok/Configuration already exists.\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset creategrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $creategrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok/Configuration already exists.\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset creategrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $creategrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok/Configuration already exists.\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'

                    checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'

                    result_file_o.write(str(checkbody0))
                    result_file_o.write(str(checkbody1))
                    result_file_o.write(str(checkbody2))
                    result_file_o.write(str(checkbody3))
                    result_file_o.write(str(checkbody4))
                    result_file_o.write(str(checkbody5))

                    result_file_o.write(checkend)
                    result_file_o.write(stepend)
                    result_file_o.write("\n\n\n")

                elif re.match('.*operation="replace".*', temp) != None:
                    checkstart = '<CHECK> description "' + modename + '/' + tablename + ' replace表操作"\n<CHECK> type custom\n<CHECK> args {\n'
                    rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                    rpcxml = "".join(rpcxmltemp)

                    a = str(stepnum)
                    result_file_o.write("#STEP" + a + "\n")
                    stepnum += 1

                    result_file_o.write(stepstartofreplace)

                    result_file_o.write(checkstart)

                    # 目前针对数字　字符　范围内的列值
                    sublist = re.compile(filterField).findall(rpcxml)
                    # c count t1 t2 ...都是作为中间变量 l lenth
                    c = 1
                    for i in sublist:
                        t1 = re.findall(filterField, i)
                        t2 = t1[-1]
                        l = len(t2)
                        t3 = t2[1:l - 1]

                        rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml, 1)
                        t4 = "part_{c}".format(c=c)
                        c = c + 1
                        result_file_o.write("\tset " + t4 + " " + t3 + "\n")

                    c = c - 1
                    list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
                    rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"', '\\"')
                    checkbody0 = "\n\t#$part_1 $part_2 $part_3等 为下发报文中的过滤值，现将其提取并放入对应变量中，缺省校验最后一个列值，可以自行调整。"
                    checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i } {\n\t\tset pass [lindex $lst $i]"

                    checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset replacegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $replacegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset replacegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $replacegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset replacegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $replacegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'

                    checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'

                    result_file_o.write(str(checkbody0))
                    result_file_o.write(str(checkbody1))
                    result_file_o.write(str(checkbody2))
                    result_file_o.write(str(checkbody3))
                    result_file_o.write(str(checkbody4))
                    result_file_o.write(str(checkbody5))

                    result_file_o.write(checkend)
                    result_file_o.write(stepend)
                    result_file_o.write("\n\n\n")

                elif re.match('.*operation="delete".*', temp) != None:
                    checkstart = '<CHECK> description "' + modename + '/' + tablename + ' delete表操作"\n<CHECK> type custom\n<CHECK> args {\n'
                    rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                    rpcxml = "".join(rpcxmltemp)

                    a = str(stepnum)
                    result_file_o.write("#STEP" + a + "\n")
                    stepnum += 1

                    result_file_o.write(stepstartofdelete)

                    result_file_o.write(checkstart)

                    # 目前针对数字　字符　范围内的列值
                    sublist = re.compile(filterField).findall(rpcxml)
                    # c count t1 t2 ...都是作为中间变量 l lenth
                    c = 1
                    for i in sublist:
                        t1 = re.findall(filterField, i)
                        t2 = t1[-1]
                        l = len(t2)
                        t3 = t2[1:l - 1]

                        rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml, 1)
                        t4 = "part_{c}".format(c=c)
                        c = c + 1
                        result_file_o.write("\tset " + t4 + " " + t3 + "\n")

                    c = c - 1
                    list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
                    rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"', '\\"')
                    checkbody0 = "\n\t#$part_1 $part_2 $part_3等 为下发报文中的过滤值，现将其提取并放入对应变量中，缺省校验最后一个列值，可以自行调整。"
                    checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i } {\n\t\tset pass [lindex $lst $i]"

                    checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset deletegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $deletegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok/Configuration does not exist.\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset deletegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $deletegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok/Configuration does not exist.\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset deletegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $deletegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok/Configuration does not exist.\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'

                    checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'

                    result_file_o.write(str(checkbody0))
                    result_file_o.write(str(checkbody1))
                    result_file_o.write(str(checkbody2))
                    result_file_o.write(str(checkbody3))
                    result_file_o.write(str(checkbody4))
                    result_file_o.write(str(checkbody5))

                    result_file_o.write(checkend)
                    result_file_o.write(stepend)
                    result_file_o.write("\n\n\n")

                elif re.match('.*operation="remove".*', temp) != None:
                    checkstart = '<CHECK> description "' + modename + '/' + tablename + ' remove表操作"\n<CHECK> type custom\n<CHECK> args {\n'
                    rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                    rpcxml = "".join(rpcxmltemp)

                    a = str(stepnum)
                    result_file_o.write("#STEP" + a + "\n")
                    stepnum += 1

                    result_file_o.write(stepstartofremove)

                    result_file_o.write(checkstart)

                    # 目前针对数字　字符　范围内的列值
                    sublist = re.compile(filterField).findall(rpcxml)
                    # c count t1 t2 ...都是作为中间变量 l lenth
                    c = 1
                    for i in sublist:
                        t1 = re.findall(filterField, i)
                        t2 = t1[-1]
                        l = len(t2)
                        t3 = t2[1:l - 1]

                        rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml, 1)
                        t4 = "part_{c}".format(c=c)
                        c = c + 1
                        result_file_o.write("\tset " + t4 + " " + t3 + "\n")

                    c = c - 1
                    list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
                    rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"', '\\"')
                    checkbody0 = "\n\t#$part_1 $part_2 $part_3等 为下发报文中的过滤值，现将其提取并放入对应变量中，缺省校验最后一个列值，可以自行调整。"
                    checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i } {\n\t\tset pass [lindex $lst $i]"

                    checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'

                    checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'

                    result_file_o.write(str(checkbody0))
                    result_file_o.write(str(checkbody1))
                    result_file_o.write(str(checkbody2))
                    result_file_o.write(str(checkbody3))
                    result_file_o.write(str(checkbody4))
                    result_file_o.write(str(checkbody5))

                    result_file_o.write(checkend)
                    result_file_o.write(stepend)
                    result_file_o.write("\n\n\n")

                elif re.match('.*<action>.*', temp) != None:
                    checkstart = '<CHECK> description "' + modename + '/' + tablename + ' action操作"\n<CHECK> type custom\n<CHECK> args {\n'
                    rpcxmltemp = re.findall('<rpc.*rpc>', temp)
                    rpcxml = "".join(rpcxmltemp)

                    a = str(stepnum)
                    result_file_o.write("#STEP" + a + "\n")
                    stepnum += 1

                    result_file_o.write(stepstartofaction)

                    result_file_o.write(checkstart)

                    # 目前针对数字　字符　范围内的列值
                    sublist = re.compile(filterField).findall(rpcxml)
                    # c count t1 t2 ...都是作为中间变量 l lenth
                    c = 1
                    for i in sublist:
                        t1 = re.findall(filterField, i)
                        t2 = t1[-1]
                        l = len(t2)
                        t3 = t2[1:l - 1]

                        rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml, 1)
                        t4 = "part_{c}".format(c=c)
                        c = c + 1
                        result_file_o.write("\tset " + t4 + " " + t3 + "\n")

                    c = c - 1
                    list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
                    rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"', '\\"')
                    checkbody0 = "\n\t#$part_1 $part_2 $part_3等 为下发报文中的过滤值，现将其提取并放入对应变量中，缺省校验最后一个列值，可以自行调整。"
                    checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i } {\n\t\tset pass [lindex $lst $i]"

                    checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
                    checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请将xxx替换为需要检查的内容，例如 ok\n\t\t\tif {[string first "xxx" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'

                    checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'

                    result_file_o.write(str(checkbody0))
                    result_file_o.write(str(checkbody1))
                    result_file_o.write(str(checkbody2))
                    result_file_o.write(str(checkbody3))
                    result_file_o.write(str(checkbody4))
                    result_file_o.write(str(checkbody5))

                    result_file_o.write(checkend)
                    result_file_o.write(stepend)
                    result_file_o.write("\n\n\n")

        # 拼接脚本尾
        result_file_o.write(ender)
        result_file_o.close()

# 生成tcl
    # def creattcl(self):
    #     getnetconflog = self.getnetconflog()
    #     # result_data, print_data, configreturn = self.disposelog()
    #     modename, tablename = self.getmodelname()
    #     result_file_o = open(self.result_file, mode='w+')
    #     header = 'SET_RUNNING_PARAM if_address 1 open_mode 1\n<TESTCASE_BEGIN>\n<TESTCASE_HEADER_BEGIN>\n    <TITLE>      "自动化生成脚本"\n    <INDEX>      "x.x.x"\n    <LEVEL>      "2"\n    <WEIGHT>     "4"\n    <MODULE>     "{mode}"\n    <TYPE>       "NETCONF"\n    <AUTHOR>     "Automatic Generation"\n    <LIMITATION> "CmwV7Device"\n    <VERSION>    "2.1"\n    <DESIGN>     "netconf自动化脚本"\n    <SOURCE>     "netconf_rpc_1.topo"\n<TESTCASE_HEADER_END>\n\n<TESTCASE_DEVICE_MAP_BEGIN>\n\n<TESTCASE_DEVICE_MAP_END>\n'.format(mode=modename)
    #     #header = 'SET_RUNNING_PARAM if_address 1 open_mode 1\n<TESTCASE_BEGIN>\n<TESTCASE_HEADER_BEGIN>\n    <TITLE>      "自动化生成脚本"\n    <INDEX>      "x.x.x"\n    <LEVEL>      "2"\n    <WEIGHT>     "4"\n    <MODULE>     "mode"\n    <TYPE>       "NETCONF"\n    <AUTHOR>     "Automatic Generation"\n    <LIMITATION> "CmwV7Device"\n    <VERSION>    "2.1"\n    <DESIGN>     "netconf自动化脚本"\n    <SOURCE>     "netconf_rpc_1.topo"\n<TESTCASE_HEADER_END>\n\n<TESTCASE_DEVICE_MAP_BEGIN>\n\n<TESTCASE_DEVICE_MAP_END>\n'
    #
    #     xmlhellorpc = '"<hello xmlns=\\"urn:ietf:params:xml:ns:netconf:base:1.0\\"><capabilities><capability>urn:ietf:params:netconf:base:1.0</capability></capabilities></hello>\]\]>\]\]>"'
    #     xmlcloserpc = '"<rpc message-id=\\"100\\" xmlns=\\"urn:ietf:params:xml:ns:netconf:base:1.0\\"><close-session/></rpc>\]\]>\]\]>"'
    #     preconfig = '\tset xmlhello ' + xmlhellorpc + '\n\tset xmlclose ' + xmlcloserpc + '\n\tDUT1 Config "netconf ssh server enable\n\tline vty 0 63\n\tauthentication-mode none\n\tuser-role network-admin\n\tidle-timeout 0 0\n\tquit\n\tpassword-recovery enable\n\tundo password-control composition enable\n\tpassword-control length 4\n\tundo password-control complexity user-name check\n\tlocal-user admin class manage\n\tpassword simple admin\n\tservice-type ssh telnet http https\n\tauthorization-attribute user-role network-admin\n\tauthorization-attribute user-role network-operator\n\tquit\n\tquit"\n\tOpenTerm -name netconf -type telnet -addr $addr(DUT1,PORT1) -port 23\n\tafter 3000\n\n\n\t##########部分对象须提前命令行配置的请在此处下发############\n\tDUT1 Config ""\n\n'
    #     ender = '\n<TESTCASE_END>'
    #     stepstart = '<STEP> "验证netconf功能" {\n'
    #     stepend = "}\n"
    #
    #     #拼接脚本头和预配置
    #     result_file_o.write(header)
    #     result_file_o.write(preconfig)
    #     result_file_o.write(stepstart)
    #
    #     #获取模块名  表名，考虑后不使用该方式获取模块名 表名，暂时注释
    #     '''for line in print_data:
    #         temp = line.get("config")
    #         if re.match('.*XML_REQUEST.*', temp) != None and re.match('.*operation="merge".*', temp) != None:
    #             rpcxmltemp = re.findall('<rpc.*rpc>', temp)
    #             rpcxml = "".join(rpcxmltemp)
    #
    #             startindex = rpcxml.index('"merge"><')
    #             endindex = rpcxml.index("></top>")
    #             tmp = rpcxml[startindex:endindex].split("></")
    #             feature = tmp[-1]
    #             tablename = tmp[-2]
    #         else:
    #             continue'''
    #
    #     #将print_data遍历 组织成测试步骤
    #     for line in getnetconflog:
    #         temp = line.get("config")
    #         if re.match('.*XML_REQUEST.*', temp) != None:
    #             checkend = "\n}\n<CHECK>\n"
    #
    #             #拼装check
    #             if re.match('.*<get>.*', temp) != None:
    #                 checkstart = '<CHECK> description "' + modename + '/' + tablename + ' get表操作"\n<CHECK> type custom\n<CHECK> args {\n'
    #                 rpcxmltemp = re.findall('<rpc.*rpc>',temp)
    #                 rpcxml = "".join(rpcxmltemp)
    #                 result_file_o.write(checkstart)
    #
    #                 #目前针对数字　字符　范围内的列值
    #                 sublist = re.compile('>[0-9a-zA-Z/]+<').findall(rpcxml)
    #                 #c count t1 t2 ...都是作为中间变量 l lenth
    #                 c = 1
    #                 for i in sublist:
    #                     t1 = re.findall(">[0-9a-zA-Z/]+<", i)
    #                     t2 = t1[-1]
    #                     l = len(t2)
    #                     t3 = t2[1:l - 1]
    #
    #                     rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml,1)
    #                     t4 = "part_{c}".format(c=c)
    #                     c = c + 1
    #                     result_file_o.write("\tset "+t4+" "+t3+"\n")
    #
    #                 c = c - 1
    #                 list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
    #                 rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"','\\"')
    #
    #                 checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i }  {\n\t\tset pass [lindex $lst $i]"
    #
    #                 checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset getrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset getrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset getrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #
    #                 checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'
    #
    #
    #                 result_file_o.write(str(checkbody1))
    #                 result_file_o.write(str(checkbody2))
    #                 result_file_o.write(str(checkbody3))
    #                 result_file_o.write(str(checkbody4))
    #                 result_file_o.write(str(checkbody5))
    #                 result_file_o.write(checkend)
    #                 result_file_o.write("\n\n\n")
    #
    #             elif re.match('.*<get-bulk>.*', temp) != None:
    #                 checkstart = '<CHECK> description "' + modename + '/' + tablename + ' get-bulk表操作"\n<CHECK> type custom\n<CHECK> args {\n'
    #                 rpcxmltemp = re.findall('<rpc.*rpc>', temp)
    #                 rpcxml = "".join(rpcxmltemp)
    #                 result_file_o.write(checkstart)
    #
    #                 #目前针对数字　字符　范围内的列值
    #                 sublist = re.compile('>[0-9a-zA-Z/]+<').findall(rpcxml)
    #                 #c count t1 t2 ...都是作为中间变量 l lenth
    #                 c = 1
    #                 for i in sublist:
    #                     t1 = re.findall(">[0-9a-zA-Z/]+<", i)
    #                     t2 = t1[-1]
    #                     l = len(t2)
    #                     t3 = t2[1:l - 1]
    #
    #                     rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml,1)
    #                     t4 = "part_{c}".format(c=c)
    #                     c = c + 1
    #                     result_file_o.write("\tset "+t4+" "+t3+"\n")
    #
    #                 c = c - 1
    #                 list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
    #                 rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"','\\"')
    #
    #                 checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i }  {\n\t\tset pass [lindex $lst $i]"
    #
    #                 checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset getbulkrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset getbulkrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset getbulkrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #
    #                 checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'
    #
    #
    #                 result_file_o.write(str(checkbody1))
    #                 result_file_o.write(str(checkbody2))
    #                 result_file_o.write(str(checkbody3))
    #                 result_file_o.write(str(checkbody4))
    #                 result_file_o.write(str(checkbody5))
    #
    #                 result_file_o.write(checkend)
    #                 result_file_o.write("\n\n\n")
    #
    #             elif re.match('.*<get-config>.*', temp) != None:
    #                 checkstart = '<CHECK> description "' + modename + '/' + tablename + ' get-config表操作"\n<CHECK> type custom\n<CHECK> args {\n'
    #                 rpcxmltemp = re.findall('<rpc.*rpc>', temp)
    #                 rpcxml = "".join(rpcxmltemp)
    #                 result_file_o.write(checkstart)
    #
    #                 #目前针对数字　字符　范围内的列值
    #                 sublist = re.compile('>[0-9a-zA-Z/]+<').findall(rpcxml)
    #                 #c count t1 t2 ...都是作为中间变量 l lenth
    #                 c = 1
    #                 for i in sublist:
    #                     t1 = re.findall(">[0-9a-zA-Z/]+<", i)
    #                     t2 = t1[-1]
    #                     l = len(t2)
    #                     t3 = t2[1:l - 1]
    #
    #                     rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml,1)
    #                     t4 = "part_{c}".format(c=c)
    #                     c = c + 1
    #                     result_file_o.write("\tset "+t4+" "+t3+"\n")
    #
    #                 c = c - 1
    #                 list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
    #                 rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"','\\"')
    #
    #                 checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i }  {\n\t\tset pass [lindex $lst $i]"
    #
    #                 checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset getconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset getconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset getconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #
    #                 checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'
    #
    #
    #                 result_file_o.write(str(checkbody1))
    #                 result_file_o.write(str(checkbody2))
    #                 result_file_o.write(str(checkbody3))
    #                 result_file_o.write(str(checkbody4))
    #                 result_file_o.write(str(checkbody5))
    #
    #                 result_file_o.write(checkend)
    #                 result_file_o.write("\n\n\n")
    #
    #             elif re.match('.*<get-bulk-config>.*', temp) != None:
    #                 checkstart = '<CHECK> description "' + modename + '/' + tablename + ' get-bulk-config表操作"\n<CHECK> type custom\n<CHECK> args {\n'
    #                 rpcxmltemp = re.findall('<rpc.*rpc>', temp)
    #                 rpcxml = "".join(rpcxmltemp)
    #                 result_file_o.write(checkstart)
    #
    #                 #目前针对数字　字符　范围内的列值
    #                 sublist = re.compile('>[0-9a-zA-Z/]+<').findall(rpcxml)
    #                 #c count t1 t2 ...都是作为中间变量 l lenth
    #                 c = 1
    #                 for i in sublist:
    #                     t1 = re.findall(">[0-9a-zA-Z/]+<", i)
    #                     t2 = t1[-1]
    #                     l = len(t2)
    #                     t3 = t2[1:l - 1]
    #
    #                     rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml,1)
    #                     t4 = "part_{c}".format(c=c)
    #                     c = c + 1
    #                     result_file_o.write("\tset "+t4+" "+t3+"\n")
    #
    #                 c = c - 1
    #                 list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
    #                 rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"','\\"')
    #
    #                 checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i }  {\n\t\tset pass [lindex $lst $i]"
    #
    #                 checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset getbulkconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset getbulkconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset getbulkconfigrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $getbulkconfigrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "<data></data>" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #
    #                 checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'
    #
    #
    #                 result_file_o.write(str(checkbody1))
    #                 result_file_o.write(str(checkbody2))
    #                 result_file_o.write(str(checkbody3))
    #                 result_file_o.write(str(checkbody4))
    #                 result_file_o.write(str(checkbody5))
    #
    #                 result_file_o.write(checkend)
    #                 result_file_o.write("\n\n\n")
    #
    #             elif re.match('.*operation="merge".*', temp) != None:
    #                 checkstart = '<CHECK> description "' + modename + '/' + tablename + ' merge表操作"\n<CHECK> type custom\n<CHECK> args {\n'
    #                 rpcxmltemp = re.findall('<rpc.*rpc>', temp)
    #                 rpcxml = "".join(rpcxmltemp)
    #                 result_file_o.write(checkstart)
    #
    #                 #目前针对数字　字符　范围内的列值
    #                 sublist = re.compile('>[0-9a-zA-Z/]+<').findall(rpcxml)
    #                 #c count t1 t2 ...都是作为中间变量 l lenth
    #                 c = 1
    #                 for i in sublist:
    #                     t1 = re.findall(">[0-9a-zA-Z/]+<", i)
    #                     t2 = t1[-1]
    #                     l = len(t2)
    #                     t3 = t2[1:l - 1]
    #
    #                     rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml,1)
    #                     t4 = "part_{c}".format(c=c)
    #                     c = c + 1
    #                     result_file_o.write("\tset "+t4+" "+t3+"\n")
    #
    #                 c = c - 1
    #                 list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
    #                 rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"','\\"')
    #
    #                 checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i }  {\n\t\tset pass [lindex $lst $i]"
    #
    #                 checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset mergegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $mergegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset mergegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $mergegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset mergegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $mergegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #
    #                 checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'
    #
    #
    #                 result_file_o.write(str(checkbody1))
    #                 result_file_o.write(str(checkbody2))
    #                 result_file_o.write(str(checkbody3))
    #                 result_file_o.write(str(checkbody4))
    #                 result_file_o.write(str(checkbody5))
    #
    #
    #                 result_file_o.write(checkend)
    #                 result_file_o.write("\n\n\n")
    #
    #             elif re.match('.*operation="create".*', temp) != None:
    #                 checkstart = '<CHECK> description "' + modename + '/' + tablename + ' create表操作"\n<CHECK> type custom\n<CHECK> args {\n'
    #                 rpcxmltemp = re.findall('<rpc.*rpc>', temp)
    #                 rpcxml = "".join(rpcxmltemp)
    #                 result_file_o.write(checkstart)
    #
    #                 #目前针对数字　字符　范围内的列值
    #                 sublist = re.compile('>[0-9a-zA-Z/]+<').findall(rpcxml)
    #                 #c count t1 t2 ...都是作为中间变量 l lenth
    #                 c = 1
    #                 for i in sublist:
    #                     t1 = re.findall(">[0-9a-zA-Z/]+<", i)
    #                     t2 = t1[-1]
    #                     l = len(t2)
    #                     t3 = t2[1:l - 1]
    #
    #                     rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml,1)
    #                     t4 = "part_{c}".format(c=c)
    #                     c = c + 1
    #                     result_file_o.write("\tset "+t4+" "+t3+"\n")
    #
    #                 c = c - 1
    #                 list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
    #                 rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"','\\"')
    #
    #                 checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i }  {\n\t\tset pass [lindex $lst $i]"
    #
    #                 checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset creategrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $creategrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset creategrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $creategrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset creategrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $creategrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "Configuration already exists." $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #
    #                 checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'
    #
    #
    #                 result_file_o.write(str(checkbody1))
    #                 result_file_o.write(str(checkbody2))
    #                 result_file_o.write(str(checkbody3))
    #                 result_file_o.write(str(checkbody4))
    #                 result_file_o.write(str(checkbody5))
    #
    #
    #                 result_file_o.write(checkend)
    #                 result_file_o.write("\n\n\n")
    #
    #             elif re.match('.*operation="replace".*', temp) != None:
    #                 checkstart = '<CHECK> description "' + modename + '/' + tablename + ' replace表操作"\n<CHECK> type custom\n<CHECK> args {\n'
    #                 rpcxmltemp = re.findall('<rpc.*rpc>', temp)
    #                 rpcxml = "".join(rpcxmltemp)
    #                 result_file_o.write(checkstart)
    #
    #                 #目前针对数字　字符　范围内的列值
    #                 sublist = re.compile('>[0-9a-zA-Z/]+<').findall(rpcxml)
    #                 #c count t1 t2 ...都是作为中间变量 l lenth
    #                 c = 1
    #                 for i in sublist:
    #                     t1 = re.findall(">[0-9a-zA-Z/]+<", i)
    #                     t2 = t1[-1]
    #                     l = len(t2)
    #                     t3 = t2[1:l - 1]
    #
    #                     rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml,1)
    #                     t4 = "part_{c}".format(c=c)
    #                     c = c + 1
    #                     result_file_o.write("\tset "+t4+" "+t3+"\n")
    #
    #                 c = c - 1
    #                 list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
    #                 rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"','\\"')
    #
    #                 checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i }  {\n\t\tset pass [lindex $lst $i]"
    #
    #                 checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset replacegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $replacegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset replacegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $replacegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset replacegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $replacegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #
    #                 checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'
    #
    #
    #                 result_file_o.write(str(checkbody1))
    #                 result_file_o.write(str(checkbody2))
    #                 result_file_o.write(str(checkbody3))
    #                 result_file_o.write(str(checkbody4))
    #                 result_file_o.write(str(checkbody5))
    #
    #                 result_file_o.write(checkend)
    #                 result_file_o.write("\n\n\n")
    #
    #             elif re.match('.*operation="delete".*', temp) != None:
    #                 checkstart = '<CHECK> description "' + modename + '/' + tablename + ' delete表操作"\n<CHECK> type custom\n<CHECK> args {\n'
    #                 rpcxmltemp = re.findall('<rpc.*rpc>', temp)
    #                 rpcxml = "".join(rpcxmltemp)
    #
    #                 result_file_o.write(checkstart)
    #
    #                 #目前针对数字　字符　范围内的列值
    #                 sublist = re.compile('>[0-9a-zA-Z/]+<').findall(rpcxml)
    #                 #c count t1 t2 ...都是作为中间变量 l lenth
    #                 c = 1
    #                 for i in sublist:
    #                     t1 = re.findall(">[0-9a-zA-Z/]+<", i)
    #                     t2 = t1[-1]
    #                     l = len(t2)
    #                     t3 = t2[1:l - 1]
    #
    #                     rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml,1)
    #                     t4 = "part_{c}".format(c=c)
    #                     c = c + 1
    #                     result_file_o.write("\tset "+t4+" "+t3+"\n")
    #
    #                 c = c - 1
    #                 list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
    #                 rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"','\\"')
    #
    #                 checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i }  {\n\t\tset pass [lindex $lst $i]"
    #
    #                 checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset deletegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $deletegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset deletegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $deletegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset deletegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $deletegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "Configuration does not exist." $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #
    #                 checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'
    #
    #
    #                 result_file_o.write(str(checkbody1))
    #                 result_file_o.write(str(checkbody2))
    #                 result_file_o.write(str(checkbody3))
    #                 result_file_o.write(str(checkbody4))
    #                 result_file_o.write(str(checkbody5))
    #
    #                 result_file_o.write(checkend)
    #                 result_file_o.write("\n\n\n")
    #
    #             elif re.match('.*operation="remove".*', temp) != None:
    #                 checkstart = '<CHECK> description "' + modename + '/' + tablename + ' remove表操作"\n<CHECK> type custom\n<CHECK> args {\n'
    #                 rpcxmltemp = re.findall('<rpc.*rpc>', temp)
    #                 rpcxml = "".join(rpcxmltemp)
    #                 result_file_o.write(checkstart)
    #
    #                 #目前针对数字　字符　范围内的列值
    #                 sublist = re.compile('>[0-9a-zA-Z/]+<').findall(rpcxml)
    #                 #c count t1 t2 ...都是作为中间变量 l lenth
    #                 c = 1
    #                 for i in sublist:
    #                     t1 = re.findall(">[0-9a-zA-Z/]+<", i)
    #                     t2 = t1[-1]
    #                     l = len(t2)
    #                     t3 = t2[1:l - 1]
    #
    #                     rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml,1)
    #                     t4 = "part_{c}".format(c=c)
    #                     c = c + 1
    #                     result_file_o.write("\tset "+t4+" "+t3+"\n")
    #
    #                 c = c - 1
    #                 list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
    #                 rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"','\\"')
    #
    #                 checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i }  {\n\t\tset pass [lindex $lst $i]"
    #
    #                 checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #
    #                 checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'
    #
    #
    #                 result_file_o.write(str(checkbody1))
    #                 result_file_o.write(str(checkbody2))
    #                 result_file_o.write(str(checkbody3))
    #                 result_file_o.write(str(checkbody4))
    #                 result_file_o.write(str(checkbody5))
    #
    #                 result_file_o.write(checkend)
    #                 result_file_o.write("\n\n\n")
    #
    #             elif re.match('<action>', temp) != None:
    #                 checkstart = '<CHECK> description "' + modename + '/' + tablename + ' action操作"\n<CHECK> type custom\n<CHECK> args {\n'
    #                 rpcxmltemp = re.findall('<rpc.*rpc>', temp)
    #                 rpcxml = "".join(rpcxmltemp)
    #                 result_file_o.write(checkstart)
    #
    #                 #目前针对数字　字符　范围内的列值
    #                 sublist = re.compile('>[0-9a-zA-Z/]+<').findall(rpcxml)
    #                 #c count t1 t2 ...都是作为中间变量 l lenth
    #                 c = 1
    #                 for i in sublist:
    #                     t1 = re.findall(">[0-9a-zA-Z/]+<", i)
    #                     t2 = t1[-1]
    #                     l = len(t2)
    #                     t3 = t2[1:l - 1]
    #
    #                     rpcxml = re.sub(re.compile(i), ">$part_{c}<".format(c=c), rpcxml,1)
    #                     t4 = "part_{c}".format(c=c)
    #                     c = c + 1
    #                     result_file_o.write("\tset "+t4+" "+t3+"\n")
    #
    #                 c = c - 1
    #                 list1 = "set lst " + '"' + "合法值 " + "$part_{c}".format(c=c) + " 非法值" + '"'
    #                 rpcxml = rpcxml.replace("$part_{c}".format(c=c), "$pass").replace('"','\\"')
    #
    #                 checkbody1 = "\n\t" + list1 + "\n\tset i 0\n\tset lenth [expr [llength $lst]-1]\n\n\tfor { set i $i } { $i <= $lenth } { incr i }  {\n\t\tset pass [lindex $lst $i]"
    #
    #                 checkbody2 = '\n\t\tif {$i==0} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody3 = '\n\t\tif {$i==1} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #                 checkbody4 = '\n\t\tif {$i==$lenth} {\n\t\t\tset removegrpc ' + '"' + rpcxml + "\]\]>\]\]>" + '"' + '\n\t\t\ttsend3  netconf "xml"\n\t\t\t<WAIT> 3\n\t\t\ttsend3  netconf -t 3000  $xmlhello\n\t\t\t<WAIT> 3\n\t\t\ttclear netconf\n\t\t\ttsend3  netconf -t 3000  $removegrpc\n\t\t\t<WAIT> 3\n\t\t\tset res [tget netconf]\n\n\t\t\t#请根据实际情况调整检查内容\n\t\t\tif {[string first "ok" $res] != -1} {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tcontinue\n\t\t\t} else {\n\t\t\t\ttsend3  netconf -t 1000 $xmlclose\n\t\t\t\t<WAIT> 3\n\t\t\t\tputs "检查失败，错误信息如下: $res"\n\t\t\t\tbreak\n\t\t\t}\n\t\t}'
    #
    #                 checkbody5 = '\n\t}\n\texpr $i == [expr $lenth+1]'
    #
    #
    #                 result_file_o.write(str(checkbody1))
    #                 result_file_o.write(str(checkbody2))
    #                 result_file_o.write(str(checkbody3))
    #                 result_file_o.write(str(checkbody4))
    #                 result_file_o.write(str(checkbody5))
    #
    #                 result_file_o.write(checkend)
    #                 result_file_o.write("\n\n\n")
    #
    #
    #     # 拼接脚本尾　
    #     result_file_o.write(stepend)
    #     result_file_o.write(ender)
    #     result_file_o.close()


# ss = generateNetconfTcl()
# aa = ss.getnetconflog()
# print(aa)
# zz = '[2022/04/25 17:20:10] %Apr 25 16:57:33:648 2022 H3C XMLSOAP/6/XML_REQUEST: -MDC=1; netconf from 172.17.0.232,session id 3,message-id 101,receive get request.<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:web="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101"><get><filter type="subtree"><top xmlns="http://www.h3c.com/netconf/data:1.0"><ND><NdProxySendEnable><SendEnable><IfIndex>433</IfIndex><Enable>0</Enable></SendEnable></NdProxySendEnable></ND></top></filter></get></rpc>'
# qq = re.compile(
#             "\[\d{4}(?:-|/|.)\d{1,2}(?:-|/|.)\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}]\s*[[<\[]*.*[>\]]*]*%[A-Za-z]*\s*\d{1,2}\s*\d{1,2}:\d{1,2}:\d{1,2}:\d{1,3}\s\d{4}\s*.*").findall(zz)
# print(qq)