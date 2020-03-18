#!/usr/bin/env python3
from ev3dev.ev3 import *
from ev3dev2.motor import *
from time import sleep, time
from ev3dev2.sensor.lego import ColorSensor, SoundSensor

cl = ColorSensor()
cl.mode = 'COL-COLOR'
sou = Sound()
count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0

mB = LargeMotor('outB')
mC = LargeMotor('outC')

while True:
    if cl.value() == 1 and count_2 == 0:
        count_1 += 1
        mB.run_to_rel_pos(position_sp=10, speed_sp=100, stop_action="brake")
    elif cl.value()!=1 and count_2 == 0:
        # print(count_1)
        sou.speak("count one is", count_1)
        count_2=count_1
        mB.stop()
    elif count_2 != 0 :
        for i in range (count_2, 0, -1) :
            count_2-=1
            mB.run_to_rel_pos(position_sp = -10, speed_sp = 100)
        print(count_2)
        mB.stop()
        sou.speak("count two is", count_2)
        break

while True:
    if cl.value() == 1 and count_4 == 0:
        count_3 += 1
        mC.run_to_rel_pos(position_sp=10, speed_sp=100, stop_action="brake")
    elif cl.value()!= 1 and count_4 == 0:
        # print(count_1)
        sou.speak("count one is", count_3)
        count_4=count_3
        mC.stop()
    elif count_4 != 0 :
        for i in range (count_4, 0, -1) :
            count_4-=1
            mC.run_to_rel_pos(position_sp = -10, speed_sp = 100)
        print(count_4)
        mC.stop()
        sou.speak("count two is", count_4)
        break

    # sou.speak("count two is", count_2)

    # if cl.value() == 1 and count_2 == 0:
    #     count_2 += 1
    #     mC.run_to_rel_pos(position_sp =10, speed_sp = 100, stop_action = "brake")
    # elif cl.value() != 1and count_2 != 0:
    #     mC.run_to_rel_pos(position_sp = 10, speed_sp=-100, stop_action = "brake")
    #
    # if cl.value() == 1 and count_2 != 0 and count_1 != 0:
    #     sleep(5)
