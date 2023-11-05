# -*- coding: utf-8 -*-
from operationalController import ControlPolicy
from numpy import inf

class Release(ControlPolicy):
    inputParameters = ['WIP']
    def __init__(self,WIPlimit=inf):
        self.WIPlimit = WIPlimit
    def solve(self,WIP):
        sequence = self._controller.decisionVariables['sequence']
        admission = self._controller.decisionVariables['admission']
        if WIP < self.WIPlimit:
            admission[0] = True
        return {'admission' : admission}