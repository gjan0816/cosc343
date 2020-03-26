#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.wheel import EV3Tire
from time import sleep

""" 
Robot class structure for achieving the tasks we have been given 
"""
class Robot:

    # Initialise robot's sensor and their instances. 
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
        self.mdiff = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, 16 * 8) # 8 is the distance between the 2 wheels
        # ultrasonic sensor instance
        self.us = UltrasonicSensor()
        self.us.mode = 'US-DIST-CM'
        # varaibles that helps to count the tile and check its position
        self.count_black_tile = 0
        self.distance_right=0
        self.distance_left = 0


    # function that turn on both motors for certain numbers of rotation at the certain percentage of its maximum speed
    def drive_for_rotation(self, speed, rotations):
        self.drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), rotations)

    # function that turn on both motors for certain distance at the certain number of revolution per minutes
    # 1 revolution is the wheel will travel a distance to wheel's circumference
    def drive_for_distance (self, speed, distance):
        self.mdiff.on_for_distance(SpeedRPM(speed), distance)\

    # Rotate the left/right wheel to a specific position relative to its current position at certain speed
    # right/left wheel as the pivot, not moving part

    def turn_on_left_motor_pos(self,position,speed):
        self.mB.run_to_rel_pos(position_sp=position, speed_sp=speed, stop_action="brake")

    def turn_on_right_motor_pos(self,position,speed):
        self.mC.run_to_rel_pos(position_sp=position, speed_sp=speed, stop_action="brake")

    # turn the left/right motor for certain degrees at certain speed
    # right/left motor as the pivot, not moving part

    def turn_on_left_motor_degree(self,speed,degree):
        self.mB.on_for_degrees(speed=speed, degrees=degree)

    def turn_on_right_motor_degree(self,speed,degree):
        self.mC.on_for_degrees(speed=speed, degrees=degree)

    # check whether the robot is perpendicular to the front edge of the black tile
    # if not, then correct its position till it's perpendicular to the front edge of the black tile

    def check_position(self):
        self.drive_for_rotation(20, -0.5)

        while True:
           
            # CHECK THE RIGHT DISTANCE TO BLACK TILE 
            self.turn_on_left_motor_degree(20,15)
            self.distance_right = 0
            while self.cl.value() != 1:
                self.drive_for_distance(40,10)
                self.distance_right +=1
            # Returning back to the original position
            for d in range (0,self.distance_right,1):
                self.drive_for_distance(40,-10)
            self.turn_on_left_motor_degree(20,-15)

            # CHECK THE LEFT DISTANCE TO BLACK TILE 
            self.turn_on_right_motor_degree(20,15)
            self.distance_left = 0
            while self.cl.value() != 1:
                self.drive_for_distance(40,10)
                self.distance_left +=1

            # returning back to the original position
            for d in range (0,self.distance_right,1):
                 self.drive_for_distance(40,-10)
            self.turn_on_right_motor_degree(20,-15)

            # correcting and checking its position again
            if self.distance_right < self.distance_left: # slightly shift to the right
                self.turn_on_right_motor_degree(20,2)  # turn to left for 2 degree 
            elif self.distance_right > self.distance_left: #slightly shift to the left
                self.turn_on_left_motor_degree(20,2) # turn to right for 2 degree 
            else: # when the both distances to the black tile is equal then move back to the black tile
                self.move(20, 0.6) 
                break

    #moving across the black tiles
    def count_tiles(self, targer_colour):
       
        while self.count_black_tile < 13:
            # detects a black tile
            if self.cl.color == targer_colour:
                self.count_black_tile += 1
                self.check_position()
                if self.count_black_tile == 1:
                    self.turn_right_pos(350,360)
                    self.sound.speak(self.count_black_tile)
                    self.drive_for_rotation(20, 0.5)
                elif 1 < self.count_black_tile < 7:
                    self.sound.speak(self.count_black_tile)
                    self.drive_for_rotation(20,1.2)
                elif self.count_black_tile == 7:
                    self.turn_right_pos(345,360)
                    self.sound.speak(self.count_black_tile)
                    self.drive_for_rotation(20,1.9)
                elif 7 < self.count_black_tile < 13:
                    self.sound.speak(self.count)
                    self.drive_for_rotation(20,2.3)
                elif self.count_black_tile == 13:
                    self.sound.speak(self.count_black_tile)
                    break

    # after passed 13th black tile
    def detect_tower_push_tower(self, target_distance):
        self.drive_for_rotation(20, 1.1)
        self.turn_left_pos(345, 360)
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
    r.drive_for_rotation(20, 0.65)
    # start to move from the first black tile to the 13th black tile
    r.count_tiles(1)
    # after 13th black tile and move towards the tower and push it off
    r.detect_tower_push_tower(200)
