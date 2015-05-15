import pexpect
import time
import sys
import pygattt
import os
import numpy
import convert
import notifi
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np


global calc_output
global raw_output




accel_list_handles = [52,'01','00',48,49,'0100',55,'10']
gyro_list_handles =  [100,'07','00',96,97,'0100',103,'10']
magneto_list_handles = [74,'01','00',70,71,'0100',77,'10']

class sensor_error(Exception): pass

class sensor(pygattt.BluetoothLeDevice):
    def __init__(self,sensor_tag,list_handles,calc_func_pointer,verbose=True,enable=True,notify=True,set_period=True):
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
        self.calc_fun_pointer = calc_func_pointer
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

    def calculate(self,hex_val):
        val = self.calc_fun_pointer(hex_val)
        return val
class plotting():
    def __init__(self):
        #self.data = data
        self.fig_accel = plt.figure()
        self.ax_accel = plt.axes(xlim = (0,100), ylim = (0,64))
              
        #self.fig_gyro = plt.figure()
        #self.ax_gyro = plt.axes(xlim = (0,100), ylim = (-5,120))
        
        #self.fig_magneto = plt.figure()
        #self.ax_magneto = plt.axes(xlim = (0,100), ylim = (-10,10))


        self.accel_anim_objects = [plt.plot([], [])[0] for _ in range(3)]
        print self.accel_anim_objects
        #self.gyro_anim_objects = [plt.plot([], [])[0] for _ in range(3)]
        #self.magneto_anim_objects = [plt.plot([], [])[0] for _ in range(3)]

        #self.anim_init()
        #self.anim_init()
        #self.anim_init()
        
        

    def anim_init(self):
        zero_data = list(np.zeros(100))
        hundred = list(np.arange(1,101))
        for animobj in self.accel_anim_objects:
            animobj.set_data(hundred,zero_data)

        print self.accel_anim_objects[0:2]
        return self.accel_anim_objects
        
            
            
            
    def animate(self,i):
        print '------- \n'
        j = 0
        n = 1
        #for n in range(3):
        
        get_out(raw_output)
        print raw_output
        print '\n'
        animobj = self.accel_anim_objects[n]
        dummy_list= animobj.get_ydata()
        dummy_list.pop(0)
        dummy_list.append(calc_output['0x0030'][n])
        print '$$$$$$$$$$$$$$ \n'
        print calc_output['0x0030'][n]
        print '\n $$$$$$$$$$$$$$ \n'
        animobj.set_ydata(dummy_list)
        
        print animobj.get_ydata()
       
        print '\n'

        print '^^^^^^^^^^^^^^^^\n'
        print calc_output['0x0060'][n]
        print '^^^^^^^^^^^^^^^^\n'
        
        return [self.accel_anim_objects[n]]
    
def get_out(raw_output):
    raw_output = notif.parse_output(raw_output)   

    #output_2 = dict([(handle,dict_conv_func[str(handle)](output[handle])) for handle in data_list_handles])
    for handle in data_list_handles:
        calc_output[handle] = dict_conv_func[handle](raw_output[handle])
    print calc_output
    

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

accelerometer = sensor(sensor_tag,accel_list_handles,convert.accel)
gyroscope = sensor(sensor_tag,gyro_list_handles,convert.gyro)
#magnetometer= sensor(sensor_tag,magneto_list_handles,convert.magneto)


#handle_name = [(0x0030,accel_convert),(0x0060,gyro_convert),(0x0046,magneto_convert)]

data_list_handles = ['0x0030','0x0060']#,'0x0046']
dict_conv_func = {'0x0030':accelerometer.calculate,'0x0060':gyroscope.calculate} #'0x0046':magnetometer.calculate,

zero_val = '0 0 0'
raw_output = dict([(handle,zero_val) for handle in data_list_handles])


                    
global notifi
notif = notifi.notification(sensor_tag,data_list_handles)
calc_output = {}
plot_obj = plotting()


##while True:
##    time.sleep(.100)
##    os.system('clear')

    
anim = animation.FuncAnimation(plot_obj.fig_accel, plot_obj.animate, init_func=plot_obj.anim_init, frames = 100000, interval=20, blit=True) #Currently animating only one axis acceleration. Soon going to extend it to all axes
plt.show()


 































