# -*- coding: utf-8 -*-
from DTPPC.operationalController import ControlModule

class UpdateWIP(ControlModule):
    def run(self,**kwargs):
        self._controller.systemModel["WIP"] -= 1