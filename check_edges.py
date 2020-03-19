#!/usr/bin/env python3
from ev3dev.ev3 import *
from ev3dev2.motor import *
from time import sleep, time
from ev3dev2.sensor.lego import ColorSensor, SoundSensor


class Robot:

    def __init__(self):
        self.cl = ColorSensor()
        self.cl.mode = 'COL-COLOR'
        self.sou = Sound()
        self.mB = LargeMotor('outB')
        self.mC = LargeMotor('outC')

    def turn_right(self, count_left, count_right):
        while True:
            if self.cl.value() == 1 and count_left == 0:
                count_right += 1
                self.mB.run_to_rel_pos(position_sp=10, speed_sp=100, stop_action="brake")
            elif self.cl.value() != 1 and count_left == 0:
                # print(count_1)
                self.sou.speak("count one is", count_right)
                count_left = count_right
                self.mB.stop()
            elif count_left != 0:
                for i in range(count_left, 0, -1):
                    count_left -= 1
                    self.mB.run_to_rel_pos(position_sp=-10, speed_sp=100)
                print(count_left)
                self.mB.stop()
                self.sou.speak("count two is", count_left)
                return count_right
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

    def turn_left(self, count_left, count_right):
        while True:
            if self.cl.value() == 1 and count_right == 0:
                count_left += 1
                self.mC.run_to_rel_pos(position_sp=10, speed_sp=100, stop_action="brake")
            elif self.cl.value() != 1 and count_right == 0:
                # print(count_1)
                self.sou.speak("count one is", count_left)
                count_right = count_left
                self.mC.stop()
            elif count_right != 0:
                for i in range(count_right, 0, -1):
                    count_right -= 1
                    self.mC.run_to_rel_pos(position_sp=-10, speed_sp=100)
                print(count_right)
                self.mC.stop()
                self.sou.speak("count two is", count_right)
                return count_left
                break


if __name__ == "__main__":
    r = Robot()
    check_right = r.turn_right(0, 0)
    check_left = r.turn_left(0, 0)



