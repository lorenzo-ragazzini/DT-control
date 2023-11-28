from DTPPC.operationalController import ControlPolicy, ControlMap, ControlModule, ControlRule, OperationalController
from DTPPC.controller.policies import GenerateSchedule, ExecuteSchedule, Release
from DTPPC.controller import SmartController
from DTPPC.controller.modules import SetObjective, SetWIP, UpdateWIP
import asyncio

class SmartController(SmartController):
    def __init__(self):
        super().__init__()
        self.systemModel.update({'orders':[]})
        self.decisionVariables = {'sequence':list(range(1,1+self.n_orders))}
        self.decisionVariables['admission'] = [False for i in range(self.n_orders)]
        self.systemModel.update({'WIP':0})
        self.actuator = None
    @property
    def n_orders(self):
        return len(self.systemModel['orders'])
    async def send_async(self,event):
        print(event)
        super().send(event)
    def execute(self, c: ControlPolicy):
        print(type(c))
        dv = super().execute(c)
        print(dv)
        self.actuator.act(dv)

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

def main() -> SmartController:
    ctrl = SmartController()
    ctrl.dt = dt
    ctrl.policies = [ExecuteSchedule(), Release(WIPlimit=5), GenerateSchedule(), SetWIP()]
    ctrl.linkPolicies()
    ctrl.map = ControlMap()
    ctrl.map.rules = [Rule1(), Rule2(), Rule3(), Rule4()]
    return ctrl


if __name__ == '__main__':
    from DTPPC.digitaltwin import DigitalTwin
    dt = DigitalTwin()
    ctrl = SmartController()
    ctrl.dt = dt
    ctrl.policies = [ExecuteSchedule(), Release(WIPlimit=5), GenerateSchedule(), SetWIP()]
    ctrl.linkPolicies()
    ctrl.map = ControlMap()
    ctrl.map.rules = [Rule1(), Rule2(), Rule3(), Rule4()]
    ctrl.send('start')