#! /usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
from std_msgs.msg import String

#gets the data from the topic
def callback(data):
    rospy.loginfo(data.data)
    global x, y
    values = data.data.split()
    x = float(values[0])
    y = float(values[1])
    print("x is ", x, "y is ", y)

#tells the node to get info from topic initiated at ui.py
def receive():
    rospy.init_node('snode_automatic')
    rospy.Subscriber('pub_automatic', String, callback)
    rospy.wait_for_message('pub_automatic', String)

#function that sends the goal target for the simulation
def processing(x_desired, y_desired):

    print("going to point x: ",x_desired," y: ",y_desired)

    #initiate simple action client and target instance
    sac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    sac.wait_for_server()
    target = MoveBaseGoal()

    #initiate map, orientation and state the target positon
    target.target_pose.header.frame_id = 'map'
    target.target_pose.pose.orientation.w = 1
    target.target_pose.pose.position.x = x_desired
    target.target_pose.pose.position.y = y_desired

    #send the target coordinates
    sac.send_goal(target)

    #timeout to exclude waiting for too long if target is outside of the arena
    wait = sac.wait_for_result(timeout=rospy.Duration(50.0))

    if not wait:
        print("the point can't be reached!")
        #cancel goal
        sac.cancel_goal()
        return -1
    print("Arrived at destination")
    return 1

if __name__=="__main__":
    receive()
    processing(x,y)
