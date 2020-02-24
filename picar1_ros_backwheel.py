#!/usr/bin/env python
import rospy
import time
import random
from SunFounder_PiCar import back_wheels
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from std_msgs.msg import String
from std_msgs.msg import Int16
from std_msgs.msg import Int32MultiArray


bw = back_wheels.Back_Wheels(db='config')
bw.ready()
forward_speed = 60
picar_id = 1 #change this for each car
first_flag = True
ua_flag = 0

def uaflag_cb(ultrasonic_flag):
    global ua_flag
    if ultrasonic_flag.data == 1:
        ua_flag = 1
    else:
        ua_flag = 0

def flag_cb(flags):
    global first_flag
    if ua_flag == 1:
        bw.stop()
        time.sleep(0.5)
    else:
        if first_flag:
                if flags.data[picar_id-1] == 1:
                    bw.stop()
                    first_flag = False
                    time.sleep(random.randint(1,10))
                else:
                    bw.speed = forward_speed
                    bw.forward()
        else:
                if flags.data[picar_id-1] == 0:
                    first_flag = True
                else:
                    bw.speed = forward_speed
                    bw.forward()

def backwheels():
    rospy.init_node('picar1_backwheels', anonymous=False)
    uaflag_sub = rospy.Subscriber("picar1_ultrasonic", Int16, uaflag_cb)
    picarflags_sub = rospy.Subscriber("picar_flags", Int32MultiArray, flag_cb)
    rospy.spin()

def stop():
    bw.stop()

if __name__ == '__main__':
    try:
	    backwheels()
    except KeyboardInterrupt:
        print "KeyboardInterrupt, stop"
        stop()
    except rospy.ROSInterruptException:
	    stop()
	    pass
    finally:
	    stop()
