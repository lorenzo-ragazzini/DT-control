from operationalController import OperationalController
from .sync import planned_orders

class SmartController(OperationalController):
    dt = None
    def __init__(self):
        self.systemModel['orders'] = planned_orders()
        n_orders = len(self.systemModel['orders'])
        self.decisionVariables = {'sequence':list(range(1,1+n_orders))}
        self.decisionVariables['admission'] = [False for i in range(n_orders)]
        self.systemModel.update({'WIP':0})