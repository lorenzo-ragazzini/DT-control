from DTPPC.operationalController import ControlPolicy, ControlMap, ControlModule, ControlRule, OperationalController
from DTPPC.digitaltwin import DigitalTwin
from DTPPC.controller.policies import GenerateSchedule, ExecuteSchedule, Release
from DTPPC.controller import SmartController
from DTPPC.controller.modules import SetObjective, SetWIP, UpdateWIP
from DTPPC.implementation.controller.events import EventListenerMsg
from DTPPC.implementation.controller.uploader import SendDV
import asyncio

class SmartController(SmartController):
    async def send(self,event):
        super().send(event)

class Rule1(ControlRule):
    trigger = 'new'
    def run(self,event):
        return [Release,ExecuteSchedule]
        
class Rule2(ControlRule):
    trigger = 'completion'
    def run(self,event):
        return [UpdateWIP]
    
class Rule3(ControlRule):
    trigger = 'start'
    def run(self,event):
        # return [SetWIP,GenerateSchedule]
        return [GenerateSchedule]    

class Rule4(ControlRule):
    trigger = '?'
    def run(self,event):
        return [SetObjective]

def main():
    dt = DigitalTwin()
    ctrl = SmartController()
    ctrl.dt = dt
    ctrl.policies = [ExecuteSchedule(), Release(WIPlimit=5), GenerateSchedule(), SetWIP()]
    ctrl.linkPolicies()
    ctrl.map = ControlMap()
    ctrl.map.rules = [Rule1(), Rule2(), Rule3(), Rule4()]
    ctrl.decisionVariables._callback = None
    e = EventListenerMsg('events',1)
    d = SendDV('dv')
    e.ctrl = ctrl
    ctrl.decisionVariables._callback = d.run
    asyncio.run(e.async_listen(),debug=True)

if __name__ == '__main__':
    main()