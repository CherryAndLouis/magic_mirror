<TESTCASE_BEGIN>
<TESTCASE_HEADER_BEGIN>
    <TITLE>      "ִ�������Զ������ɽű�"
    <INDEX>      "ִ�б��"
    <LEVEL>      "2"
    <WEIGHT>     "4"
    <MODULE>     "no_modename"
    <TYPE>       "FUN"
    <AUTHOR>     "Automatic Generation"
    <LIMITATION> "CmwV7Device"
    <VERSION> "2.1"
    <DESIGN> "log�Զ����ű�"
    <SOURCE> "isis.topo"
<TESTCASE_HEADER_END>

<TESTCASE_DEVICE_MAP_BEGIN>

<TESTCASE_DEVICE_MAP_END>

<STEP> "step 1" {
  DUT1 Config "

      reset logbuffer
      sy
      interface $intf(DUT1,PORT1) 
      interface $intf(DUT1,PORT1) 
      qu
      sy	"
}
<TESTCASE_END>