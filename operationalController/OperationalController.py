from typing import List, Dict, Any, Union, Iterable
from abc import ABC, abstractmethod
from .ControlMap import ControlMap
from .ControlPolicy import ControlPolicy
from .ControlModule import ControlModule

class OperationalController:
    map:ControlMap
    policies:Iterable[ControlPolicy] = list()
    modules:Iterable[ControlModule] = list()
    def send(self,event):
        policies:Iterable[ControlPolicy] = self.map(event)
        for cp in policies:
            self._execute(cp)
    def _execute(self,cp:ControlPolicy):
        pars = cp.getInputParamters()
        input = self._search(Iterable[str])
        dv = cp(input)
    @abstractmethod
    def _search(self,input:str) -> List[Any]:
        pass
    def __getattr__(self,attr):
        try:
            value = [p for p in self.policies+self.modules if p.__class__.__name__ is attr]
            if not value:
                raise AttributeError
            else:
                return value
            return [p for p in self.policies+self.modules if p.__class__.__name__ is attr]
        except:
            object().__getattr__(self,attr)