import pexepct
import time
import sys
import pygattt
import os

class sensor_error(Exception): pass

class sensor(pygattt.BluetoothLeDevice):

    def __init__(self,sensor_tag,list_handles,verbose=True,enable=True,notify=True,set_period=True):
        #Expects a connected BluetoothLeDevice object - sensor_tag as an input
        #list_handles goes in this order:
        # list_handles[0] = enable_handle - the decimal number version of the handle
        # list_handles[1] = enable_value - the string to write to to enable the sensor accordingly
        # list_handles[2] = data_handle - int
        # list_handles[3] = notify_handle - int
        # list_handles[4] = notify_value - str (The pygatt source code has been modified accordingly to write strings
                                                #using the def ""char-write"")
        # list_handles[5] = period_handle - int
        # list_handles[6] = period_value - str
        #accel_list_handles = [52,'03','00',48,49,'0100',55,'10'] - for 10 milliseconds
        self.enable_handle = list_handles[0]
        self.enable_value =  list_handles[1]
        self.disable_value = list_handles[2]
        self.data_handle =   list_handles[3]
        self.notify_handle = list_handles[4]
        self.notify_value =  list_handles[5]
        self.period_handle = list_handles[6]
        self.period_value =  list_handles[7]

        #Don't have to worry about connection handling as Pygatt throws an exception if self.con.running is aborted

        if self.enable:
            self.enable_sensor()
        if self.notify:
            self.notify_sensor()
        if self.set_period:
            self.set_period()



        print "Sensor - "+str(self.__name__)+"is initialized in the Senosor Tag - "+str(sensor_tag.mac_address)+"\n"

    def enable_sensor(self):

        #Uses the char_write from pygattt
        sensor_tag.char_write(self.enable_handle,self.enable_value,wait_for_response=True)
        state = sensor_tag.char_read_hnd(self.enable_handle)
        if state:
            print "Enabled \n"
        else:
            print "Enable unsuccesfull \n"
            raise sensor_error("Enable unsuccesful. Aborted \n")

    def notify_sensor(self):
        sensor_tag.char_write(self.notify_handle,self.noftify_value,wait_for_response=True)
        print "Notification enabled \n" + "Value: " str(sensor_tag.char_read_hnd(self.notify_handle) + "\n" #Checking should be made more rigorous.
    def set_period(self):
        sensor_tag.char_write(self.period_handle,self.period_value,wait_for_response=True)
        print "Period set \n" + "Value: " str(sensor_tag.char_read_hnd(self.period_handle) + "\n" #Checking should be made more rigorous.
    #def disable(self): - To do:


def read_notification_output(sensor_tag,handle_to_read):
    f = sensor_tag.con.logfile
    f.truncate(0)
    substring = "Notification handle :" + str(handle_to_read)
    data_sen= 0
    while True:
        time.sleep(0.100)
        data = f.readlines()
        for line in data:
            if substring in line:
                data_sen = line[36:44]
                print data_sen

        f.truncate(0)





sensor_tag = pygattt.BluetoothLeDevice('90:59:AF:0B:83:25',bond=False,connect=True,verbose=True)
accel_list_handles = [52,'03','00',48,49,'0100',55,'10'] 
accel = sensor(sensor_tag,accel_list_handles)
read_notification_output(sensor_tag,'0x0030')
































