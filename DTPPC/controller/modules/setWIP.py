# -*- coding: utf-8 -*-
from time import sleep
from DTPPC.operationalController import ControlModule
from DTPPC.controller.misc import SimulationRequest
import pandas as pd

class SetWIP(ControlModule):
    def __init__(self,timeout=600) -> None:
        self.timeout = timeout
    def solve(self,**kwargs):
        while True:
            sleep(self.timeout)
            r = list()
            for WIPlevel in range(1,10):
                ctrlUpdate = {"executeSchedule":{"sequence":self._controller.decisionVariables['sequence']}}
                req = SimulationRequest()
                res = self._controller.dt.interface(None,ctrlUpdate,req)
                r.append([WIPlevel,res['TH'],res["st"]])
            r = pd.DataFrame(r,columns=["WIP","TH","LT"]).set_index(['WIP'])
