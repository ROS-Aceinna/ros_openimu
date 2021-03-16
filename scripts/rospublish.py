#!/usr/bin/env python

#import serial
import rospy
import sys
#import struct as st
#import binascii
import math

from time import time
from sensor_msgs.msg import Imu, MagneticField

#from tf.transformations import quaternion_from_euler
#from dynamic_reconfigure.server import Server
#from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue

imu_msg = Imu()             # Raw IMU data
mag_msg = MagneticField()       # Magnetometer data

# Main function
if __name__ == '__main__':
    rospy.init_node("rospublish")       #name of this file

    # Sensor measurements publishers
    #pub_data = rospy.Publisher('imu/data', Imu, queue_size=1)
    pub_imu = rospy.Publisher('imu_acc_ar', Imu, queue_size=1)
    pub_mag = rospy.Publisher('imu_mag', MagneticField, queue_size=1)

    # initialize - call the setup function
    rospy.loginfo("Aceinna IMU is connected.")


    rate = rospy.Rate(10)   # 10Hz
    seq = 0
    frame_id = 'OpenIMU'

    convert_rads = math.pi *2
    convert_gauss = 10000

    while not rospy.is_shutdown():
        #read the data - call the get imu measurement data
        readback = []
        #publish the data m/s^2 and convert deg/s to rad/s
        imu_msg.header.stamp = rospy.Time.now()
        imu_msg.header.frame_id = frame_id
        imu_msg.header.seq = seq
        imu_msg.orientation_covariance[0] = -1
        imu_msg.linear_acceleration.x = float(readback[0])
        imu_msg.linear_acceleration.y = float(readback[1])
        imu_msg.linear_acceleration.z = float(readback[2])
        imu_msg.linear_acceleration_covariance[0] = -1
        imu_msg.angular_velocity.x = float(readback[3]) / convert_rads
        imu_msg.angular_velocity.y = float(readback[4]) / convert_rads
        imu_msg.angular_velocity.z = float(readback[5]) / convert_rads
        imu_msg.angular_velocity_covariance[0] = -1
        pub_imu.publish(imu_msg)

        # Publish magnetometer data - convert Gauss to Tesla
        mag_msg.header.stamp = imu_msg.header.stamp
        mag_msg.header.frame_id = frame_id
        mag_msg.header.seq = seq
        mag_msg.magnetic_field.x = float(readback[6]) / convert_gauss
        mag_msg.magnetic_field.y = float(readback[7]) / convert_gauss
        mag_msg.magnetic_field.z = float(readback[8]) / convert_gauss
        mag_msg.magnetic_field_covariance = 0
        pub_mag.publish(mag_msg)

        seq = seq + 1
        rate.sleep()
    ser.close()         # exit this stuff



'''
add file to scripts folder and make executable
$ chmod +x rospublish.py



Add the following to your CMakeLists.txt. This makes sure the python script gets installed properly, and uses the right python interpreter.

catkin_install_python(PROGRAMS scripts/rospublish.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)



Then Go to your catkin workspace and run catkin_make
$ cd ~/catkin_ws
$ catkin_make


Running the Publisher
Make sure that a roscore is up and running:
$ roscore

# In your catkin workspace
$ cd ~/catkin_ws
$ source ./devel/setup.bash

$ rosrun locationofdriver rospublish.py   (Python) 



...