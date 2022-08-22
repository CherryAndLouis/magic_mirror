# -*- coding=utf-8 -*-

import sys
import time
import netconf
import ncclient
from netconf.client import NetconfSSHSession
import logging
from string import Template
from ncclient import manager
# from ncclient import
from ncclient import operations

log = logging.getLogger(__name__)


def h3c_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           hostkey_verify=False,
                           device_params={'name': 'h3c'},
                           allow_agent=False,
                           look_for_keys=False)


def _check_response(rpc_obj, snippet_name):
    print("RPCReply for %s is %s" % (snippet_name, rpc_obj.xml))
    xml_str = rpc_obj.xml
    print(xml_str)
    if "<ok/>" in xml_str:
        print("%s successful" % snippet_name)
    else:
        print("Cannot successfully execute: %s" % snippet_name)


def ss(host, port, user, password):
    # 1.Create a NETCONF session
    with h3c_connect(host=host, port=port, user=user, password=password) as m:
#         acl = '''
#        <access-lists xmlns="urn:ietf:params:xml:ns:yang:ietf-acl" xmlns:hw-acl="urn:huawei:params:xml:ns:yang:huawei-acl" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
#         <access-list>
#           <access-control-list-name>3900</access-control-list-name>
#
#         </access-list>
#       </access-lists>
#
# '''
        acl = '''
             <top xmlns="http://www.h3c.com/netconf/config:1.0"><Ifmgr xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:xc="http://www.h3c.com/netconf/base:1.0"></Ifmgr></top>
        '''
        get = m.get_config(source='running', filter=('subtree', acl))
        print(get)


# if __name__ == '__main__':
#     host = '172.16.23.231'
#     port = 830
#     user = 'test'
#     password = 'test'
#     ss(host, port, user, password)


#
#
def ssh_send_rpc(host, port=830, username='admin', password='admin', rpc_xml=None, timeout=20000):
    try:
        session = NetconfSSHSession(host, port, username, password)
        print(session)
        return_xml = session.send_rpc(rpc=rpc_xml.strip(), timeout=int(timeout))
        return_xml_2 = session.send_rpc(rpc='<commit xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"/>', timeout=int(timeout))
        #session.close()
        ret = return_xml[-1] + return_xml_2
        return ret

    except netconf.error.NetconfError as net_err:
        return str(net_err)
    except netconf.error.SessionError as ses_err:
        return str(ses_err)
    except Exception as e:
        return str(e)
#
# reply_xml = ssh_send_rpc(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] , sys.argv[6])
reply_xml = ssh_send_rpc(host='172.16.23.231',username='test', password='test', rpc_xml='''<commit xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"/>''')
# print(reply_xml)
# print(reply_xml.replace('<?xml version="1.0" encoding="UTF-8"?>',''))
#

# test = '''sss
#     ssss
#         sssss
#             sssss'''
# print(test)


