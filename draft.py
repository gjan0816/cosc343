#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sound import Sound
from time import sleep


class Robot:

    def __init__(self):
        self.cl = ColorSensor()
        self.cl.mode = 'COL-COLOR'
        self.sou = Sound()
        self.mB = LargeMotor('outB')
        self.mC = LargeMotor('outC')
        self.us = UltrasonicSensor()
        self.us.mode = 'US-DIST-CM'
        self.drive = MoveTank(OUTPUT_B, OUTPUT_C)
        self.count = 0
        self.sound = Sound()
        self.count_1 = 0
        self.count_2 = 0
        self.correct_value = 380
        self.co = True

    def turn_right(self, tile_colour, degree_turn):
        self.count_1 = 0
        while self.cl.value() == tile_colour:
            self.count_1 += 1
            self.mB.on_for_degrees(speed=20, degrees=degree_turn)
        self.mB.stop()
        # self.mB.run_to_rel_pos(position_sp=-degree_turn, speed_sp=100, stop_action="brake")
        self.sound.speak(self.count_1)
        for degree in range(0, self.count_1, 1):
            self.mB.on_for_degrees(speed=20, degrees=-degree_turn)
        return self.count_1

    def turn_left(self, tile_colour, degree_turn):
        self.count_1 = 0
        while self.cl.value() == tile_colour:
            self.count_1 += 1
            self.mC.on_for_degrees(speed=20, degrees=degree_turn)
        self.mC.stop()
        # self.mB.run_to_rel_pos(position_sp=-degree_turn, speed_sp=100, stop_action="brake")
        self.sound.speak(self.count_1)
        for degree in range(0, self.count_1, 1):
            self.mC.on_for_degrees(speed=20, degrees=-degree_turn)
        return self.count_1

    def compare_L_R(self, L_count, R_count):
        if L_count > R_count:
            differ = L_count - R_count
            change = int(differ / 2)
            for degree in range(0, change, 1):
                self.mC.on_for_degrees(speed=20, degrees=20)
        else:
            differ = R_count -  L_count
            change = int(differ/2)
            for degree in range(0, change, 1):
                self.mB.on_for_degrees(speed=20, degrees=20)

    def move(self, speed):
        self.drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), 0.65)

    def count_tiles(self, tile_colour):
        while self.count < 13:
            # detects a black tile
            if self.cl.color == tile_colour:
                self.count += 1
                if self.count == 1:
                    self.mB.run_to_rel_pos(position_sp=347.5, speed_sp=360, stop_action="brake")
                    self.sound.speak(self.count)
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 0.5)
                elif 1 < self.count < 7:
                    self.sound.speak(self.count)
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 1.15)
                elif self.count == 7 and self.co:
                    self.mB.run_to_rel_pos(position_sp=345, speed_sp=360, stop_action="brake")
                    self.sound.speak(self.count)
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 2.1)
                elif 7 < self.count < 13:
                    self.sound.speak(self.count)
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 2.3)
                elif self.count == 13:
                    self.sound.speak(self.count)
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 1.0)
                    sleep(0.2)
                    self.mC.run_to_rel_pos(position_sp=346, speed_sp=360, stop_action="brake")
                    sleep(2)
                    break

            elif self.cl.color != tile_colour:
                if self.count < 7:
                    self.count -= 1
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), -1.15)
                    R_count = r.turn_right(1, 20)
                    sleep(2)
                    L_count = r.turn_left(1, 20)
                    sleep(2)
                    r.compare_L_R(L_count, R_count)
                    sleep(2)

                elif 7 <= self.count < 13:
                    self.count -= 1
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), -2.3)
                    R_count = r.turn_right(1, 20)
                    sleep(2)
                    L_count = r.turn_left(1, 20)
                    sleep(2)
                    r.compare_L_R(L_count, R_count)
                    sleep(2)
                    self.co = False

    def detect_tower(self, target_distance):
        while True:
            self.mB.run_forever(speed_sp=300)
            self.mC.run_forever(speed_sp=300)
            if self.us.value() < target_distance:
                self.mB.stop(stop_action="brake")
                self.mC.stop(stop_action="brake")
                self.sound.speak("Enemy detected")

                break

        sleep(1)
        self.mB.run_forever(speed_sp=500)
        self.mC.run_forever(speed_sp=500)

        sleep(2)
        self.mB.stop(stop_action="brake")
        self.mC.stop(stop_action="brake")

        self.sound.speak("Success!")


if __name__ == "__main__":
    r = Robot()
    r.move(20)
    r.count_tiles(1)
    r.detect_tower(200)

