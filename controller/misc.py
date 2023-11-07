# -*- coding: utf-8 -*-

class SimulationRequest(dict):
    def __init__(self):
        self['input'] = {'simLength':'01:00:00'}
        # self['simLength'] = '01:00:00'
        self['nrOfSimul'] = 1
        self['output'] = ['th']
        super().__init__()