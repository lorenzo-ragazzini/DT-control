from DTPPC.operationalController import OperationalController

class SmartController(OperationalController):
    dt = None
    def __init__(self):
        self.systemModel['orders'] = []
        self.decisionVariables = {'sequence':list(range(1,1+self.n_orders))}
        self.decisionVariables['admission'] = [False for i in range(self.n_orders)]
        self.systemModel.update({'WIP':0})
    @property
    def n_orders(self):
        return len(self.systemModel['orders'])
    async def send(self,event):
        super().send(event)