#! /usr/bin/env python

import rospy
import time
from move_base_msgs.msg import MoveBaseActionGoal
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from actionlib_msgs.msg import GoalID
import termios
import sys, tty

# publisher of velocity
pub_velocity = rospy.Publisher("cmd_vel", Twist, queue_size = 10)

## welcoming words and instructions
def wasdq():
    print("Semi-manual mode acivated: collisions are avoided\n")
    print("Press 'W' key: to move forward")
    print("Press 'A' key: to turn left")
    print("Press 'S' key: to move backward")
    print("Press 'D' key: to turn right")

    print("Press 'Q' key: to quit\n")

# function for convenient usage enter inputs
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

# Control buttons for robot
def user_input():
    linear_vel = 0
    angular_vel = 0
    exit_system = False
    control_letter = getch()

    ## buttons for movement (forward, backward, right, left) and exit
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

# for detecting the minimal distance until obstacle from all sides
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

# main function for option three
def ui_semi():
    exit_system = 0
    distance_obst = 1 # Variable to set the minimal safe distance
    wasdq()

    msg_twist = Twist()
    msg_twist.linear.y = 0
    msg_twist.linear.z = 0
    msg_twist.angular.x = 0
    msg_twist.angular.y = 0

    # until not exitting from system
    while not exit_system:

        ## start controlling the robot and publish
        [msg_twist.linear.x, msg_twist.angular.z, exit_system] = user_input()

        ## consider the laser distance_wall for obstacle avoidance
        laser = rospy.wait_for_message("/scan", LaserScan)
        laser_data = laser.ranges
        [min_left, min_front, min_right] = min_distance(laser_data)

        ## distance to wall from left
        if min_left < distance_obst:
            if msg_twist.angular.z < 0:
                print("Obstacle from the left \n")
                msg_twist.angular.z = 0

        ## distance to wall from front
        elif min_front < distance_obst:
            if msg_twist.linear.x > 0:
                print("Obstacle from the front \n")
                msg_twist.linear.x = 0

        ## distance to wall from right
        elif min_right < distance_obst:
            if msg_twist.angular.z > 0:
                print("Obstacle from the right \n")
                msg_twist.angular.z = 0

        pub_velocity.publish(msg_twist)

        ## after some time just reset the values
        time.sleep(0.2)
        msg_twist.linear.x = 0
        msg_twist.angular.z = 0
        pub_velocity.publish(msg_twist)

    return 1
