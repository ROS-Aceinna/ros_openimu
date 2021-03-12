#!/usr/bin/env python

import sys
#import time # not used - delete
import struct
##import rospy
'''
##sys.path.append("..") #didnt work
print ("printing")
print (sys.path)
print ('printed')
sys.path.append('./src')
print ("printing")
print (sys.path)
print ('printed')
'''
#from src.aceinna.tools import Detector
from src.aceinna.devices.openimu.uart_provider import Provider
#.openimu.uart_provider import Provider?

class OpenImuDriverROS:
    def __init__(self):
        self.openimudriver = Provider(communicator='uart')   ##### maybe????
        self.readback = []
        self.imudata = []
        self.openimudriver.setup(self, None) #check this options/or replace with None
    def close(self):
        self.openimudriver.close(self)
    def get_imudata(self):
        self.readback = self.openimudriver.read_untils_have_data(self, 'z1')
        self.decode_imudata()
    def decode_imudata(self):
        xaccelraw = (self.readback[4:8]) #xaccel
        xaccel = struct.unpack('f', bytes(xaccelraw))[0]
        yaccelraw = (self.readback[8:12]) #yaccel
        yaccel = struct.unpack('f', bytes(yaccelraw))[0]
        zaccelraw = (self.readback[12:16]) #zaccel
        zaccel = struct.unpack('f', bytes(zaccelraw))[0]
        xrateraw = (self.readback[16:20]) #xrate
        xrate = struct.unpack('f', bytes(xrateraw))[0]
        yrateraw = (self.readback[20:24]) #yrate
        yrate = struct.unpack('f', bytes(yrateraw))[0]
        zrateraw = (self.readback[24:28]) #zrate
        zrate = struct.unpack('f', bytes(zrateraw))[0]
        self.imudata = [xaccel, yaccel, zaccel, xrate, yrate, zrate]
    '''
    def set_config(self):
        self.openimudriver.Provider.set_param(self, params, *args)
        self.openimudriver.Provider.set_params(self, params, *args)
    '''
'''
#from cli
        self.device_provider.set_param({
            'paramId': select_param['paramId'],
            'value': self.input_string[2]
        })


'''



'''
class OpenImuDriverROS:
    def __init__(self):
        self.openimudriver = Detector()
        self.openimudriver.find(on_find_device)
    def close(self):
        self.openimudriver.communicator.close() #correct???
    #def on_find_device(device): #device or not - something else
    #   device.setup(None)
    def on_find_device(self):
        self.openimudriver.communicator.get_device_connection_info()
        self.openimudriver.communicator.
'''
       
'''
def on_find_device(device): #device or not - something else
    device.setup(None)
    connectioninfo = device.get_device_connection_info()   #src/aceinna/devices/openimu/uart_provider.py
    print(connectioninfo)
'''

if __name__ == "__main__":
    ##rospy.init_node("ros_openimu") # or should it be detector
    openimu = OpenImuDriverROS()
    ##rospy.on_shutdown(openimu.close)
    ##rospy.loginfo("OpenIMU driver is now started.")
    ##rospy.spin()
    openimu.get_imudata()
    print (openimu.imudata)
