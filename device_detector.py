import sys
import time
import struct
try:
    from aceinna.tools import Detector
    #from aceinna.devices.parsers.open_packet_parser import common_continuous_parser
except:  # pylint: disable=bare-except
    print('load package from local')
    sys.path.append('./src')
    from aceinna.tools import Detector
    #from aceinna.devices.parsers.open_packet_parser import common_continuous_parser


def on_find_device(device):
    '''
    callback after find device
    '''
    device.setup(None)

    #tempsteve = device.get_latest() ####error
    #tempsteve = device.data ### doesnt work either
    #tempsteve = 12345
    tempsteve = device.get_device_connection_info()   #src/aceinna/devices/openimu/uart_provider.py
    #tempsteve = device.on_receive_output_packet('z1', 'data')
    print(tempsteve)
    #print(tempsteve[0])
    #print(tempsteve[1])
    print(device)

    '''
    readback = device.read_untils_have_data('z1')
    #print(readback)
    a = (readback[12:16]) #zaccel
    print (a)
    b = struct.unpack('f', bytes(a))[0]
    print(b)
    '''
    print('getting imu data')
    imuresult = get_imudata(device)
    print(imuresult)
    imuresult = get_imudata(device)
    print(imuresult)
    imuresult = get_imudata(device)
    print(imuresult)

    #tempsteve2 = payload_parser(tempsteve, 'z1')
    #tempsteve2 = common_continuous_parser(tempsteve, 'z1')
    #print(tempsteve2)

    #tempsteve = device.read_output()
    #print(tempsteve)
    #tempsteve = device.read_utils_have_data('z1')
    #print(tempsteve)

    '''
    see uart_provider.py added function or try use read_utils_have_data function directly
        def get_latest(self)        #worth trying this out steve
            return self.read_untils_have_data('z1')
    '''
    #tempsteve = device.get_latest()
    #tempsteve = device.get_log_info()
    #print(tempsteve)

  # start log
    #device.start_data_log()  # move this below?
    #device._lock()
    #print('Logging...')
    #time.sleep(2)
    # stop log
    #device.stop_data_log()
    
    device.close()
'''
    device._lock()
    # print('Logging...')
    # time.sleep(10)
    # stop log
    # device.stop_data_log()
    device.close()
'''

def get_imudata(device):
    '''
    get imu data
    '''
    readback = device.read_untils_have_data('z1')
    #print(readback)
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
    #print (zaccelraw)
    #print(zaccel)
    #return zaccel
    imudata =[time_ms, xaccel, yaccel, zaccel, xrate, yrate, zrate, xmag, ymag, zmag]
    return imudata


def simple_start():
    detector = Detector()
    detector.find(on_find_device)


def parameters_start():
    detector = Detector(
        device_type='opemimu',
        com_port='COM3',
        baudrate=115200
    )
    detector.find(on_find_device)

if __name__ == '__main__':
    simple_start()
    #parameters_start()
    
'''
from .tools.bootloader import OpenIMU
def read_output():
    openx = OpenIMU()  
'''   