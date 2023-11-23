import asyncio
import json
from DTPPC.implementation.azure.communication.message import MessengerOnly
from DTPPC.implementation.local.actuator import Actuator


class DownloadDV:
    def __init__(self,queue_name) -> None:
        self.msg = MessengerOnly(queue_name)
        self.log = list()
        self.actuator : Actuator = None
    def listen(self):
        list_dvs = self.msg.receive()
        for dvs in list_dvs:
            print(dvs)
            self.log.append(dvs)
            self.actuator.run(dvs)
            with open('dv.json','w') as f:
                json.dump(dvs,f) 
    async def async_listen(self):
        while True:
            self.listen()
            await asyncio.sleep(self.timeout)