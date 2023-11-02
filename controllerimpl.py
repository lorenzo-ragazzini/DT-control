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
cmap = ControlMap()
executeSchedule = ExecuteSchedule()
admit = Admit()
r1 = Rule1()
r2 = Rule2()

ctrl.map = cmap
cmap.rules = {'r1':r1, 'r2':r2}
r1.target = {'t',[executeSchedule,admit]}
r2.target = {'t',[admit]}


def gefromtype():
    pass