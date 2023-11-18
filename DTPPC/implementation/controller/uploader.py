from typing import Any
from DTPPC.implementation.communication.message import MessengerOnly
import json

local_path = ''
filename = 'dv.json'

class SendDV():
    def __init__(self,queue_name,input_filename='dv.json'):
        self.input_filename = input_filename
        self.msg = MessengerOnly(queue_name)
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.run()
    def run(self,dv=None):
        if not dv:
            with open(self.input_filename) as f:
                dv = json.load(f)
        return self.msg.send(dv)