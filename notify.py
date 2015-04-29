class notification():
    def __init__(self,sensor_tag,handles_to_read):
        self.handles = handles_to_read
        self.sensor_tag = sensor_tag
        self.logfile_pygatt = open('log.txt','w+')
        self.logfile_pygatt.truncate(0)
        self.f = self.logfile_pygatt
        zero_val = '0 0 0'
        self.raw_output = dict([(handle,zero_val) for handle in handles_to_read])
        self.sent_reading = 0
    def parse_output(self):
        spawn_out_tty = self.f.readlines()
        for line in spawn_out_tty:
            for specific_sensor_handle in self.handles:
                if specific_sensor_handle in line:                  
                    self.sent_reading = str(line[36:])        #[22:28])
                    self.sent_reading = self.sent_reading[0:len(self.sent_reading)-3]                  #To remove the trailing '\r\n'                     #.replace('\r\n',"")
                    self.raw_output[specific_sensor_handle] = str(self.sent_reading)  #[22:28]]
                    
        self.f.truncate(0)
        return self.raw_output





##def init():
##    f = open('log.txt','w+')
##    f.truncate(0)
##    return f
##
##def parse_notification_output(sensor_tag,handles_to_read,f=lambda open('log.txt'.): ## log.txt is the log file of the pygatt spawn of pexepect. Need to grab the pointer from the sensor_tag object itself.
##    #f = open('log.txt','w+')
##    #f.truncate(0)
##    #string_to_read = []
##    #string_to_read.append(str(handle_to_read[0]))#Accel
##    #string_to_read.append(str(handle_to_read[1]))#Gyro
##    #string_to_read.append(str(handle_to_read[2]))#Magneto """"Notification handle = " + """
##    #output = {}
##    
##    
##
##    #plot_data=[]
##    #FIFO_size = 50
##    #element = ['gyro':[0,0,0],'magneto':[0,0,0],'accel',[0,0,0]]
##    
##    #for n in range(FIFO_size):
##        #plot_data.append(element)
##    
##    
##    reading_sent= 0
##    while True:
##        time.sleep(0.100)
##        os.system('clear')
##        spawn_out_tty = f.readlines()
##        for line in spawn_out_tty:
##            for specific_sensor_handle in handles_to_read:
##                if specific_sensor_handle in line:                  
##                    reading_sent = line[36:44]                                                               #[22:28])
##                    output[specific_sensor_handle] = str(reading_sent)#[22:28]]
##                    #print output
##                    cnvted_val = conv_val(output)
##                    #plot_data.append(cnvted_val)
##                    #plot_data.pop(0)
##                    
##                    
##
##                     
##        print cnvted_val       
##        f.truncate(0)
