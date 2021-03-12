import sys
import time
import struct

try:
    from aceinna.framework.communicator import Communicator
    from aceinna.framework.communicator import CommunicatorFactory
except:
    sys.path.append('./src')
    from aceinna.framework.communicator import Communicator
    from aceinna.framework.communicator import CommunicatorFactory
try:
    from aceinna.devices.openimu.uart_provider import Provider
except:  # pylint: disable=bare-except
    print('load package from local')
    sys.path.append('./src')
    from aceinna.devices.openimu.uart_provider import Provider as OpenIMUProvider
    

def on_find_device(device):
    print(device)

def simple_start():
    #detector = Provider()
    options = {             #aceinna.models.args.py - not right?
        'device_type': 'auto',
        'baudrate': 'auto',
        'com_port': 'auto'
    }
   
    detector = Provider(CommunicatorFactory.create('uart', options)) #see cli.py
    #detector.communicator.find_device(on_find_device)
    #print(detector.get_device_connection_info())
    #detector.on_receive_output_packet('z1', data)
    #detector.read_untils_have_data('z1', 200, 20)
  

if __name__ == '__main__':
    simple_start()