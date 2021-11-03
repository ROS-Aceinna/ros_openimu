import struct
from ..models.args import DetectorArgs
from ..framework.communicator import CommunicatorFactory
from ..devices.openimu.uart_provider import Provider

INITIAL = 0


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
        # self.imudevice.setup(None)

    def startup(self):
        self.find(self.onfinddev)

    def close(self):
        self.communicator.close()

    def getdata(self, datatype):
        readback = self.imudevice.read_untils_have_data(datatype)
        if datatype == ('z1'):
            timeraw = (readback[0:4])  # time in ms
            time_ms = struct.unpack('I', bytes(timeraw))[0]
            xaccelraw = (readback[4:8])  # xaccel
            xaccel = struct.unpack('f', bytes(xaccelraw))[0]
            yaccelraw = (readback[8:12])  # yaccel
            yaccel = struct.unpack('f', bytes(yaccelraw))[0]
            zaccelraw = (readback[12:16])  # zaccel
            zaccel = struct.unpack('f', bytes(zaccelraw))[0]
            xrateraw = (readback[16:20])  # xrate
            xrate = struct.unpack('f', bytes(xrateraw))[0]
            yrateraw = (readback[20:24])  # yrate
            yrate = struct.unpack('f', bytes(yrateraw))[0]
            zrateraw = (readback[24:28])  # zrate
            zrate = struct.unpack('f', bytes(zrateraw))[0]
            xmagraw = (readback[28:32])  # xrate
            xmag = struct.unpack('f', bytes(xmagraw))[0]
            ymagraw = (readback[32:36])  # yrate
            ymag = struct.unpack('f', bytes(ymagraw))[0]
            zmagraw = (readback[36:40])  # zrate
            zmag = struct.unpack('f', bytes(zmagraw))[0]
            imudata = [time_ms, xaccel, yaccel, zaccel,
                       xrate, yrate, zrate, xmag, ymag, zmag]

# a1 a2 packets in development
        if datatype == ('a1'):
            time_ms = struct.unpack('I', bytes(readback[0:4]))[0]  # unin32
            time_s = struct.unpack('d', bytes(readback[4:12]))[0]  # double
            roll = struct.unpack('f', bytes(readback[12:16]))[0]
            pitch = struct.unpack('f', bytes(readback[16:20]))[0]
            xrate = struct.unpack('f', bytes(readback[20:24]))[0]
            yrate = struct.unpack('f', bytes(readback[24:28]))[0]
            zrate = struct.unpack('f', bytes(readback[28:32]))[0]
            xaccel = struct.unpack('f', bytes(readback[32:36]))[0]
            yaccel = struct.unpack('f', bytes(readback[36:40]))[0]
            zaccel = struct.unpack('f', bytes(readback[40:44]))[0]
            opMode = struct.unpack('B', bytes(readback[44:45]))[0]  # uint8
            linAccSw = struct.unpack('B', bytes(readback[45:46]))[0]  # uint8
            turnSw = struct.unpack('B', bytes(readback[46:47]))[0]  # uint8
            imudata = [time_ms, time_s, roll, pitch, xrate, yrate,
                       zrate, xaccel, yaccel, zaccel, opMode, linAccSw, turnSw]

        if datatype == ('a2'):
            imudata = {'time_ms': INITIAL, 'time_s': INITIAL,
                       'roll': INITIAL, 'pitch': INITIAL, 'heading': INITIAL,
                       'xrate': INITIAL, 'yrate': INITIAL, 'zrate':INITIAL,
                       'xaccel': INITIAL, 'yaccel': INITIAL, 'zaccel': INITIAL,
                       'errorflag'=INITIAL}
            try:
                time_ms = struct.unpack('I', bytes(readback[0:4]))[0]  # unin32
                time_s = struct.unpack('d', bytes(readback[4:12]))[0]  # double
                roll = struct.unpack('f', bytes(readback[12:16]))[0]
                # Change degrees limit angles from -pi to pi
                pitch = struct.unpack('f', bytes(readback[16:20]))[0]
                heading = struct.unpack('f', bytes(readback[20:24]))[0]
                xrate = struct.unpack('f', bytes(readback[24:28]))[0]
                yrate = struct.unpack('f', bytes(readback[28:32]))[0]
                zrate = struct.unpack('f', bytes(readback[32:36]))[0]
                xaccel = struct.unpack('f', bytes(readback[36:40]))[0]
                yaccel = struct.unpack('f', bytes(readback[40:44]))[0]
                zaccel = struct.unpack('f', bytes(readback[44:48]))[0]
                errorflag = False
                #zaccel = struct.unpack('f', bytes(readback[48:52]))[0]
                # Create a dictionairy since lookup is faster and code is cleaner

                imudata = [time_ms, time_s, roll, pitch, heading, xrate,
                           yrate, zrate, xaccel, yaccel, zaccel, errorflag]

            except Exception:
                errorflag = True
            return imudata

# set values in development
    def setpacketrate(self, packetrate):
        # 200, 100, 50, 20, 10, 5, 2, 0
        self.imudevice.set_param(['rate', packetrate])

    def setpackettype(self, packettype):
        self.imudevice.set_param(['type', packettype])  # 'z1", "a1", "a2"
