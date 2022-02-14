#! /usr/bin/env python

import rospy
from std_msgs.msg import String, Float32
from semi import ui_semi

#this function is a welcome message and user input is taken
def ui():
    print("\nChoose the modality for the control:\n")
    print("Press '1' to have automatic control\n")
    print("Press '2' to have manual control\n")
    print("Press '3' to have manual control with obstacle avoidance\n")
    print("Press '4' to quit")
    ui_loop = 1
    while (ui_loop == 1):
        try:
            ui_mode = int(input("\nYour input: "))
            ui_loop = 0
            break
        except ValueError:
            print("ERROR")
    return ui_mode

#this is command sequence for the automatic MODE
#acivates when user input is 1
def automatic():
    automatic_x = 1
    automatic_y = 1
    print("\nYou've chosen automatic control\n")

    #take the float values for the required coordinates
    #throws exceptions if wrong input is fed
    while(automatic_x == 1):
        print("Please enter the target coordinate x: ")
        try:
            ui_x = float(input())
            automatic_x = 0
            break
        except ValueError:
            print("\n!Use numeric input!\n")

    while(automatic_y == 1):
        print("Please enter the target coordinate y: ")
        try:
            ui_y = float(input())
            automatic_y = 0
            break
        except ValueError:
            print("\n!Use numeric input!\n")

    return ui_x, ui_y

#control sequence for the manual control MODE
#output activates the subscriber in manual.py
def manual():
    print("\nYou've chosen manual control\n")
    manualo = 2
    return manualo
#control sequence for the mode with collision avoidance
#subscriber is in the semi.py
def semi():
    ui_semi()



if __name__=="__main__":

    #initialize node and publishers
    rospy.init_node('pnode_automatic')
    pub_automatic = rospy.Publisher('pub_automatic', String, queue_size = 10)
    pub_manual = rospy.Publisher('pub_manual', Float32, queue_size = 10)

    #this is used to run code again if the wrong input has been fed
    #allows while loop to run
    marker = 1
    while not rospy.is_shutdown() and marker== 1:

        ui_mode = ui()
        if int(ui_mode) == 1:
            ui_x, ui_y = automatic()
            print("x coordinate is:", ui_x)
            print("y coordinate is:", ui_y)

            target = str(ui_x) +" "+ str(ui_y)
            print(target)

            #send goal target to automatic control sequence using string in form [x y]
            pub_automatic.publish(target)

        elif int(ui_mode) == 2:
            ui_manual = manual()
            print("Entering the manual mode")

            #allows control sequence of manual control to be executed by sending command
            pub_manual.publish(ui_manual)
            print("SENT DATA: ", ui_manual)

        elif int(ui_mode) == 3:
            #exectutes the control sequence of collision avoidance unless it's deactivated on the semi.py
            while not ui_semi():
                pass
        elif int(ui_mode) == 4:
            marker = 0
            print("Process shut down")
        else:
            print("error")
