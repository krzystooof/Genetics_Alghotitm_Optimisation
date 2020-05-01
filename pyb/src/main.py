# main.py -- put your code here!
# Code below is essentialy hello world for pyboard
import pyb

switch = pyb.Switch()
leds = [pyb.LED(i+1) for i in range(4)]
accel = pyb.Accel()

i = 0
while not switch():
    y = accel.y()
    i = (i + (1 if y > 0 else -1)) % len(leds)
    leds[i].toggle()
    pyb.delay(10 * max(1, 20 - abs(y)))
