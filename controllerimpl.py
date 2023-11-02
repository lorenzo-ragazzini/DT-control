from operationalController import ControlPolicy, ControlMap, ControlModule, ControlRule, OperationalController


from controller.policies import GenerateSchedule, ExecuteSchedule, Release
from controller.smartController import SmartController
from controller.modules import SetObjective, SetWIP


class Rule1(ControlRule):
    trigger = 'new'

class Rule2(ControlRule):
    trigger = 'completion'

class Controller(OperationalController):
    pass

class SetObjective(ControlModule):
    pass



ctrl = Controller()
ctrl.dt = 1
ctrl.policies = [ExecuteSchedule(), Release()]
ctrl.map = ControlMap()
ctrl.map.rules = [Rule1(), Rule2()]
