from __future__ import print_function

from collections import defaultdict
import pexpect
import subprocess
import threading
import re
import string
import thread
from threading import Lock
import sys

def reset_bluetooth_controller():
    print("Re-initializing Bluetooth controller")
    subprocess.Popen(["sudo", "hciconfig", "hci0", "down"]).wait()
    subprocess.Popen(["sudo", "hciconfig", "hci0", "up"]).wait()

def lescan(timeout=5):
    scan = pexpect.spawn("sudo hcitool lescan")
    # TODO don't want to expect anything, just want to take advantage of
    # pexpect's timeout feature
    try:
        scan.expect("foooooo", timeout=timeout)
    except pexpect.TIMEOUT:
        devices = {}
        for line in scan.before.split("\r\n"):
            match = re.match("(([0-9A-Fa-f][0-9A-Fa-f]:?){6}) (\(?[\w]+\)?)", line)
            if match is not None:
                name = match.group(1)
                devices[name] = {
                    'address': match.group(1),
                    'name': match.group(3)
                }
    return [device for device in devices.values()]

class BluetoothLeError(Exception): pass

class BluetoothLeDevice(object):
    DEFAULT_TIMEOUT_S = .5
    DEFAULT_ASYNC_TIMEOUT_S = .5
    connection_lock = threading.RLock()
    handles = {}    
    callbacks = defaultdict(set)
    subscribed_handlers = {}
    running = True

    def __init__(self, mac_address, bond=False, connect=True, verbose=True):
        self.lock = Lock()        
        self.verbose = verbose
        f = open("log.txt","w+")
        self.con = pexpect.spawn('gatttool -b ' + mac_address + ' --interactive')
        self.con.logfile = f
        self.con.expect('\[LE\]>', timeout=1)
        if bond:
            self.con.sendline('sec-level medium')
        if connect:
            self.connect()
        thread.start_new_thread(self.run, ())
        #handle = self.con.get_handle_list()

    def connect(self, timeout=5.0):
        try:
            with self.connection_lock:
                self.con.sendline('connect')
                self.con.expect('\[CON\].*>', timeout)
                print ('Connected succesfully' ) 
               
        except pexpect.TIMEOUT:
            raise BluetoothLeError("Unable to connect to device")
        
    def get_handle_list(self):
       
        #with self.connection_lock:            
        self.con.sendline('characteristics')
        #try:
        #self.con.expect(uuid, timeout=50)
    #except pexpect.TIMEOUT:
        #raise BluetoothLeError(self.con.before)
    #else:
        # TODO ugh this is sketchy, but then again so is this whole
        # "library". The last line of the output will be the one
        # matching our uuid (because it was the filter for the call
        # to 'expect' above. Take that and pull out the leftmost
        # handle value.
        # ...just split on ':'!
        #matching_line = self.con.before.splitlines(True)[-1]
        #self.handles[uuid] = int(
         #       re.search("handle: 0x([a-fA-F0-9]{4})",
          #          matching_line).group(1), 16)
        self.con.expect([pexpect.EOF,pexpect.TIMEOUT],timeout = 50)
        #Output of the 'characteristics' will be something like, with the first element a little skewed. So delete the first element and use the rest.
        #handle: 0x0006, char properties: 0x02, char value handle: 0x0007, uuid: 00002a02-0000-1000-8000-00805f9b34fb
        #handle: 0x0008, char properties: 0x08, char value handle: 0x0009, uuid: 00002a03-0000-1000-8000-00805f9b34fb
        #handle: 0x000a, char properties: 0x02, char value handle: 0x000b, uuid: 00002a04-0000-1000-8000-00805f9b34fb
        #handle: 0x000d, char properties: 0x20, char value handle: 0x000e, uuid: 00002a05-0000-1000-8000-00805f9b34fb
        #handle - [8:14], char-properties - [33:37], char-value-handle - [58-64], uuid - [72:108]
        
        #handle_uuid_data_text = self.con.before
        list_data = self.con.before.splitlines()
        del list_data[0]
        uuid_handle_dict = {}
        for line in list_data:
            self.handles[line[8:14]] = (line[33:37],line[58:64],line[72:108])
            
        return self.handles         
                
                #print handle_uuid_data_text
                    
                    
        

    #def get_handle(self, uuid):
        """Look up and return the handle for an attribute by its UUID.

        uuid - the UUID of the characteristic.

        Returns None if the UUID was not found.
        """
        ##if uuid not in self.handles:
            

    def _expect(self, expected, timeout=DEFAULT_TIMEOUT_S):
        """We may (and often do) get an indication/notification before a
        write completes, and so it can be lost if we "expect()"'d something
        that came after it in the output, e.g.:

        > char-write-req 0x1 0x2
        Notification handle: xxx
        Write completed successfully.
        >

        Anytime we expect something we have to expect noti/indication first for
        a short time.
        """

        with self.connection_lock:
            patterns = [
                expected,
                'Notification handle = .*? \r',
                'Indication   handle = .*? \r',
            ]
            while True:
                try:
                    matched_pattern_index = self.con.expect(patterns, timeout)
                    if matched_pattern_index == 0:
                        break
                    elif matched_pattern_index == 1 or matched_pattern_index == 2:
                        self._handle_notification(self.con.after)
                except pexpect.TIMEOUT:
                    raise BluetoothLeError(self.con.before)

    def char_write(self, handle, value, wait_for_response=False):
        with self.connection_lock:
            #hexstring = ''.join('%02x' % byte for byte in value)
            hexstring = str(value)
            if wait_for_response:
                cmd = 'req'
            else:
                cmd = 'cmd'
            cmd = 'char-write-%s 0x%02x %s' % (cmd, handle, hexstring)
            #print str(cmd)
            if self.verbose:
                print("Sending command: %s" % cmd)
            self.con.sendline(cmd)

            if wait_for_response:
                self._expect('Characteristic value was written successfully')
            if self.verbose:
                print("Sent.")

    def char_read_uuid(self, uuid):
        with self.connection_lock:
            self.con.sendline('char-read-uuid %s' % uuid)
            self._expect('value: .*? \r')
            rval = self.con.after.split()[1:]
            return bytearray([int(x, 16) for x in rval])

    def char_read_hnd(self, handle):
        with self.connection_lock:
            self.con.sendline('char-read-hnd 0x%02x' % handle)
            print("'char-read-hnd 0x%02x'" % handle)
            self._expect('descriptor: .*? \r')
            rval = self.con.after.split()[1:]
            return [int(n, 16) for n in rval]

    def subscribe(self, uuid, callback=None, indication=False):
        definition_handle = self.get_handle(uuid)
        # Expect notifications on the value handle...
        value_handle = definition_handle + 1
        # but write to the characteristic config to enable notifications
        characteristic_config_handle = value_handle + 1
        if indication:
            properties = bytearray([0x02, 0x00])
        else:
            properties = bytearray([0x01, 0x00])

        try:
            self.lock.acquire()

            if callback is not None:
                self.callbacks[value_handle].add(callback)

            if self.subscribed_handlers.get(value_handle, None) != properties:
                self.char_write(characteristic_config_handle, properties, wait_for_response=False)
                self.subscribed_handlers[value_handle] = properties
        finally:
            self.lock.release()

    def _handle_notification(self, msg):
        handle, _, value = string.split(msg.strip(), maxsplit=5)[3:]
        handle = int(handle, 16)
        value = bytearray.fromhex(value)

        try:
            self.lock.acquire()
            if handle in self.callbacks:
                for callback in self.callbacks[handle]:
                    callback(handle, value)
        finally:
            self.lock.release()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            with self.connection_lock:
                try:
                    self._expect("fooooooo", timeout=.1)
                except BluetoothLeError:
                    pass
            # TODO need some delay to avoid aggresively grabbing the lock,
            # blocking out the others. worst case is 1 second delay for async
            # not received as a part of another request
            import time
            time.sleep(.001)
    def disconnect(self):
        self.con.sendline('disconnect')
        print("Disconnected. Returning the child process to terminal")
        self.con.interact()
        
    def kill_child(self):
        self.con.sendline('quit')
        print('Quit the process. Returning the child process to terminal')
        self.con.interact()
