#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sound import Sound
from time import sleep


class Robot:

    # Initialise all the things we need in the program
    def __init__(self):
        # colour sensor instance
        self.cl = ColorSensor()
        self.cl.mode = 'COL-COLOR'
        # sound class instance
        self.sound = Sound()
        # motor class instance
        self.mB = LargeMotor('outB')
        self.mC = LargeMotor('outC')
        self.drive = MoveTank(OUTPUT_B, OUTPUT_C)
        # ultrasonic sensor instance
        self.us = UltrasonicSensor()
        self.us.mode = 'US-DIST-CM'
        # varaible that helps to count the tile
        self.count = 0
        self.count_1 = 0
        self.co = True
    # functions that turn on both motors for certain rotation at certain percentage of its maximum speed
    def move(self, speed, rotations):
        self.drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), rotations)

    def count_right(self, tile_colour, degree_turn):
        self.count_1 = 0
        while self.cl.value() == tile_colour:
            self.count_1 += 1
            self.mB.on_for_degrees(speed=20, degrees=degree_turn)
        self.mB.stop()
        self.sound.speak(self.count_1)
        for degree in range(0, self.count_1, 1):
            self.mB.on_for_degrees(speed=20, degrees=-degree_turn)
        return self.count_1

    def count_left(self, tile_colour, degree_turn):
        self.count_1 = 0
        while self.cl.value() == tile_colour:
            self.count_1 += 1
            self.mC.on_for_degrees(speed=20, degrees=degree_turn)
        self.mC.stop()
        self.sound.speak(self.count_1)
        for degree in range(0, self.count_1, 1):
            self.mC.on_for_degrees(speed=20, degrees=-degree_turn)
        return self.count_1

    def compare_left_right(self, left_count, right_count):
        if left_count > right_count:
            diff = left_count - right_count
            change = int(diff / 2)
            for degree in range(0, change, 1):
                self.mC.on_for_degrees(speed=20, degrees=20)
        else:
            differ = right_count - left_count
            change = int(differ / 2)
            for degree in range(0, change, 1):
                self.mB.on_for_degrees(speed=20, degrees=20)



    def count_tiles(self, tile_colour):
        while self.count < 13:
            # detects a black tile
            if self.cl.color == tile_colour:
                self.count += 1
                if self.count == 1:
                    self.mB.run_to_rel_pos(position_sp=347.5, speed_sp=360, stop_action="brake")
                    self.sound.speak(self.count)
                    self.move(20, 0.5)
                elif 1 < self.count < 7:
                    self.sound.speak(self.count)
                    self.move(20, 1.15)
                elif self.count == 7:
                    right_count = r.count_right(1, 20)
                    sleep(2)
                    left_count = r.count_left(1, 20)
                    sleep(2)
                    r.compare_left_right(left_count, right_count)
                    sleep(2)
                    self.mB.run_to_rel_pos(position_sp=345, speed_sp=360, stop_action="brake")
                    self.sound.speak(self.count)
                    self.move(20, 2.1)
                elif 7 < self.count < 13:
                    self.sound.speak(self.count)
                    self.move(20, 2.3)
                elif self.count == 13:
                    self.sound.speak(self.count)
                    self.move(20, 1.0)
                    sleep(0.2)
                    self.mC.run_to_rel_pos(position_sp=346, speed_sp=360, stop_action="brake")
                    sleep(2)
                    break

            elif self.cl.color != tile_colour:
                if self.count < 7:
                    self.count -= 1
                    self.move(20, -1.15)
                    right_count = r.count_right(1, 20)
                    sleep(2)
                    left_count = r.count_left(1, 20)
                    sleep(2)
                    r.compare_left_right(left_count, right_count)
                    sleep(2)

                elif 7 <= self.count < 13:
                    self.count -= 1
                    self.move(20, -2.3)
                    right_count = r.count_right(1, 20)
                    sleep(2)
                    left_count = r.count_left(1, 20)
                    sleep(2)
                    r.compare_left_right(left_count, right_count)
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
    # from S tile to first
    r.move(20, 0.65)
    # start to move from the first black tile to the 13th black tile
    r.count_tiles(1)
    # after 13th black tile and move towards the tower and push it off
    r.detect_tower(200)



