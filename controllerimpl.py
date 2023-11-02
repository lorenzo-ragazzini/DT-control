from operationalController import ControlPolicy, ControlMap, ControlModule, ControlRule, OperationalController

class ExecuteSchedule(ControlPolicy):
    # sequence
    def run(self):
        if len(self.sequence)>0:
            return self.sequence.pop(0)
        
class Admit(ControlPolicy):
    inputParameters = ['WIP']
    def run(self,WIP):
        return WIP < self.WIPlimit
    
class Schedule(ControlPolicy):
    pass

class SetWIP(ControlPolicy):
    pass
    
class ControlMap(ControlMap):
    pass

class Rule1(ControlRule):
    trigger = 'new'

class Rule2(ControlRule):
    trigger = 'completion'

class Controller(OperationalController):
    pass

class SetObjective(ControlModule):
    pass



ctrl = Controller()
ctrl.policies = [ExecuteSchedule(), Admit()]
ctrl.map = ControlMap()
ctrl.map.rules = [Rule1(), Rule2()]
