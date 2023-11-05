from typing import List, Dict, Any, Union, Iterable, Type
from abc import ABC, abstractmethod
from collections import ChainMap
from .controlMap import ControlMap
from .controlPolicy import ControlPolicy
from .controlModule import ControlModule

class OperationalController:
    map:ControlMap
    policies:Iterable[ControlPolicy] = list()
    modules:Iterable[ControlModule] = list()
    decisionVariables = dict()
    systemModel = {}
    def addPolicy(self,Cp:Type[ControlPolicy]):
        self.policies.append(Cp(self))
    def addModule(self,Cm:Type[ControlModule]):
        self.modules.append(Cm(self))
    def linkPolicies(self):
        for cp in self.policies+self.modules:
            cp._controller = self
    def send(self,event):
        policies:Iterable[Type[ControlPolicy]] = self.map(event)
        for cp in policies:
            self._execute(self[cp])
    def _execute(self,cp:ControlPolicy):
        pars = cp.getInputParamters()
        input = self._search(pars)
        dv = cp(input=input)
        self.decisionVariables.update(dv)
    @abstractmethod
    def _search(self,input:Iterable[str]) -> List[Any]:
        return dict(ChainMap(*[{el:self.systemModel[el]} for el in input]))
    def __getattr__(self,attr):
        try:
            value = [p for p in self.policies+self.modules if p.__class__.__name__ is attr]
            if not value:
                raise AttributeError
            else:
                return value[0]
            return [p for p in self.policies+self.modules if p.__class__.__name__ is attr]
        except:
            object.__getattribute__(self,attr)
    def __getitem__(self,item):
        if type(item) is type:
            return self.__getattr__(item.__name__)