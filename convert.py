def accel(hex_val):
    print hex_val
    hex_val_split = hex_val.split()
    val_x = int(hex_val_split[0],16)#*9.8/(64.0)
    val_y = int(hex_val_split[1],16)#*9.8/(64.0)
    val_z = int(hex_val_split[2],16)#*9.8/(64.0)
    return [val_x,val_y,val_z]

def gyro(hex_val):
    hex_val_split = hex_val.split()
    val_x = hex_val_split[1]+hex_val_split[0]
    print '0000000000000\n'
    print val_x
    print '0000000000000\n'
    val_x = int(val_x,16)#*1.0/(65536/500)
    val_y = hex_val_split[3]+hex_val_split[2]
    print '0000000000000\n'
    print val_y
    print '0000000000000\n'
    val_y = int(val_y,16)#*1.0/(65536/500)
    val_z = hex_val_split[5]+hex_val_split[4]
    print '0000000000000\n'
    print val_z
    print '0000000000000\n'
    val_z = int(val_z,16)#*1.0/(65536/500)
    return [val_x,val_y,val_z]
    
def magneto(hex_val):
    hex_val_split = hex_val.split()
##    val_x = int(hex_val_split[0],16)*1.0/(65536/2000)
##    val_y = int(hex_val_split[1],16)*1.0/(65536/2000)
##    val_z = int(hex_val_split[2],16)*1.0/(65536/2000)
    val_x = int(hex_val_split[0]+hex_val_split[1],16)#*1.0/(65536/500)
    val_y = int(hex_val_split[2]+hex_val_split[3],16)#*1.0/(65536/500)
    val_z = int(hex_val_split[4]+hex_val_split[5],16)#*1.0/(65536/500)
    return [val_x,val_y,val_z]
#added space for more conversions:
