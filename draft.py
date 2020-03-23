#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sound import Sound
from ev3dev2.wheel import EV3Tire
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
        self.distance_right=0
        self.distance_left = 1
        self.co = True
        self.mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, 16 * 8)

    # functions that turn on both motors for certain rotation at certain percentage of its maximum speed
    def move(self, speed, rotations):
        self.drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), rotations)

    def check_angle(self):
        self.move(20, -0.5)

        while True:
            # check right
            self.mB.on_for_degrees(speed=20, degrees=15)
            self.distance_right = 0
            while self.cl.value() != 1:
                self.mdiff.on_for_distance(SpeedRPM(40),10)
                self.distance_right +=1
            for d in range (0,self.distance_right,1):
                self.mdiff.on_for_distance(SpeedRPM(40), -10)
            self.mB.on_for_degrees(speed=20, degrees=-15)
            # check left
            self.mC.on_for_degrees(speed=20, degrees=15)
            self.distance_left = 0
            while self.cl.value() != 1:
                self.mdiff.on_for_distance(SpeedRPM(40),10)
                self.distance_left +=1
            for d in range (0,self.distance_right,1):
                self.mdiff.on_for_distance(SpeedRPM(40), -10)
            self.mB.on_for_degrees(speed=20, degrees=-15)

            if self.distance_right < self.distance_left:
                self.mB.on_for_degrees(speed=20, degrees=2)
            elif self.distance_right > self.distance_left:
                self.mC.on_for_degrees(speed=20, degrees=2)
            else:
                self.move(20, 0.6)
                break


    def count_tiles(self, tile_colour):
        while self.count < 13:
            # detects a black tile
            if self.cl.color == 1:
                self.count += 1
                if self.count == 1:
                    self.mB.run_to_rel_pos(position_sp=350, speed_sp=360, stop_action="brake")
                    self.sound.speak(self.count)
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 0.5)
                elif 1 < self.count < 7:
                    self.sound.speak(self.count)
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 1.2)
                elif self.count == 7:
                    self.mB.run_to_rel_pos(position_sp=345, speed_sp=360, stop_action="brake")
                    self.sound.speak(self.count)
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 1.9)
                elif 7 < self.count < 13:
                    self.sound.speak(self.count)
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 2.3)
                elif self.count == 13:
                    self.drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 1.1)
                    self.mC.run_to_rel_pos(position_sp=345, speed_sp=360, stop_action="brake")
                    self.sound.speak(self.count)
                    break



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

