#!/usr/bin/env python3.5
import subprocess
from sense_hat import SenseHat
import io
sense = SenseHat()
sense.clear()
import time

r = 255
g = 0
b = 0

#for ip in $(seq 1 254); do ping -c 1 192.168.1.$ip>/dev/nul;
#    [ $? -eq 0 ] && echo "192.268.1.$ip UP" || : ;
#done

#sense.clear((r, g, b))
#blue = (0, 0, 255)
#yellow = (255, 255, 0)
#sense.show_message("GARY WAS HERE! ASH IS A LOSER!", text_colour=yellow, back_colour=blue)
while(1):
    temp = sense.get_temperature()
    temp = temp * 1.8
    temp = temp + 32
    f = open("/sys/class/thermal/thermal_zone0/temp", "r")
    t = f.readline()
    t = float(int(t))/1000
    t = t * 1.8
    t = t + 32


    cputemp = "CPU temp: " + str(t)
    print cputemp
    print(temp)

    temp_calibrated = temp -((t - temp)/5.466)
    print temp_calibrated
    time.sleep(5)
#sense.set_pixel(2,2,(0,0,255))
#sense.set_pixel(4, 2, (0, 0, 255))
#sense.set_pixel(3,4,(100,0,0))
#sense.set_pixel(1,5(255,0,0))
#sense.set_pixel(2,6,(255,0,0))
#sense.set_pixel(3,6,(255,0,0))  
#sense.set_pixel(4,6,(255,0,0))
#sense.set_pixel(5,5,(255,0,0))

while False:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x=round(x,0)
    y=round(y,0)
    z=round(z,0)

    print("x={0}, y={1}, z={2}".format(x,y,z))

    if x == -1:
        sense.set_rotation(180)
    elif y == 1:
        sense.set_rotation(90)
    elif y == -1:
        sense.set_rotation(270)
    else:
        sense.set_rotation(0)
