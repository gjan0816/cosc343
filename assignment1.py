#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sound import Sound
from ev3dev2.wheel import EV3Tire
from time import sleep

# test with a robot that:
# - uses the standard wheels known as EV3Tire
# - wheels are 16 studs apart
mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, 16 * 8)
cl = ColorSensor()
cl.mode = 'COL-COLOR'

us = UltrasonicSensor()
us.mode = 'US-DIST-CM'

drive = MoveTank ( OUTPUT_B,OUTPUT_C )
mB = LargeMotor('outB')
mC = LargeMotor('outC')

count = 0
sound = Sound()

count_1 = 0
count_2 = 0
correct_value = 380
result = 0

drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 0.65)

while count < 13:
    # detects a black tile
    if cl.color == 1:
        count += 1
        if count == 1:
            mB.run_to_rel_pos(position_sp=347.5, speed_sp=360, stop_action="brake")
            sound.speak(count)
            drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 0.5)
        elif 1 < count < 7:
            sound.speak(count)
            drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 1.2)
        elif count == 7:
            mB.run_to_rel_pos(position_sp=345, speed_sp=360, stop_action="brake")
            sound.speak(count)
            drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 1.9)
        elif 7 < count < 13:
            sound.speak(count)
            drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 2.3)
        elif count == 13:
            sound.speak(count)
            drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 1.0)
            sleep(0.2)
            mC.run_to_rel_pos(position_sp=346, speed_sp=360, stop_action="brake")
            sleep(2)
            break
    # do not detect a black tile
    # move back and correct its position(not complete)
    elif cl.color != 1:
        if count < 7:
            count -= 1
            drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), -1.2)
            count_1 = 0
            count_2 = 0
            result =0
            while True:
                if cl.value() == 1 and count_2 == 0:
                    count_1 += 1
                    mB.run_to_rel_pos(position_sp=10, speed_sp=100, stop_action="brake")
                elif cl.value() != 1 and count_2 == 0:
                    count_2 = count_1
                    mB.stop()
                elif count_2 != 0:
                    for i in range(correct_value, 0, -1):
                        mB.run_to_rel_pos(position_sp=-10, speed_sp=100)
                    mB.stop()
                    break

        elif 7 < count < 13:
            count -= 1
            result = 0
            count_1 = 0
            count_2 = 0
            drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), -2.1)
            while True:
                if cl.value() == 1 and count_2 == 0:
                    count_1 += 1
                    mB.run_to_rel_pos(position_sp=10, speed_sp=100, stop_action="brake")
                elif cl.value() != 1 and count_2 == 0:
                    count_2 = count_1
                    mB.stop()
                elif count_2 != 0:
                    for i in range(correct_value, 0, -1):
                        mB.run_to_rel_pos(position_sp=-10, speed_sp=100)
                    mB.stop()
                    break


while True:
    mB.run_forever(speed_sp=300)
    mC.run_forever(speed_sp=300)
    if us.value() < 200:
        mB.stop(stop_action="brake")
        mC.stop(stop_action="brake")
        sound.speak("Enemy detected")

        break

sleep(1)
mB.run_forever(speed_sp=500)
mC.run_forever(speed_sp=500)

sleep(2)
mB.stop(stop_action="brake")
mC.stop(stop_action="brake")

sound.speak("Success!")


