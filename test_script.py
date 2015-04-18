##import commands
##print commands.getstatusoutput('sudo python -m compileall')
import pygattt as pgt
sen = pgt.BluetoothLeDevice('90:59:AF:0B:83:25',bond=False,connect=True,verbose=True)
sen.char_write(52,'03')
sen.char_write(49,'0100')
#print state
##sen.get_handle('2a00')
##sen.disconnect()
##sen.kill_child()e

##import pexpect
##import sys
##
##obj = pexpect.spawn('/bin/bash -c "sudo gatttool -b 90:59:AF:0B:83:25 --interactive | tee cat.txt | tee cat.txt"')
##print str(obj.pid)
##obj.logfile = sys.stdout
###obj.expect(pexpect.EOF)
##obj.sendline('connect')
##obj.expect(pexpect.EOF)
###obj.sendline('')
