#!/usr/bin/env python
import rospy
import time
import random
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from std_msgs.msg import Int16

ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
ua_flag = 0

def ultrasonic():
    global ua_flag
    rospy.init_node('picar1_ua', anonymous=False)
    ua_pub = rospy.Publisher('picar1_ultrasonic', Int16, queue_size=1)
    while not rospy.is_shutdown():
        distance = ua.get_distance()
        print(distance)
        if distance <= 30:
            ua_flag = 1
        else:
            ua_flag = 0
        ua_pub.publish(ua_flag)

if __name__ == '__main__':
    try:
        ultrasonic()
    except rospy.ROSInterruptException:
        pass
