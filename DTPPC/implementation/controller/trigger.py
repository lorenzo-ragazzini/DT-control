from typing import Any
import asyncio
import pandas as pd
from DTPPC.implementation.controller.controller import SmartController
from DTPPC.implementation.local.events import EventCreator


class Trigger(EventCreator):
    def __init__(self,input_file,controller:SmartController=None):
        self.controller = controller
        super().__init__(input_file,output_file=None)
    def process(self):
        events = self.events()
        for event in events:
            print(pd.Timestamp.now(),event)
            # asyncio.run(self.controller.send_async(event))
            asyncio.create_task(self.controller.send_async(event))