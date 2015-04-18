import pexepct
import time
import sys
import pygattt
import os

class sensor(pygattt.BluetoothLeDevice):

    def __init__(self,sensor_tag,list_handles,verbose=True,connect=True,notify=True,set_period=True):
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
        
        self.enable_handle = list_handles[0]
        self.enable_value =  list_handles[1]
        self.data_handle =   list_handles[2]
        self.notify_handle = list_handles[3]
        self.notify_value =  list_handles[4]
        self.period_handle = list_handles[5]
        self.period_value =  list_handles[6]

        #Don't have to worry about connection handling as Pygatt throws an exception if self.con.running is aborted
        
        
