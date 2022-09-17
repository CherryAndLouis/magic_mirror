# from pysnmp.hlapi import *
#
# iterator = bulkCmd(
#     SnmpEngine(),
#     CommunityData('snmp-agent', 'public', 1),
#     # UsmUserData('usr-md5-des', 'authkey1', 'privkey1'),
#     UdpTransportTarget(('88.88.88.88', 161)),
#     ContextData(),
#     0, 2,
#     ObjectType(ObjectIdentity('1.3.6.1.2.1.31.1.1.1.18'), '261'),
#     # ObjectType(ObjectIdentity('IP-MIB', 'ipAddrEntry')),
#     lexicographicMode=False
# )
#
# for errorIndication, errorStatus, errorIndex, varBinds in iterator:
#
#     if errorIndication:
#         print(errorIndication)
#         break
#
#     elif errorStatus:
#         print('%s at %s' % (errorStatus.prettyPrint(),
#                             errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
#         break
#
#     else:
#         for varBind in varBinds:
#             print(' = '.join([x.prettyPrint() for x in varBind]))


# from pysnmp.entity.rfc3413.oneliner import cmdgen
# cmdGen=cmdgen.CommandGenerator()
# errorIndication,errorStatus,errorindex,varBindTable=cmdGen.bulkCmd(
# cmdgen.CommunityData('snmp-agent', 'public', 1),
# cmdgen.UdpTransportTarget(('88.88.88.88',161)),
# 0,2,
# '1.3.6.1.2.1.31.1.1.1.18.258',
# # '1.3.6.1.2.1.31.1.1.1.15',
# )
# for varBindTableRow in varBindTable:
#     for name,val in varBindTableRow:
#         print('%s=%s'%(name.prettyPrint(),val.prettyPrint()))

# from pysnmp.hlapi import *
#
# N, R = 0, 2
# g = bulkCmd(SnmpEngine(),
#              CommunityData('public'),
#              UdpTransportTarget(('88.88.88.88', 161)),
#              ContextData(),
#              1, 2,
#              ObjectType(ObjectIdentity('1.3.6.1.2.1.31.1.1.1.18.277')))

# print(next(g))
# (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'), DisplayString('SunOS zeus.snmplabs.com'))])
# next(g)
# (None, 0, 0, [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.2.0'), ObjectIdentifier('1.3.6.1.4.1.20408'))])
# for errorIndication, errorStatus, errorIndex, varBinds in g:
#
#     if errorIndication:
#         print(errorIndication)
#         break
#
#     elif errorStatus:
#         print('%s at %s' % (errorStatus.prettyPrint(),
#                             errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
#         break
#
#     else:
#         for varBind in varBinds:
#             print(' = '.join([x.prettyPrint() for x in varBind]))
import os
import sys
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    print(application_path)
elif __file__:
    application_path = os.path.dirname(__file__)
    print(application_path)