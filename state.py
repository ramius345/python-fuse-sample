class State:
    #By default, if not defined, a state should block
    #filesystem events
    def blockOnFsEvent(self):
        return True

    #Default handler for filesystem events
    def fsevent(self,machine):
        print "fsevent called an not overloaded in ",self.__class__.__name__
        return self

    #Handler for timer events
    def timerevent(self,machine):
        print "timer event called in ",self.__class__.__name__
        return self
