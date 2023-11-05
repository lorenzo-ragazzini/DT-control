# -*- coding: utf-8 -*-

from operationalController import ControlPolicy
from numpy import inf

class Release(ControlPolicy):
    inputParameters = ['WIP']
    def __init__(self):
        self.WIPlimit = inf
    def solve(self,sequence,WIP):
        dv = [False for i in range(len(sequence))]
        if WIP < self.WIPlimit:
            dv[0] = True
        return {'admission' : dv}