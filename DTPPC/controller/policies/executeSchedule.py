# -*- coding: utf-8 -*-
from DTPPC.operationalController import ControlPolicy

class ExecuteSchedule(ControlPolicy):
    # sequence
    def solve(self,*args,**kwargs):
        sequence = self._controller.decisionVariables['sequence']
        admission = self._controller.decisionVariables['admission']
        if len(sequence)>0:
            admission.pop(0)
            sequence.pop(0)
            return {'sequence' : sequence, 'admission' : admission}
