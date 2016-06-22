from state import State
from power_on_sent_state import PowerOnSent

import struct, socket
import sys

class FsMachineOff(State):
    def blockOnFsEvent(self):
        return False

    def sendUdpPacket(self,msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(msg, ('<broadcast>', 9))
        s.close()

    def sendPowerOn(self,config):
        # Construct a six-byte hardware address
        addr_byte = config.ethernet_address.split(':')
        hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
                              int(addr_byte[1], 16),
                              int(addr_byte[2], 16),
                              int(addr_byte[3], 16),
                              int(addr_byte[4], 16),
                              int(addr_byte[5], 16))

        # Build the Wake-On-LAN "Magic Packet"...

        msg = '\xff' * 6 + hw_addr * 16
        # ...and send it to the broadcast address using UDP
        self.sendUdpPacket(msg)
    
    def fsevent(self,config):
        self.sendPowerOn(config)
        return PowerOnSent()

if __name__ == '__main__':
    global_msg = ''
    real_test = False
    import unittest

    class MockConfig:
        def __init__(self):
            self.ethernet_address = 'd0:50:99:85:0c:46'

    class TestFsMachineOffState(unittest.TestCase):
        def mock_send_function(self,msg):
            global global_msg
            global_msg = msg
        
        def test_sendPowerOn(self):
            #dont send an actual power on, but override so
            #that we can do verification
            real_send_packet = FsMachineOff.sendUdpPacket
            FsMachineOff.sendUdpPacket = self.mock_send_function

            #perform test
            fmo = FsMachineOff()
            returned_state = fmo.fsevent(MockConfig())
            expected_msg = '\xff' * 6 + '\xd0\x50\x99\x85\x0c\x46' * 16
            self.assertTrue( global_msg == expected_msg)
            self.assertTrue( returned_state.__class__.__name__ == 'PowerOnSent' )

            #cleanup
            FsMachineOff.sendUdpPacket = real_send_packet

        def test_sendPowerOnReal(self):
            #only test for real if we supply an argument
            if real_test:
                fmo = FsMachineOff()
                fmo.fsevent(MockConfig())

    if len( sys.argv ) > 1:
        real_test = True
        sys.argv = [sys.argv[0]]
    
    unittest.main()
