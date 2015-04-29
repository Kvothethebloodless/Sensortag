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
                    self.sent_reading = str(line[36:])        
                    self.sent_reading = self.sent_reading[0:len(self.sent_reading)-3]                  #To remove the trailing '\r\n'                   
                    self.raw_output[specific_sensor_handle] = str(self.sent_reading)  
                    
        self.f.truncate(0)
        return self.raw_output


