from operationalController import ControlPolicy
from abc import abstractmethod

class DispatchingRule(ControlPolicy):
    def __init__(self) -> None:
        self.unscheduled = []
        super().__init__()
    def run(self,input):
        df = input["df"]
        mode = input['mode']
        if mode == "All":
            jobs = []
        elif mode == "New":
            self.unscheduled = []
            jobs = []
            pass
        self.sort(jobs)
    @abstractmethod
    def sort(jobs):
        pass

class FIFODispatchingRule(DispatchingRule):
    def sort(self,jobs):
        pass

