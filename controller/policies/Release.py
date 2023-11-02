# -*- coding: utf-8 -*-

from operationalController import ControlPolicy

class Release(ControlPolicy):
    inputParameters = ['WIP']
    def run(self,WIP):
        return WIP < self.WIPlimit