import pexpect
import time
import sys
import pygattt
import os
import numpy

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
        self.enable = enable
        self.notify = notify
        self.set_period = set_period
        self.verbose = verbose
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
            self.set_perd()



        print "Sensor - "+"is initialized in the Senosor Tag - "+str(sensor_tag.mac_address)+"\n" #+str(self.__name__)

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
        sensor_tag.char_write(self.notify_handle,self.notify_value,wait_for_response=True)
        print ("Notification enabled " + "Value: " + str(sensor_tag.char_read_hnd(self.notify_handle))+'\n' )                                           
                                                                #Checking should be made more rigorous.
                                                          
    def set_perd(self):                                                          
        sensor_tag.char_write(self.period_handle,self.period_value,wait_for_response=True)
        print "Period set \n" + "Value: " + str(sensor_tag.char_read_hnd(self.period_handle)) + "\n" #Checking should be made more rigorous.
    #def disable(self): - To do:


def read_notification_output(sensor_tag,handles_to_read): ## log.txt is the log file of the pygatt spawn of pexepect. Need to grab the pointer from the sensor_tag object itself.
    f = open('log.txt','w+')
    f.truncate(0)
    #string_to_read = []
    #string_to_read.append(str(handle_to_read[0]))#Accel
    #string_to_read.append(str(handle_to_read[1]))#Gyro
    #string_to_read.append(str(handle_to_read[2]))#Magneto """"Notification handle = " + """
    output = {}
    
    for handle in handles_to_read:
        output[handle] = '0 0 0'

    plot_data=[]
    FIFO_size = 50
    element = ['gyro':[0,0,0],'magneto':[0,0,0],'accel',[0,0,0]]
    
    for n in range(FIFO_size):
        plot_data.append(element)
    
    
    data_sen= 0
    while True:
        time.sleep(0.100)
        os.system('clear')
        notification_out_tty = f.readlines()
        for line in notification_out_tty:
            for specific_sensor_handle in handles_to_read:
                if specific_sensor_handle in line:                  
                    data_sen = line[36:44]                                                               #[22:28])
                    output[specific_sensor_handle] = str(data_sen)#[22:28]]
                    #print output
                    cnvted_val = conv_val(output)
                    plot_data.append(cnvted_val)
                    plot_data.pop(0)
                    
                    

                     
        print cnvted_val       
        f.truncate(0)

def conv_val(output):
    conv_value = {}
    #handle_sensor_functions = 
    for handle in output: #handle is the key of this dictionary
        if handle == '0x0030':
            conv_value['accel'] = accel_convert(output[handle])
        elif handle == '0x0046':
            conv_value['magneto'] = magneto_convert(output[handle])
        elif handle == '0x0060':
            conv_value['gyro'] = gyro_convert(output[handle])
        #conv_val[handle] = handle_sensor_functions[handle](output[handle])
    return conv_value



def accel_convert(hex_val):
##    val = hex_val.split()
##    int_values = []
##    for reading in val:
##        int_values.append(int(str(reading),16)*9.8/64.0)
##    return int_values
    #print hex_val
    hex_val_split = hex_val.split()
    val_x = int(hex_val_split[0],16)*9.8/(64.0)
    val_y = int(hex_val_split[1],16)*9.8/(64.0)
    val_z = int(hex_val_split[2],16)*9.8/(64.0)
    return [val_x,val_y,val_z]

def gyro_convert(hex_val):
    #print hex_val
    hex_val_split = hex_val.split()
    val_x = int(hex_val_split[0],16)*1.0/(65536/500)
    val_y = int(hex_val_split[1],16)*1.0/(65536/500)
    val_z = int(hex_val_split[2],16)*1.0/(65536/500)
    return [val_x,val_y,val_z]
    
def magneto_convert(hex_val):
    #print hex_val
    hex_val_split = hex_val.split()
    val_x = int(hex_val_split[0],16)*1.0/(65536/2000)
    val_y = int(hex_val_split[1],16)*1.0/(65536/2000)
    val_z = int(hex_val_split[2],16)*1.0/(65536/2000)
    return [val_x,val_y,val_z]




sensor_tag = pygattt.BluetoothLeDevice('90:59:AF:0B:83:25',bond=False,connect=True,verbose=True)
#list_handles goes in this order:
        # list_handles[0] = enable_handle - the decimal number version of the handle
        # list_handles[1] = enable_value - the string to write to to enable the sensor accordingly
        # lsit_handles[2] = disable_value - The string to write to disable the value 
        # list_handles[3] = data_handle - int
        # list_handles[4] = notify_handle - int
        # list_handles[5] = notify_value - str (The pygatt source code has been modified accordingly to write strings
                                                #using the def ""char-write"")
        # list_handles[6] = period_handle - int
        # list_handles[7] = period_value - str
        #accel_list_handles = [52,'03','00',48,49,'0100',55,'10'] - for 10 milliseconds

accel_list_handles = [52,'02','00',48,49,'0100',55,'10']
gyro_list_handles =  [100,'07','00',96,97,'0100',103,'10']
magneto_list_handles = [74,'01','00',70,71,'0100',77,'10']


accel = sensor(sensor_tag,accel_list_handles)
gyro = sensor(sensor_tag,gyro_list_handles)
magneto_list_handles= sensor(sensor_tag,magneto_list_handles)

#handle_name = [(0x0030,accel_convert),(0x0060,gyro_convert),(0x0046,magneto_convert)]
                        

read_notification_output(sensor_tag,['0x0030','0x0060','0x0046'])

































