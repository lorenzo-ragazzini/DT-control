from operationalController import ControlPolicy, ControlMap, ControlModule, ControlRule, OperationalController
from digitaltwin import DigitalTwin

from controller.policies import GenerateSchedule, ExecuteSchedule, Release
from controller import SmartController
from controller.modules import SetObjective, SetWIP


class Rule1(ControlRule):
    trigger = 'new'

class Rule2(ControlRule):
    trigger = 'completion'

class Controller(OperationalController):
    pass

class SetObjective(ControlModule):
    pass

if __name__ == '__main__':
    dt = DigitalTwin()
    # dt.start()
    ctrl = Controller()
    ctrl.dt = dt
    ctrl.policies = [ExecuteSchedule(), Release()]
    ctrl.map = ControlMap()
    ctrl.map.rules = [Rule1(), Rule2()]
