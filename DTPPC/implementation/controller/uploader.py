from typing import Any
from DTPPC.implementation.communication.message import MessengerOnly
import json

local_path = ''
filename = 'dv.json'

class SendDV():
    def __init__(self,queue_name,input_filename='dv.json'):
        self.input_filename = input_filename
        self.actuator = None
    def run(self,dvs=None):
        if not dvs:
            with open(self.input_filename) as f:
                dvs = json.load(f)
        return self.actuator.run(dvs)

class SendDVmsg():
    def __init__(self,queue_name,input_filename='dv.json'):
        self.input_filename = input_filename
        self.msg = MessengerOnly(queue_name)
    def run(self,dvs=None):
        if not dvs:
            with open(self.input_filename) as f:
                dvs = json.load(f)
        return self.msg.send(dvs)