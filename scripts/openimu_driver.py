#!/usr/bin/env python3

import rospy
import sys
import math
from time import time
from sensor_msgs.msg import Imu, MagneticField
from tf.transformations import quaternion_from_euler

# Configure driver to use enu 
ENU = True
PACKAGETYPE = 'a2'

try:
    from ros_openimu.src.aceinna.tools import OpenIMU
except:  # pylint: disable=bare-except
    temp = (sys.path[0])
    temp2 = temp[0:(len(temp)-7)]
    sys.path.append(temp2 + 'src')
    #sys.path.append('./src')
    from aceinna.tools import OpenIMU


class OpenIMUros:
    def __init__(self):
        self.openimudev = OpenIMU()
        self.openimudev.startup()
        self.use_ENU = ENU

    def close(self):
        self.openimudev.close()

    '''
    def readimu(self, packet_type):
        readback = self.openimudev.getdata(packet_type)
        return readback
    '''

    def readimu(self):
        readback = self.openimudev.getdata(PACKAGETYPE)
        return readback


    def dataToMsg(self, readback, use_enu, pub_imu, seq, imu_msg, frame_id):
        imu_msg.header.stamp = rospy.Time.now()
        imu_msg.header.frame_id = frame_id
        imu_msg.header.seq = seq
        '''
        Convert values to be compliant with REP-103 
        and REP-105
        '''
        if(readback['errorflag'] == False):
            if(use_enu):
                if readback['roll'] > 0.0:
                    readback['roll'] = (readback['roll'] - 180.0) * convert_rads

                else:
                    readback['roll'] = (readback['roll'] + 180.0) * convert_rads

                readback['pitch'] = readback['pitch'] * -1 * convert_rads

                readback['heading'] = readback['heading'] * -1 * convert_rads

            imu_msg.orientation_covariance[0] = 0.025
            imu_msg.orientation_covariance[3] = 0.025
            imu_msg.orientation_covariance[6] = 0.025
            
            orientation_quat = quaternion_from_euler(readback['roll'], readback['pitch'], readback['heading'])
            imu_msg.orientation.x = orientation_quat[0]
            imu_msg.orientation.y = orientation_quat[1]
            imu_msg.orientation.z = orientation_quat[2]
            imu_msg.orientation.w = orientation_quat[3] 
            imu_msg.linear_acceleration.x = readback['xaccel']
            imu_msg.linear_acceleration.y = readback['yaccel']
            imu_msg.linear_acceleration.z = readback['zaccel']
            imu_msg.linear_acceleration_covariance[0] = 0.002
            imu_msg.linear_acceleration_covariance[3] = 0.002
            imu_msg.linear_acceleration_covariance[6] = 0.002
            imu_msg.angular_velocity.x = readback['xrate'] * convert_rads
            imu_msg.angular_velocity.y = readback['yrate'] * convert_rads
            imu_msg.angular_velocity.z = readback['zrate'] * convert_rads
            imu_msg.angular_velocity_covariance[0] = -1
            pub_imu.publish(imu_msg)
            seq = seq + 1

    def dataToMsgRaw(self, readback, pub_imu, seq, imu_msg, frame_id):
        imu_msg.header.stamp = rospy.Time.now()
        imu_msg.header.frame_id = frame_id
        imu_msg.header.seq = seq
        imu_msg.orientation_covariance[0] = -1
        imu_msg.linear_acceleration.x = readback[1]
        imu_msg.linear_acceleration.y = readback[2]
        imu_msg.linear_acceleration.z = readback[3]
        imu_msg.linear_acceleration_covariance[0] = -1
        imu_msg.angular_velocity.x = readback[4] * convert_rads
        imu_msg.angular_velocity.y = readback[5] * convert_rads
        imu_msg.angular_velocity.z = readback[6] * convert_rads
        imu_msg.angular_velocity_covariance[0] = -1
        pub_imu.publish(imu_msg)

        # Publish magnetometer data - convert Gauss to Tesla
        mag_msg.header.stamp = imu_msg.header.stamp
        mag_msg.header.frame_id = frame_id
        mag_msg.header.seq = seq
        mag_msg.magnetic_field.x = readback[7] * convert_tesla
        mag_msg.magnetic_field.y = readback[8] * convert_tesla
        mag_msg.magnetic_field.z = readback[9] * convert_tesla
        mag_msg.magnetic_field_covariance = [0,0,0,0,0,0,0,0,0]
        pub_mag.publish(mag_msg)

        seq = seq + 1

if __name__ == "__main__":
    rospy.init_node("openimu_driver")

    pub_imu = rospy.Publisher('imu_acc_ar', Imu, queue_size=1)
    pub_mag = rospy.Publisher('imu_mag', MagneticField, queue_size=1)

    imu_msg = Imu()             # IMU data
    mag_msg = MagneticField()   # Magnetometer data
    
    rate = rospy.Rate(100)   # 10Hz
    seq = 0
    frame_id = 'OpenIMU'
    convert_rads = math.pi /180
    convert_tesla = 1/10000

    openimu_wrp = OpenIMUros()
    rospy.loginfo("OpenIMU driver initialized.")


    while not rospy.is_shutdown():
        #read the data - call the get imu measurement data
        readback = openimu_wrp.readimu()
        #publish the data m/s^2 and convert deg/s to rad/s
        imu_msg.header.stamp = rospy.Time.now()
        imu_msg.header.frame_id = frame_id
        imu_msg.header.seq = seq
        # Dependening on package from imu read data with appropriate method 
        if(PACKAGETYPE == 'a2'):
            openimu_wrp.dataToMsg(readback, ENU, pub_imu, seq, imu_msg, frame_id)
        
        else:
            openimu_wrp.dataToMsgRaw(readback, pub_imu, seq, imu_msg, frame_id)


        rate.sleep()
    openimu_wrp.close()         # exit



