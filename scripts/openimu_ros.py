#!/usr/bin/env python

import rospy
import sys
import time
import math
import sensor_msgs.msg


#from ..src.aceinna.tools import OpenIMU

try:
    from aceinna.tools import OpenIMU
except:  # pylint: disable=bare-except
    print('load package from local')
    sys.path.append('./src')
    from aceinna.tools import OpenIMU


class OpenIMUros:
    def __init__(self):
        self.openimudev = OpenIMU()
        self.openimudev.startup()

    def close(self):
        self.openimudev.close()

    '''
    def readimu(self, packet_type):
        readback = self.openimudev.getdata(packet_type)
        return readback
    '''

    def readimu(self):
        readback = self.openimudev.getdata('z1')
        return readback

if __name__ == "__main__":
    rospy.init_node("openimu_driver")
    openimu_wrp = OpenIMUros()

    #imuresult = openimu_wrp.readimu('z1')

    rospy.on_shutdown(openimu_wrp.close)
    rospy.loginfo("OpenIMU driver started.")
    rospy.spin()
