from operationalController import ControlPolicy, ControlMap, ControlModule, ControlRule, OperationalController


from controller.policies.schedule import GenerateSchedule, ExecuteSchedule, Release

       
class SetWIP(ControlPolicy):
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
ctrl.policies = [ExecuteSchedule(), Release()]
ctrl.map = ControlMap()
ctrl.map.rules = [Rule1(), Rule2()]
