import struct
from ..models.args import DetectorArgs
from ..framework.communicator import CommunicatorFactory
from ..devices.openimu.uart_provider import Provider

class OpenIMU(object):
    '''
    IMU Device Detector
    '''
    def __init__(self, **kwargs):
        self.communication = 'uart'
        self.communicator = None
        self._build_options(**kwargs)
        self.imudevice = None

    def find(self, callback):
        '''find if there is a connected device'''
        print('start to find device')
        if self.communicator is None:
            self.communicator = CommunicatorFactory.create(
                self.communication, self.options)

        self.communicator.find_device(callback)

    def _build_options(self, **kwargs):
        self.options = DetectorArgs(**kwargs)

    def onfinddev(self, device):
        self.imudevice = device
        #self.imudevice.setup(None)
    
    def startup(self):
        self.find(self.onfinddev)

    def close(self):
        self.communicator.close()

    def getdata(self, datatype):
        readback = self.imudevice.read_untils_have_data(datatype)
        if datatype == ('z1'):
            timeraw = (readback[0:4]) #time in ms
            time_ms = struct.unpack('I', bytes(timeraw))[0]
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
            xmagraw = (readback[16:20]) #xrate
            xmag = struct.unpack('f', bytes(xmagraw))[0]
            ymagraw = (readback[20:24]) #yrate
            ymag = struct.unpack('f', bytes(ymagraw))[0]
            zmagraw = (readback[24:28]) #zrate
            zmag = struct.unpack('f', bytes(zmagraw))[0]
            imudata =[time_ms, xaccel, yaccel, zaccel, xrate, yrate, zrate, xmag, ymag, zmag]
        return imudata
