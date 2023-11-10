# -*- coding: utf-8 -*-
from operationalController import ControlModule

class UpdateWIP(ControlModule):
    def run(self,**kwargs):
        self._controller.systemModel["WIP"] -= 1