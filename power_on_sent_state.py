from state import State
from failed_state import Failed
import os

class MachineOn:
    pass

class PowerOnSent(State):
    MAXPING=3
    def __init__(self):
        self.pingcount = 0

    def sendping(self,config):
        response = os.system("ping -c 1 " + config.hostname)
        if response == PowerOnSent.MAXPING:
            return "Success"
        else:
            return "Failure"
        
    def timerevent(self,config):
        self.pingcount += 1
        if self.pingcount > 3:
            return Failed("Ping could not be established!")
        elif self.sendping(config) == "Success":
            return MachineOn()
        else:
            return self

if __name__ == '__main__':
    real_test = False
    import unittest
    import sys
    
    class MockConfig:
        def __init__(self):
            self.hostname = 'greengrape'

    class TestPowerOnSent(unittest.TestCase):
        def mock_sendping_success(self,config):
            return "Success"
        
        def test_sendOnePingSuccess(self):
            #Overload the sending of the ping to test fail procedure
            old_sendping = PowerOnSent.sendping
            PowerOnSent.sendping = self.mock_sendping_success
            
            pos = PowerOnSent()
            new_state = pos.timerevent(MockConfig())

            #should have sent one ping
            self.assertTrue( pos.pingcount == 1 )

            #the current state should be MachineOn
            self.assertTrue( new_state.__class__.__name__ == 'MachineOn' )

    if len( sys.argv ) > 1:
        real_test = True
        sys.argv = [sys.argv[0]]
    
    unittest.main()

