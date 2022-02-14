#! /usr/bin/env python

import rospy
from final_assignment.srv import Directions
import actionlib
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
from std_msgs.msg import String


def callback(data):
    rospy.loginfo(data.data)
    global x, y
    values = data.data.split()
    x = float(values[0])
    y = float(values[1])
    print("x is ", x, "y is ", y)

def receive():
    rospy.init_node('snode_automatic')
    rospy.Subscriber('pub_automatic', String, callback)
    rospy.wait_for_message('pub_automatic', String)

def processing(x_desired, y_desired):
    #function to manage the user choice of mode 1. Sets the target and waits for the result

    print("going to point x: ",x_desired," y: ",y_desired)

    #starting the action and wait for the server
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    target = MoveBaseGoal()

    #set the target's parameters
    target.target_pose.header.frame_id = 'map'
    target.target_pose.pose.orientation.w = 1
    target.target_pose.pose.position.x = x_desired
    target.target_pose.pose.position.y = y_desired

    #send the target
    client.send_goal(target)
    #timeout to prevent infinite waiting
    wait = client.wait_for_result(timeout=rospy.Duration(50.0))

    if not wait:
        #target not reached
        print("the point can't be reached!")
        client.cancel_goal()
        return -1
    #target reached
    print("Arrived at destination")
    return 1

# def directions_server():
#     #node description
#
#     print("automatic motion node, DO NOT CLOSE THE TERMINAL")
#     #initialize the node
#     rospy.init_node('directions_controller')
#
#     #call the service handler
#     s = rospy.Service('directions', Directions, manage_input)
#     print("service ready")
#     rospy.spin()

if __name__=="__main__":
    # directions_server()
    receive()
    processing(x,y)
