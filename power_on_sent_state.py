from state import State

#TODO remove
class MachineOn:
    pass

class Failed:
    pass

class PowerOnSent(State):
    def __init__(self):
        self.pingcount = 0

    def sendping(self):
        pass #TODO true on success ping
        
    def timerevent(self,machine):
        if self.pingcount > 3:
            return Failed("Ping could not be established!")
        elif self.sendping() == "Success":
            return MachineOn()
        else:
            return self
