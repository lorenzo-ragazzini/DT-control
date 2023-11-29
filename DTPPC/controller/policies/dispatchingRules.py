from DTPPC.operationalController import ControlPolicy
from abc import abstractmethod

class DispatchingRule(ControlPolicy):
    inputParameters = ['orders']
    def __init__(self) -> None:
        self.unscheduled = []
        super().__init__()
    def solve(self,input):
        sequence = self._controller.decisionVariables['sequence']
        new_orders = [order for order in input['orders'].Order if order not in sequence.keys()]
        sequence = self.sort(new_orders,sequence)
        return {"sequence":sequence}
    @abstractmethod
    def sort(jobs):
        pass
    def dictmax(self,items):
        if not items:
            return 0
        else: 
            return items[max(items)]

class FIFODispatchingRule(DispatchingRule):
    def sort(self,new_orders,sequence):
        for order in new_orders:
            sequence[order] = self.dictmax(sequence) + 1
        return sequence

class LIFODispatchingRule(DispatchingRule):
    def sort(self,new_orders,sequence):
        for order in reversed(new_orders):
            sequence[order] = self.dictmax(sequence) + 1
        return sequence