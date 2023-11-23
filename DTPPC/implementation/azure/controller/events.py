import json
import pandas as pd
from time import sleep
import asyncio 
from DTPPC.implementation.communication.message import MessengerOnly

class EventListener:
    def __init__(self,queue_name,timeout=1):
        self.log = list()
        self.timeout = timeout
        self.ctrl = None
    def listen(self):
        while True:
            events = self.msg.receive()
            for event in events:
                if event not in self.log:
                    self.log.append(event)
                    self.ctrl.send(event)
            sleep(self.timeout)

class EventListenerMsg:
    def __init__(self,queue_name,timeout=1):
        self.msg = MessengerOnly(queue_name)
        self.log = list()
        self.timeout = timeout
        self.ctrl = None
    def listen(self):
        events = self.msg.receive()
        for event in events:
            if event not in self.log:
                self.log.append(event)
                self.ctrl.send(event.content)
    async def async_listen(self):
        while True:
            events = self.msg.receive()
            for event in events:
                if event not in self.log:
                    print(event)
                    self.log.append(event)
                    asyncio.run(self.ctrl.send(event.content))
            await asyncio.sleep(self.timeout)