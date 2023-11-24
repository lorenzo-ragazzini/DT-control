import requests
from DTPPC.implementation.flask.front import DTInterface
from DTPPC.implementation.controller.controller import SmartController, ExecuteSchedule, Release, GenerateSchedule, SetWIP, ControlMap, Rule1, Rule2, Rule3, Rule4
from DTPPC.implementation.local.planned_orders import planned_orders
dt = DTInterface("127.0.0.1:5000")

ctrl = SmartController()
ctrl.dt = dt
ctrl.policies = [ExecuteSchedule(), Release(WIPlimit=5), GenerateSchedule(), SetWIP()]
ctrl.linkPolicies()
ctrl.map = ControlMap()
ctrl.map.rules = [Rule1(), Rule2(), Rule3(), Rule4()]
ctrl.systemModel['orders'] = planned_orders()
ctrl.send('start')
