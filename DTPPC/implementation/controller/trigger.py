from typing import Any
import asyncio
import pandas as pd
from DTPPC.implementation.controller.controller import SmartController
from DTPPC.implementation.local.events import EventCreator
from multiprocessing import Process
from DTPPC.implementation.local.planned_orders import planned_orders_simplified


class Trigger(EventCreator):
    def __init__(self,input_file,controller:SmartController=None):
        self.controller = controller
        super().__init__(input_file,output_file=None)
    def process(self):
        events = self.events()
        for event in events:
            print(pd.Timestamp.now(),event)
            # asyncio.run(self.controller.send_async(event))
            self.controller.systemModel['orders'] = planned_orders_simplified('MESdata.xlsx')
            p=Process(target=self.controller.send,args=(event,))
            p.start()
            p.join()