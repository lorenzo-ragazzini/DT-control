# -*- coding: utf-8 -*-
from operationalController import ControlPolicy

class ExecuteSchedule(ControlPolicy):
    # sequence
    def solve(self,*args,**kwargs):
        sequence = self._controller.decisionVariables['sequence']
        if len(sequence)>0:
            self.sequence.pop(0)
            return {'sequence' : self.sequence}