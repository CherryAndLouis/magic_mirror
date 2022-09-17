#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: wangzhen
# FILE: D:\python\TeBot\script\public.py
# DATE: 2022/04/05 周二
# TIME: 16:50:02

# DESCRIPTION:
from configparser import ConfigParser
from pathlib import Path


class MyParser(ConfigParser):
    """
    MyParser _Inherit from built-in class: ConfigParser_

    _extended_summary_

    Args:
        ConfigParser (_type_): _description_
    """

    def optionxform(self, optionstr):
        """
        optionxform _Rewrite without lower()_

        _extended_summary_

        Args:
            optionstr (_type_): _description_

        Returns:
            _type_: _description_
        """
        return optionstr


def set_value(section: str, key: str, value: str):
    """
    set_value _global_var.ini配置文件中写入键值对_

    _extended_summary_

    Args:
        section (str): _description_
        key (str): _description_
        value (str): _description_
    """
    conf = MyParser()
    try:
        conf.read(Path(__file__).parent / 'global_var.ini', encoding='utf-8')
    except Exception as e:
        pass
    if section not in conf.sections():
        conf.add_section(section)
        conf.set(section, key, value)
    else:
        conf[section][key] = value
    with open(Path(__file__).parent / 'global_var.ini', 'w', encoding='utf-8') as f:
        conf.write(f)


def get_value(section: str, key: str) -> object:
    """
    get_value _获取global_var.ini配置文件中键值对_

    _extended_summary_

    Args:
        section (str): _.ini文件中section_
        key (str): _description_

    Returns:
        _type_: key存在则返回对应Value，否则返回None_
    """
    conf = MyParser()
    conf.read(Path(__file__).parent / 'global_var.ini', encoding='utf-8')
    if conf.has_option(f"{section}", f"{key}"):
        # 判断存在option
        return conf.get(section, key)
    else:
        # 不存在option
        # print(f"全局变量中不存在 {section} {key}")
        return None


def var_has_option(section: str, key: str):
    """
    var_has_option _判断是否存在option,存在返回True,否则返回False_

    _extended_summary_

    Args:
        section (str): _description_
        key (str): _description_

    Returns:
        _type_: _description_
    """
    conf = MyParser()
    conf.read(Path(__file__).parent / 'global_var.ini', encoding='utf-8')
    return True if conf.has_option(f"{section}", f"{key}") else False


def get_options(section: str):
    """
    get_options _summary_

    _extended_summary_

    Args:
        section (str): _description_
    """
    conf = MyParser()
    conf.read(Path(__file__).parent / 'global_var.ini', encoding='utf-8')
    if conf.has_section(f"{section}"):
        # 判断存在section
        return conf.options(f"{section}")
    else:
        # 不存在section
        # print(f"全局变量中不存在 {section}")
        return None


def clear_value():
    """
    clear_value _清空 global_var.ini 中文本内容_

    _extended_summary_
    """
    with open(Path(__file__).parent / 'global_var.ini', 'w', encoding='utf-8') as f:
        f.truncate(0)
    set_value('LoginParams', 'userName', '')
    set_value('LoginParams', 'password', '')
    set_value('LoginParams', 'LoginStatus', '')
    set_value('LoginParams', 'chassisAddr', '')
    set_value('LoginParams', 'loginToken', '')
    set_value('scriptParams', 'path', '')
    set_value('port_summary', 'allportNameList', '')
    set_value('port_summary', 'reservedportNameList', '')
    set_value('port_summary', 'reservedportTopoNameList', '')
    set_value('port_summary', 'specialportInfo', '')
    set_value('device_summary', 'alldeviceNameList', '')
    set_value('device_summary', 'alldeviceIdList', '')
    set_value('device_summary', 'specialdeviceInfo', '')
    set_value('streamStatistics_summary', 'allStreamNameList', '')
    set_value('streamStatistics_summary', 'allStreamIdList', '')
    set_value('streamStatistics_summary', 'specialPortStaticsInfo', '')
    set_value('streamStatistics_summary', 'specialStreamStaticsInfo', '')
    set_value('statusBar', 'status', '')

