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
    <SOURCE> "no_topo_name"
<TESTCASE_HEADER_END>

<TESTCASE_DEVICE_MAP_BEGIN>

<TESTCASE_DEVICE_MAP_END>

<STEP> "step 1" {
  DUT1 Config "

      reset logbuffer
      sys 
      interface GigabitEthernet 2/0/1
      description dsfhkjadsfhkasdjg	"

	<CHECK> description "check 1"
	<CHECK> type custom
	<CHECK> args  {  
	    DUT1 Config "return"
	    DUT1 CheckConfig -command "display thi" -include "dsf"  -checkreturn configreturn
    }
	<CHECK> repeat 1 -interval 5 
    <CHECK> whenfailed {PUTSINFO "$configreturn"}
    <CHECK> 
}
<TESTCASE_END>