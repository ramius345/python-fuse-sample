from state import State

class Failed(State):
    def __init__(self,reason):
        print "Entering failed state for reason:\n"
        print reason,"\n"

