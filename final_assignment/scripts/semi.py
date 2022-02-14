#! /usr/bin/env python

import rospy
import time
from move_base_msgs.msg import MoveBaseActionGoal
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from actionlib_msgs.msg import GoalID
import termios
import sys, tty

#send velocity that was stated by terminal
pub_velocity = rospy.Publisher("cmd_vel", Twist, queue_size = 10)

#message to tell how to control
def wasdq():
    print("Semi-manual mode acivated: collisions are avoided\n")
    print("Press 'W' key: to move forward")
    print("Press 'A' key: to turn left")
    print("Press 'S' key: to move backward")
    print("Press 'D' key: to turn right")

    print("Press 'Q' key: to quit\n")

#take user input without pressing enter at each instance
def getch():
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()

#responses for each element in the instance of user input
def user_input():
    linear_vel = 0
    angular_vel = 0
    exit_system = False
    control_letter = getch()

    if control_letter == 'w' or control_letter == 'W':
        return 1.0, 0, False
    elif control_letter == 'a' or control_letter == 'A':
        return 0, 2, False
    elif control_letter == 's' or control_letter == 'S':
        return -1.0, 0, False
    elif control_letter == 'd' or control_letter == 'D':
        return 0, -2, False

    elif control_letter == 'q' or control_letter == 'Q':
        return 0, 0, True
    else:
        print("Wrong button\n")
    return linear_vel, angular_vel, exit_system

#takes the ranges of laser input data and sorts them from minimum to maximum value
def min_distance(data):
    min_DistanceLeft = 30
    min_DistanceFront = 30
    min_DistanceRight = 30
    for i in range(0, 4*45):
        if data[i] < min_DistanceLeft:
            min_DistanceLeft = data[i]
    for i in range(4*45, 4*135):
        if data[i] < min_DistanceFront:
            min_DistanceFront = data[i]
    for i in range(4*135, len(data)):
        if data[i] < min_DistanceRight:
            min_DistanceRight = data[i]
    return min_DistanceLeft, min_DistanceFront, min_DistanceRight

#function that sends corresponding data to the robot and set's up the process
def ui_semi():

    #conditions for execution
    #minimum safe distance is set as distance_obst
    exit_system = 0
    distance_obst = 1
    wasdq()

    #initiate Twist element to send the linear and angular speed
    msg_twist = Twist()
    msg_twist.linear.y = 0
    msg_twist.linear.z = 0
    msg_twist.angular.x = 0
    msg_twist.angular.y = 0

    while not exit_system:

        [msg_twist.linear.x, msg_twist.angular.z, exit_system] = user_input()

        laser = rospy.wait_for_message("/scan", LaserScan)
        laser_data = laser.ranges
        [min_left, min_front, min_right] = min_distance(laser_data)

        #stop the robot is obstacle is on the left
        if min_left < distance_obst:
            if msg_twist.angular.z < 0:
                print("Obstacle on the left \n")
                msg_twist.angular.z = 0
        #stop the robot is obstacle is in front
        elif min_front < distance_obst:
            if msg_twist.linear.x > 0:
                print("Obstacle in front \n")
                msg_twist.linear.x = 0
        #stop the robot is obstacle is on the right
        elif min_right < distance_obst:
            if msg_twist.angular.z > 0:
                print("Obstacle on the right \n")
                msg_twist.angular.z = 0

        #considering all the conditions above satisfied, send the target linear and angular velocity
        pub_velocity.publish(msg_twist)

        #allows to move
        time.sleep(0.2)
        msg_twist.linear.x = 0
        msg_twist.angular.z = 0
        pub_velocity.publish(msg_twist)

    return 1
