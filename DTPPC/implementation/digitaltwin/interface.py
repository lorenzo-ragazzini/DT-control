import numpy as np

class Interface:
    def __init__(self):
        pass
    def identify(self)->int:
        l = 'abcdefghijklmnopqrstuvwxyz'
    def synchronize(self):
        pass
    def update(self):
        pass
    def simulate(self):
        pass
    def interface(self):
        self.synchronize(taskResourceInformation)
        self.update(controlUpdate)
        return self.simulate(request)

def send():
    pass
    # receive inputs
    # upload inputs
    # wait for results
    # download results
    # return results

def receive():
    pass
    #download inputs
    #save files
    #execute simulation
    #upload results

if __name__ == '__main__':
    import random