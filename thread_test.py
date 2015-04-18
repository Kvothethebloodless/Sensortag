import threading
import pexpect

class test_thread(threading.Thread):
    def run(self):
        print"Running test_thread"
        for i in range(100):
            print i

class pexpect_thread(threading.Thread):
    #def __init__(self):
    def run(self):
        obj = pexpect.spawn('hcitool dev | tee cat.txt')
        obj.sendline('ls -R | cat.txt')
        obj.expect(pexpect.EOF)
        print obj.before


a = test_thread()
b = pexpect_thread()
a.start()
b.start()
