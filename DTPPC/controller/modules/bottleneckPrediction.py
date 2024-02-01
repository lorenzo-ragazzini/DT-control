# -*- coding: utf-8 -*-

from time import sleep
from DTPPC.operationalController import ControlModule
from DTPPC.controller.misc import SimulationRequest
from DTPPC.controller.misc import genControlUpdate

class BottleneckPrediction(ControlModule):
    def __init__(self,timeout=60) -> None:
        self.timeout = timeout
    def solve(self,**kwargs):
        sleep(60) # initial delay
        while True:
            DTname = self._controller.dt.new()
            taskResourceInformation = self._controller.systemModel['orders'].to_dict()
            ctrlUpdate = genControlUpdate(self._controller)
            req = SimulationRequest()
            req['output'] = ['U']
            res = self._controller.dt.interface(DTname,taskResourceInformation,ctrlUpdate,req)
            w_dict = dict((key,value['Working']) for key,value in zip(res["U"].keys(), res["U"].values()))
            print(['Bottleneck predicted at station: ' + max(w_dict, key=w_dict.get) + ' --> U = '+str(w_dict[max(w_dict, key=w_dict.get)])+'%'])
            self._controller.dt.clear(DTname)
            sleep(self.timeout)