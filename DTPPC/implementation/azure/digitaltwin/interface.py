# from DTPPC.implementation.communication.message import MessengerOnly

class DTIFront:
    def __getattr__(self):
        pass
    def dummy(self):
        pass

class DTIBack:
    pass

if __name__ == '__main__':
    dt = DTIFront()
    dt.Dummy