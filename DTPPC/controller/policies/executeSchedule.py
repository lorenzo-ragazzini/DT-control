# -*- coding: utf-8 -*-
from DTPPC.operationalController import ControlPolicy

class ExecuteSchedule(ControlPolicy):
    def solve(self,*args,**kwargs):
        sequence = self._controller.decisionVariables['sequence']
        admission = self._controller.decisionVariables['admission']
        if len(sequence)>0:
            index = min(sequence)
            if admission[index]:
                admission.pop(index), sequence.pop(index)
            return {'sequence' : sequence, 'admission' : admission}