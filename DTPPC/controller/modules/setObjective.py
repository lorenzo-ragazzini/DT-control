# -*- coding: utf-8 -*-
from time import sleep
from DTPPC.operationalController import ControlModule
from DTPPC.controller.misc import genControlUpdate, SimulationRequest

class SetObjective(ControlModule):
    def __init__(self,timeout=180) -> None:
        self.timeout = timeout
    def solve(self,**kwargs):
        while True:
            sleep(self.timeout)
            DTname = self._controller.dt.new()
            taskResourceInformation = self._controller.systemModel['orders'].to_dict()
            ctrlUpdate = genControlUpdate(self._controller)
            req = SimulationRequest()
            req['output'] = ['th','st']
            res = self._controller.dt.interface(DTname,taskResourceInformation,ctrlUpdate,req)
            self._controller.dt.clear(DTname)
            print("Optimization objective updated!")
            