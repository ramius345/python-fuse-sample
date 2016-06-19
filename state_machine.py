import time
import threading

class StateMachine(threading.Thread):
    def __init__(self,initialState):
        self.state = initialState
        self.intcount = 0
        self.blockcount = 0
        self.lock = threading.Lock()
        threading.Thread.__init__(self)
        
    def count(self):
        return self.intcount

    def terminate(self):
        self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            time.sleep(1)
            self.intcount += 1
            self.timerevent()

    def fsevent(self):
        '''
        Handle a filesystem event.  These might
        need to be blocked if they are in a transitional state
        instead of an end state.
        '''
        while self.state.blockOnFsEvent():
            self.blockcount += 1
            time.sleep(.1)

        self.lock.acquire()
        self.state = self.state.fsevent(self)
        self.lock.release()
        
    def timerevent(self):
        '''
        Timer events are always handled
        '''
        self.lock.acquire()
        self.state = self.state.fsevent(self)
        self.lock.release()


if __name__ == '__main__':
    import unittest
    class State1:
        def blockOnFsEvent(self):
            return False

        def timerevent(self,machine):
            return State2()

        def fsevent(self,machine):
            return State2()

    class State2:
        def __init__(self):
            self.called = True
            
        def blockOnFsEvent(self):
            value = self.called
            self.called = False
            return value

        def timerevent(self,machine):
            return self

        def fsevent(self,machine):
            return self
        
    class TestStateMachine(unittest.TestCase):
        def test_stateProgression(self):
            sm = StateMachine(State1())
            sm.start()
            time.sleep(2)
            sm.terminate()
            self.assertTrue( sm.state.__class__.__name__ == "State2" )


        def test_blockOnFsEvent(self):
            sm = StateMachine(State1())
            #Don't start the timer thread
            #send an FS event
            sm.fsevent()

            #we should be in state 2
            self.assertTrue( sm.state.__class__.__name__ == "State2" )

            #now send another fs event.  State2 is set up to block once
            #in which case it will sleep then try again and at which
            #point it will tell it that it is no longer blocked and we will exit
            sm.fsevent()

            #now look at the block counter to verify the blocking behavior
            self.assertTrue( sm.blockcount == 1 )
            

    unittest.main()
