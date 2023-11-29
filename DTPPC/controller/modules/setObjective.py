# -*- coding: utf-8 -*-
from time import sleep
from DTPPC.operationalController import ControlModule

class SetObjective(ControlModule):
    def __init__(self,timeout=600) -> None:
        self.timeout = timeout
    def solve(self):
        while True:
            sleep(self.timeout)