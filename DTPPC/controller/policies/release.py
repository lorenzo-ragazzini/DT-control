# -*- coding: utf-8 -*-
from DTPPC.operationalController import ControlPolicy
from numpy import inf

class Release(ControlPolicy):
    inputParameters = ['WIP']
    def __init__(self,WIPlimit=inf):
        self.WIPlimit = WIPlimit
    def solve(self,**kwargs):
        WIP=kwargs['input']['WIP']
        sequence = self._controller.decisionVariables['sequence']
        admission = self._controller.decisionVariables['admission']
        if WIP < self.WIPlimit & len(sequence)>0:
            admission[sequence[0]] = True
            self._controller.systemModel['WIP'] += 1
        return {'admission' : admission}
