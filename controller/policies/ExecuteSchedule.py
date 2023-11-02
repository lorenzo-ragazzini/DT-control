# -*- coding: utf-8 -*-
from operationalController import ControlPolicy

class ExecuteSchedule(ControlPolicy):
    # sequence
    def run(self):
        if len(self.sequence)>0:
            return self.sequence.pop(0)