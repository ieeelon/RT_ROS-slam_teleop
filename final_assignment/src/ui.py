#! /usr/bin/env python

import rospy
from final_assignment.srv import Directions		#service for mode 1
from final_assignment.srv import Input_keyboard	#service for mode 2 and 3
from std_msgs.msg import String, Float32
from semi import ui_semi

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

def automatic():
    automatic_x = 1
    automatic_y = 1
    print("\nYou've chosen automatic control\n")
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
    # aim is for target (if target == 1) then print
    # if target.return_== 1:
    # 	print("target reached successfully!")
    # else:
    # 	print("target not reached")

#call the keyboard service to handle the case
def manual():
    #function to handle mode 2: calls the service to manage the input from keyboard
    #if the user selects mode 2 it will send 1 to the manage_input(request) function in choice2.py
    print("\nYou've chosen manual control\n")
    manualo = 2
    return manualo
    # rospy.wait_for_service('input_key')
    # usrInput = rospy.ServiceProxy('input_key', Input_keyboard)
    # usrInput(1)

def semi():
    #function to handle mode 3: calls the service to manage the input from keyboard
    #if the user selects mode 3 it will send 2 to the manage_input(request) function in choice2.py
    ui_semi()



if __name__=="__main__":

    rospy.init_node('pnode_automatic')
    pub_automatic = rospy.Publisher('pub_automatic', String, queue_size = 10)
    # rospy.init_node('pnode_manual')
    pub_manual = rospy.Publisher('pub_manual', Float32, queue_size = 10)

    flag = 1
    while not rospy.is_shutdown() and flag== 1:

        ui_mode = ui()
        if int(ui_mode) == 1:
            ui_x, ui_y = automatic()
            print("x coordinate is:", ui_x)
            print("y coordinate is:", ui_y)

            target = str(ui_x) +" "+ str(ui_y)
            print(target)
            pub_automatic.publish(target)

        elif int(ui_mode) == 2:
            ui_manual = manual()
            print("Entering the manual mode")
            pub_manual.publish(ui_manual)
            print("SENT DATA: ", ui_manual)

        elif int(ui_mode) == 3:
            # ui_semi = semi()
            # print("Entering assisted driving mode")
            # pub_semi.publish(ui_semi)
            while not ui_semi():
                pass
        elif int(ui_mode) == 4:
            flag = 0
            print("Process shut down")
        else:
            print("error")



    # while(flag):
    #     #loop to print the interface and save the choice in the varible mode
    #
    #     mode = userInterface()
    #
    #     if mode.isnumeric():
    #         mode = int(mode)
    #         if (mode == 1):
    #             choice1()
    #
    #         elif (mode == 2):
    #             choice2()
    #
    #         elif (mode == 3):
    #             choice3()
    #
    #         elif (mode == 0):
    #             flag = 0
    #             print("press ctrl-C to quit")
    #             print()
    #
    #         else:
    #             print("incorrect input!!")
    #     else:
    #         print("input value is not a number!!")
