from operationalController import OperationalController

class SmartController(OperationalController):
    dt = None
    def __init__(self):
        self.systemModel['orders'] = None
        n_orders = len(self.systemModel['orders'])
        self.decisionVariables = {'sequence':list(range(1,1+n_orders))}
        self.decisionVariables['admission'] = [False for i in range(n_orders)]
        self.systemModel.update({'WIP':0})
    async def send_async(self,event):
        super().send(event)