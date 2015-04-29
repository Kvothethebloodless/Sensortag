def accel(hex_val):
    hex_val_split = hex_val.split()
    val_x = int(hex_val_split[0],16)*9.8/(64.0)
    val_y = int(hex_val_split[1],16)*9.8/(64.0)
    val_z = int(hex_val_split[2],16)*9.8/(64.0)
    return [val_x,val_y,val_z]

def gyro(hex_val):
    hex_val_split = hex_val.split()
    val_x = int(hex_val_split[0],16)*1.0/(65536/500)
    val_y = int(hex_val_split[1],16)*1.0/(65536/500)
    val_z = int(hex_val_split[2],16)*1.0/(65536/500)
    return [val_x,val_y,val_z]
    
def magneto(hex_val):
    hex_val_split = hex_val.split()
    val_x = int(hex_val_split[0],16)*1.0/(65536/2000)
    val_y = int(hex_val_split[1],16)*1.0/(65536/2000)
    val_z = int(hex_val_split[2],16)*1.0/(65536/2000)
    return [val_x,val_y,val_z]
#added space for more conversions:
