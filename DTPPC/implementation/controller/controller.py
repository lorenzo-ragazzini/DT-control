from DTPPC.controller.modules.bottleneckPrediction import BottleneckPrediction
from DTPPC.operationalController import ControlPolicy, ControlMap, ControlModule, ControlRule, OperationalController
from DTPPC.controller.policies import GenerateSchedule, ExecuteSchedule, ReleaseOne
from DTPPC.controller.policies.dispatchingRules import FIFODispatchingRule
from DTPPC.controller import SmartController
from DTPPC.controller.modules import SetObjective, SetWIP
import asyncio
import time

class SmartController(SmartController):
    def __init__(self):
        super().__init__()
        self.systemModel.update({'orders':[]})
        self.decisionVariables = {'sequence':dict(), "admission":dict()}
        self.systemModel.update({'WIP':0})
        self.actuator = None
    def init_dv(self):
        orders = self.systemModel['orders']['Order']
        sequence = dict(zip(orders, list(range(1,1+self.n_orders))))
        admission = dict(zip(orders, [True for i in range(self.n_orders)]))
        self.decisionVariables.update({"sequence":sequence,"admission":admission})
    @property
    def n_orders(self):
        return len(self.systemModel['orders'])
    async def send_async(self,event):
        print(event)
        super().send(event)
    def execute(self, c: ControlPolicy):
        print(type(c).__name__)
        dv = super().execute(c)
        print(dv)
        if self.actuator and dv:
            self.actuator.act(dv)

class Rule1(ControlRule):
    trigger = 'new'
    def run(self,event):
        return [ReleaseOne,ExecuteSchedule]
        
class Rule2(ControlRule):
    trigger = 'completion'
    def run(self,event):
        self._controller.systemModel['WIP'] -= 1
        return []

class Rule2bis(ControlRule):
    trigger = 'completion'
    def run(self,event):
        self._controller.systemModel['WIP'] -= 1
        self.run_delayed()
        return []
    def run_delayed(self):
        time.sleep(4)
        asyncio.run(self._controller.send_async('new'))
    
class Rule3(ControlRule):
    trigger = 'start'
    def run(self,event):
        return [GenerateSchedule,SetWIP,SetObjective,BottleneckPrediction]    
    
class Rule4(ControlRule):
    trigger = 'arrival'
    def run(self,event):
        return [FIFODispatchingRule]
    
class Rule5(ControlRule):
    trigger = 'startUnscheduled'
    def run(self,event):
        return [FIFODispatchingRule]
    
def create_controller() -> SmartController:
    ctrl = SmartController()
    ctrl.policies = [ExecuteSchedule(), ReleaseOne(WIPlimit=5), GenerateSchedule(), SetWIP(), FIFODispatchingRule(), BottleneckPrediction(), SetObjective()]
    ctrl.linkPolicies()
    ctrl.map = ControlMap()
    ctrl.map.rules = [Rule1(), Rule2(), Rule3(), Rule4(), Rule5()]
    ctrl.linkRules()
    return ctrl

if __name__ == '__main__':
    from DTPPC.digitaltwin import DigitalTwin
    dt = DigitalTwin()
    ctrl = SmartController()
    ctrl.policies = [ExecuteSchedule(), ReleaseOne(WIPlimit=5), GenerateSchedule(), SetWIP()]
    ctrl.linkPolicies()
    ctrl.map = ControlMap()
    ctrl.map.rules = [Rule1(), Rule2(), Rule3(), Rule4()]
    ctrl.linkRules()
    ctrl.send('start')