# -*- coding: utf-8 -*-

from operationalController import ControlPolicy
from numpy import inf

class Release(ControlPolicy):
    inputParameters = ['WIP']
    def __init__(self):
        self.WIPlimit = inf
    def run(self,WIP):
        return WIP < self.WIPlimit