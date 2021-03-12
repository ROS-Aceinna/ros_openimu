import sys
import time
import struct

#sys.path.append('./src')
from src.aceinna.tools import Detector

class OpenImuDriverROS(object):
    def __init__(self):
        self.detector=Detector()
        self.detector.find(self.on_find_device)
        self.device = None #uartobject
    def on_find_device(self, device):
        '''
        callback after find device
        '''
        device.setup(None)
    def get_imudata(self, device):
        '''
        get imu data
        '''
        readback = device.read_untils_have_data('z1')
            #print(readback)
        xaccelraw = (readback[4:8]) #xaccel
        xaccel = struct.unpack('f', bytes(xaccelraw))[0]
        yaccelraw = (readback[8:12]) #yaccel
        yaccel = struct.unpack('f', bytes(yaccelraw))[0]
        zaccelraw = (readback[12:16]) #zaccel
        zaccel = struct.unpack('f', bytes(zaccelraw))[0]
        xrateraw = (readback[16:20]) #xrate
        xrate = struct.unpack('f', bytes(xrateraw))[0]
        yrateraw = (readback[20:24]) #yrate
        yrate = struct.unpack('f', bytes(yrateraw))[0]
        zrateraw = (readback[24:28]) #zrate
        zrate = struct.unpack('f', bytes(zrateraw))[0]
        #print (zaccelraw)
        #print(zaccel)
        #return zaccel
        imudata =[xaccel, yaccel, zaccel, xrate, yrate, zrate]
        return imudata

if __name__ == "__main__":
    ##rospy.init_node("ros_openimu") # or should it be detector
    openimu = OpenImuDriverROS()
    ##rospy.on_shutdown(openimu.close)
    ##rospy.loginfo("OpenIMU driver is now started.")
    ##rospy.spin()
    openimu.get_imudata()
    print (openimu.get_imudata)
