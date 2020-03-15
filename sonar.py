from ev3dev2.sensor.lego import*
from ev3dev2.motor import *
from time import sleep

mB = LargeMotor('outB')
mC = LargeMotor('outC')

us = UltrasonicSensor()
us.mode = 'US-DIST-CM'
while True:
    print(us.value())
    if us.value() >400:
        mB.run_forever(speed_sp=400)
        mC.run_forever(speed_sp=400)
    else:
        mB.stop(stop_action="brake")
        mC.stop(stop_action="brake")

sleep(1)
