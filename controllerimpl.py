from operationalController import ControlPolicy, ControlMap, ControlModule, ControlRule, OperationalController
from digitaltwin import DigitalTwin

from controller.policies import GenerateSchedule, ExecuteSchedule, Release
from controller import SmartController
from controller.modules import SetObjective, SetWIP


class Rule1(ControlRule):
    trigger = 'new'
    def run(self,event):
        return [Release,ExecuteSchedule]
        
class Rule2(ControlRule):
    trigger = 'completion'
    def run(self,event):
        return None

class Controller(SmartController):
    def __init__(self):
        self.decisionVariables = {'sequence':[]}
        self.decisionVariables['admission'] = [False for i in range(len(self.decisionVariables['sequence']))]

class SetObjective(ControlModule):
    pass

if __name__ == '__main__':
    dt = DigitalTwin()
    # dt.start()
    ctrl = Controller()
    ctrl.dt = dt
    ctrl.policies = [ExecuteSchedule(), Release(WIPlimit=5)]
    ctrl.linkPolicies()
    
    # ctrl.addPolicy(ExecuteSchedule)
    # ctrl.addPolicy(Release)
    ctrl.map = ControlMap()
    ctrl.map.rules = [Rule1(), Rule2()]

    ctrl.send('new')